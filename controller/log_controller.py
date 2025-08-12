from flask import Blueprint, request, jsonify
from db.database import SessionLocal
from service.log_service import ServicoLog
from repository.log_repository import RepositorioLog
from tasks.log_tasks import registrar_log_assincrono
from model.log_model import Log  

log_bp = Blueprint("log", __name__)

@log_bp.route('teste')
def hello_log():
    return jsonify({"mensagem": "Rota de teste do log funcionando!"})

@log_bp.route('/', methods=['POST'])
def criar_log():    
    dados = request.get_json() or {}
    try:
        tipo = dados['tipo']
        descricao = dados['descricao']
    except KeyError as e:
        return jsonify({
            "erro": "Campos obrigatórios faltando",
            "detalhes": f"Campo '{e.args[0]}' é requerido",
            "campos_esperados": {
                "tipo": "string (ex: 'INFO', 'ERRO')",
                "descricao": "string",
                "id_verificacao": "int (opcional)",
                "id_relatorio": "int (opcional)"
            }
        }), 400

    db = SessionLocal()
    try:
        # salvando descricao + tipo
        servico = ServicoLog(db)
        log = servico.registrar_log(
            tipo=tipo,
            descricao=descricao,
            id_verificacao=dados.get('id_verificacao'),
            id_relatorio=dados.get('id_relatorio'),
        )
        return jsonify(log.para_dict()), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

#revisar log assincrono
@log_bp.post('/assincrono')
def criar_log_assincrono():
    dados = request.get_json() or {}
    try:
        tipo = dados['tipo']
        descricao = dados['descricao']
    except KeyError as e:
        return jsonify({
            "erro": "Campos obrigatórios faltando",
            "detalhes": f"Campo '{e.args[0]}' é requerido",
            "campos_esperados": {
                "tipo": "string (ex: 'INFO', 'ERRO')",
                "descricao": "string",
                "id_verificacao": "int (opcional)",
                "id_relatorio": "int (opcional)"
            }
        }), 400

    task = registrar_log_assincrono.delay(
        tipo,
        descricao,
        dados.get('id_verificacao'),
        dados.get('id_relatorio')
    )
    
    return jsonify({
        "mensagem": "Registro de log assíncrono iniciado",
        "task_id": task.id
    }), 202

@log_bp.get('/listar')
def listar_logs():
    db = SessionLocal()
    try:
        pagina = int(request.args.get('pagina', 1))
        limite = int(request.args.get('limite', 10))
        
        repositorio = RepositorioLog(db)
        logs, total_paginas = repositorio.listar_logs_paginados(pagina, limite)
        total_logs = db.query(Log).count()
        
        return jsonify({
            "logs": [log.para_dict() for log in logs],
            "total": total_logs,
            "pagina_atual": pagina,
            "total_paginas": total_paginas
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()

@log_bp.get('/listar/<int:log_id>')
def buscar_log(log_id: int):
    db = SessionLocal()
    try:
        servico = ServicoLog(db)
        log = servico.buscar_log(log_id)
        if log:
            return jsonify(log.para_dict())
        return jsonify({"mensagem": "Log não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        db.close()
