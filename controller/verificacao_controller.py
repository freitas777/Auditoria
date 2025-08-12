from flask import Blueprint, request, jsonify
from db.database import SessionLocal
from service.verificacao_service import ServicoVerificacao
from tasks.verificacao_tasks import executar_verificacao_assincrono
from repository.verificacao_repository import RepositorioVerificacao
from model.verificacao_model import Verificacao

bp_ver = Blueprint('verificacao', __name__)

@bp_ver.route('/', methods=['POST'])
def executar_verificacao():
    dados = request.get_json() or {}
    try:
        id_voto = dados.get('id_voto')
        criado_por = dados.get('criado_por', 'sistema')
    except (TypeError, ValueError):
        return jsonify({"erro": "id_voto inválido. Deve ser inteiro."}), 400

    db = SessionLocal()
    try:
        servico = ServicoVerificacao(db)
        verificacao = servico.verificar_voto_por_id(id_voto, criado_por)
        return jsonify(verificacao.para_dict()), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

@bp_ver.route('/', methods=['GET'])
def listar_verificacoes():
    db = SessionLocal()
    try:
        pagina = int(request.args.get('pagina', 1))
        limite = int(request.args.get('limite', 10))

        repositorio = RepositorioVerificacao(db)
        verificacoes, total_paginas = repositorio.listar_verificacoes_paginadas(pagina, limite)
        total = db.query(Verificacao).count()

        return jsonify({
            "verificacoes": [v.para_dict() for v in verificacoes],
            "total": total,
            "pagina_atual": pagina,
            "total_paginas": total_paginas
        })
    finally:
        db.close()

@bp_ver.route('/listar', methods=["GET"])
def obter_ids_votos():
    db = SessionLocal()
    id_eleicao_padrao = 1 
    try:
        servico = ServicoVerificacao(db)
        votos = servico.obter_votos_por_eleicao(id_eleicao_padrao)

        ids_votos = [v["id_voto"] for v in votos]
        return jsonify(ids_votos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
    finally:
        db.close()

@bp_ver.route('/assincrono', methods=['POST'])
def executar_verificacao_assincrona():
    dados = request.get_json() or {}
    try:
        votos = int(dados.get('votos', 0))
        recibos = int(dados.get('recibos', 0))
        criado_por = dados.get('criado_por', 'sistema_assincrono')
    except (TypeError, ValueError) as e:
        return jsonify({
            "erro": "Dados inválidos",
            "detalhes": str(e),
            "campos_esperados": {
                "votos": "número inteiro",
                "recibos": "número inteiro",
                "criado_por": "string (opcional)"
            }
        }), 400
    
    task = executar_verificacao_assincrono.delay(votos, recibos, criado_por)

    return jsonify({
        "mensagem": "Verificação assíncrona iniciada",
        "task_id": task.id
    }), 202
