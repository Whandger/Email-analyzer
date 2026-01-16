from flask import Flask
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

def create_app():
    print("Criando app e registrando blueprints...")

    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'template'),
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
    )

    # Configurações
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
    app.config['SECRET_KEY'] = os.urandom(24)
    
    # Validar chave Gemini
    from server.config.config import Config
    try:
        Config.validate()
        print("✓ Configuração hugging validada com sucesso")
    except ValueError as e:
        print(f"⚠️  Aviso: {e}")
        print("⚠️  O sistema funcionará, mas a análise por IA não estará disponível")

    # Registrar blueprints
    print(app.url_map)
    if 'page' not in app.blueprints:
        from server.routes.routes import page_bp
        app.register_blueprint(page_bp)
        print(app.url_map)

    # Rota de saúde
    @app.route('/health')
    def health():
        return 'OK', 200

    return app

if __name__ == '__main__':
    app = create_app()
    # Rodar app normalmente, debug True só em desenvolvimento
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug_mode, use_reloader=False, host='0.0.0.0', port=5000)