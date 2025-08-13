import os, sys
from flask import Flask, jsonify
from dotenv import load_dotenv
import logging
from datetime import datetime
import socket
from db.database import Base, engine

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

load_dotenv(os.path.join(ROOT, '.env'))

from controller.log_controller import log_bp
from controller.verificacao_controller import bp_ver
from controller.relatorio_controller import bp_rel
from db.database import close_session

def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @app.route('/healthcheck')
    def healthcheck():
        return jsonify({
            "status": "online",
            "service": "auditoria-service",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "hostname": socket.gethostname(),
            "endpoints": [
                "/logs",
                "/verificacoes",
                "/relatorios"
            ]
        })

    app.register_blueprint(log_bp, url_prefix='/log')
    app.register_blueprint(bp_ver, url_prefix='/verificacao')
    app.register_blueprint(bp_rel, url_prefix='/relatorio')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro":"Recurso não encontrado","detalhes":str(e)}),404

    @app.errorhandler(400)
    def bad_request(e):
        logger.warning(f"400: {e}")
        return jsonify({"erro":"Requisição inválida","detalhes":str(e)}),400

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"500: {e}")
        return jsonify({"erro":"Erro interno do servidor","detalhes":str(e)}),500

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        close_session()

    return app

if __name__ == '__main__':
    app = create_app()
    Base.metadata.create_all(bind=engine)
    app.run(host='0.0.0.0', port=8000, debug=True)