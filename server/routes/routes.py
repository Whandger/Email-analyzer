# server/routes/routes.py
from flask import Blueprint, render_template, request, jsonify
from server.services.email_service import process_email_analysis

# Define seu blueprint
page_bp = Blueprint('page', __name__)

# Rotas para as páginas
@page_bp.route('/')
def index():
    return render_template('index.html')

# Rota para análise de email
@page_bp.route('/analyze', methods=['POST'])
def analyze_email():
    """
    Endpoint para análise de email
    Recebe: texto do email e/ou arquivo
    Retorna: análise do Gemini
    """
    try:
        # Obter dados do request
        email_text = request.form.get('email_text', '')
        file = request.files.get('file')
        
        # Validar que há conteúdo
        if not email_text and (not file or not file.filename):
            return jsonify({'error': 'Por favor, insira o texto do email ou selecione um arquivo.'}), 400
        
        # Processar análise
        result = process_email_analysis(email_text, file)
        
        return jsonify(result)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Erro interno no processamento: {str(e)}")
        return jsonify({'error': 'Erro interno no servidor. Tente novamente.'}), 500

# Rota de teste da API (opcional)
@page_bp.route('/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'online',
        'service': 'email-analyzer',
        'version': '1.0'
    })