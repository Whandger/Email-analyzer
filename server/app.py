# app.py - VERSÃO PRODUÇÃO COMPLETA
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'template'),
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
    )

    # 🔒 CONFIGURAÇÕES DE PRODUÇÃO
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.config['TESTING'] = False
    
    # 🔐 Headers de segurança
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    # Validar configuração
    from server.config.config import Config
    
    # Inicialização silenciosa em produção
    if not app.config['DEBUG']:
        print("🚀 Iniciando Perplexity Email Analyzer...")
    
    perplexity_available = Config.is_perplexity_available()
    
    if not perplexity_available:
        app.logger.error("Perplexity API não configurada")
        app.config['PERPLEXITY_ENABLED'] = False
        app.config['ERROR_MODE'] = True
    else:
        app.config['PERPLEXITY_ENABLED'] = True
        app.config['ERROR_MODE'] = False
        if app.config['DEBUG']:
            print(f"✅ Perplexity configurado - Modelo: {Config.PERPLEXITY_DEFAULT_MODEL}")

    # Registrar blueprints
    from server.routes.routes import page_bp
    app.register_blueprint(page_bp)
    
    # 🔧 Rotas de monitoramento (importantes para produção)
    @app.route('/health')
    def health():
        return jsonify({
            'status': 'healthy' if app.config['PERPLEXITY_ENABLED'] else 'unhealthy',
            'perplexity': Config.is_perplexity_available(),
            'timestamp': os.environ.get('DEPLOY_TIMESTAMP', 'unknown')
        }), 200
    
    @app.route('/metrics')
    def metrics():
        # Rota para métricas (usar com Prometheus)
        from flask import Response
        metrics_data = f"""
# HELP app_requests_total Total number of requests
# TYPE app_requests_total counter
app_requests_total{{status="healthy"}} 1
"""
        return Response(metrics_data, mimetype='text/plain')
    
    # 🛡️ Middleware de segurança
    @app.before_request
    def check_api():
        if request.endpoint == 'page_bp.analyze_email':
            if not Config.is_perplexity_available():
                return jsonify({
                    'error': 'Service unavailable',
                    'message': 'AI service is not configured'
                }), 503
    
    # 📊 Logging em produção
    if not app.config['DEBUG']:
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Configurar logging
        handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)
    
    return app

# Ponto de entrada para WSGI
app = create_app()

if __name__ == '__main__':
    # ⚠️ NÃO usar em produção - apenas para desenvolvimento
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=5000)