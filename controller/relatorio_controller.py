from flask import Blueprint, request, jsonify, send_file
from db.database import SessionLocal
from service.relatorio_service import ServicoRelatorio
from service.verificacao_service import ServicoVerificacao
from tasks.relatorio_tasks import gerar_relatorio_assincrono
from repository.relatorio_repository import RepositorioRelatorio
from model.relatorio_model import Relatorio
import os

bp_rel = Blueprint('relatorio', __name__)

@bp_rel.route('/', methods=['POST'])
def criar_relatorio():
    dados = request.get_json() or {}
    try:
        tipo = dados['tipo']
        formato = dados['formato']
        id_verificacao = int(dados['id_verificacao'])
        criado_por = dados['criado_por']
    except (KeyError, ValueError) as e:
        return jsonify({"erro": f"Parâmetros inválidos: {str(e)}"}), 400

    db = SessionLocal()
    try:
        servico = ServicoRelatorio(db)
        relatorio = servico.gerar_relatorio(
            tipo=tipo,
            formato=formato, 
            id_verificacao=dados.get('id_verificacao'),
            criado_por=dados.get('criado_por')
        )
        return jsonify(relatorio.para_dict()), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

@bp_rel.route('/votos', methods=['GET'])
def relatorio_votos():
    id_eleicao = request.args.get('id_eleicao')
    
    if not id_eleicao:
        return jsonify({
            "erro": "Parâmetro 'id_eleicao' é obrigatório",
            "exemplo": "/relatorio/votos?id_eleicao=6294de21-2810-4e19-bb19-4c4b5830cb2c"
        }), 400

    db = SessionLocal()
    try:
        servico = ServicoVerificacao(db)
        relatorio = servico.gerar_relatorio_votos(id_eleicao)
        
        if "erro_critico" in relatorio:
            return jsonify(relatorio), 500
            
        return jsonify(relatorio)
    except Exception as e:
        return jsonify({
            "erro": "Falha no servidor",
            "detalhes": str(e)
        }), 500
    finally:
        db.close()

@bp_rel.route('/assincrono', methods=['POST'])
def criar_relatorio_assincrono():
    dados = request.get_json() or {}
    try:
        tipo = dados['tipo']
        formato = dados['formato']
        id_verificacao = int(dados['id_verificacao'])
        criado_por = dados.get('criado_por', 'sistema_assincrono')
    except (KeyError, ValueError) as e:
        return jsonify({"erro": f"Parâmetros inválidos: {str(e)}"}), 400

    task = gerar_relatorio_assincrono.delay(tipo, formato, id_verificacao, criado_por)

    return jsonify({
        "mensagem": "Criação de relatório assíncrona iniciada",
        "task_id": task.id
    }), 202

@bp_rel.route('/<int:relatorio_id>', methods=['GET'])
def buscar_relatorio(relatorio_id):
    db = SessionLocal()
    try:
        servico = ServicoRelatorio(db)
        relatorio = servico.buscar_relatorio(relatorio_id)
        if relatorio:
            return jsonify(relatorio.para_dict())
        else:
            return jsonify({"mensagem": "Relatório não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

@bp_rel.route('/download/<int:relatorio_id>', methods=['GET'])
def download_relatorio(relatorio_id):
    db = SessionLocal()
    try:
        servico = ServicoRelatorio(db)
        relatorio = servico.buscar_relatorio(relatorio_id)
        if relatorio:
            if not os.path.exists(relatorio.caminho):
                return jsonify({"erro": "Arquivo de relatório não encontrado no servidor"}), 404
            return send_file(relatorio.caminho, as_attachment=True, download_name=os.path.basename(relatorio.caminho))
        else:
            return jsonify({"mensagem": "Relatório não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

@bp_rel.route('/listar', methods=['GET'])
def listar_relatorios():
    db = SessionLocal()
    try:
        pagina = int(request.args.get('pagina', 1))
        limite = int(request.args.get('limite', 10))
        
        repositorio = RepositorioRelatorio(db)
        relatorios, total_paginas = repositorio.listar_relatorios_paginados(pagina, limite)
        total_relatorios = db.query(Relatorio).count()
        
        relatorios_serializados = [r.para_dict() for r in relatorios]
        
        return jsonify({
            "relatorios": relatorios_serializados,
            "total": total_relatorios,
            "pagina_atual": pagina,
            "total_paginas": total_paginas
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()