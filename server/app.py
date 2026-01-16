# server/app.py
from flask import Flask
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

def create_app():
    print("🚀 Iniciando aplicação...")
    
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),  # MUDAR: template -> templates
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
    )

    # Configurações
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
    
    # Verificar se estamos no Render
    IS_RENDER = os.environ.get('RENDER', False)
    if IS_RENDER:
        print("🌐 Ambiente: Render (Produção)")
    
    # Validar configurações
    from server.config.config import Config
    try:
        Config.validate()
        print("✅ Configuração validada com sucesso")
    except ValueError as e:
        print(f"⚠️ Aviso: {e}")
        print("ℹ️ O sistema funcionará, mas a análise por IA não estará disponível")

    # Registrar blueprints
    try:
        from server.routes.routes import page_bp
        app.register_blueprint(page_bp)
        print(f"✅ Blueprint registrado: {page_bp.name}")
    except Exception as e:
        print(f"❌ Erro ao registrar blueprint: {e}")

    # Rota de saúde para Render
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'email-analyzer'}, 200
    
    # Rota raiz para teste
    @app.route('/')
    def index():
        return "🚀 Email Analyzer está funcionando! Acesse /upload para começar."

    print("✅ Aplicação criada com sucesso!")
    return app

# Esta parte só executa se rodar o arquivo diretamente
if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)