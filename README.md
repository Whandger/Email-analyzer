📧 Email AI Classifier
https://img.shields.io/badge/Python-3.10+-blue.svg
https://img.shields.io/badge/Flask-2.3.3-green.svg
https://img.shields.io/badge/Render-Deploy-blueviolet

Deploy Ativo: 🌐 https://email-analyzer-dx4v.onrender.com/

Classificador inteligente de emails que usa IA para analisar emails e documentos PDF, categorizando automaticamente e sugerindo respostas. A aplicação já está em produção e pode ser testada através do link acima.

✨ Funcionalidades
✅ Análise automática de emails (texto e PDF)

🤖 Classificação por IA em 8 categorias:

📄 CURRICULO - Currículos e candidaturas

💰 FINANCEIRO - Faturas, boletos, documentos

🚨 IMPORTANTE - Emails urgentes

🎓 EDUCACIONAL - Comunicação acadêmica

💼 PROFISSIONAL - Emails corporativos

📭 SPAM - Promoções e marketing

⚠️ PHISHING - Emails suspeitos

📧 ROTINA - Emails normais

📊 Score de utilidade (0-100%)

🏷️ Tags automáticas baseadas no conteúdo

📝 Resumo inteligente do conteúdo

💬 Sugestão de resposta automática

🌐 Deploy em produção no Render

🚀 Como Usar (Aplicação Online)
A aplicação já está em produção e pode ser usada diretamente:

Acesse a aplicação: https://email-analyzer-dx4v.onrender.com/

Cole um texto na área de texto

Ou envie um arquivo PDF/TXT

Clique em "Analisar Email"

Veja os resultados em tempo real

Teste Imediato
URL: https://email-analyzer-dx4v.onrender.com/

Não requer instalação

Processa PDFs e texto puro

Resultados instantâneos

🛠️ Instalação Local (Desenvolvimento)
Pré-requisitos
Python 3.10+

pip (gerenciador de pacotes)

Git (opcional)

Passo a Passo
Clone o repositório:

bash
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer
Instale dependências:

bash
pip install -r requirements.txt
Configure (opcional):
Edite server/config/config.py para adicionar seu token:

python
HF_TOKEN = "hf_seu_token_aqui"  # Token do Hugging Face (opcional)
Execute a aplicação:

bash
# Modo desenvolvimento:
python server/app.py
Acesse localmente:

text
http://localhost:5000
📁 Estrutura do Projeto
text
Email-analyzer/
├── server/                    # Backend Flask
│   ├── app.py                # Aplicação principal
│   ├── config/
│   │   └── config.py         # Configurações
│   ├── utils/
│   │   ├── text_processor.py # Processador de texto
│   │   └── hugg_handler.py   # Integração com IA
│   └── routes/
│       └── api.py            # Rotas da API
├── static/                   # Arquivos estáticos
│   ├── css/
│   │   └── index.css        # Estilos
│   └── js/
│       └── email.js         # JavaScript
├── templates/
│   └── index.html           # Página principal
├── requirements.txt         # Dependências Python
├── runtime.txt             # Versão do Python (Render)
├── render.yaml             # Configuração Render
└── README.md               # Este arquivo
🔧 Configuração da IA
Com Token do Hugging Face (Opcional)
Crie conta em huggingface.co

Vá em Settings → Access Tokens → New Token

Copie o token (começa com hf_)

Adicione como variável de ambiente HF_TOKEN

Sem Token (Modo Local)
Usa análise por keywords

Funciona para categorização básica

É o modo atual em produção

🚀 Deploy no Render (Como foi Feito)
Configuração do Render
O projeto está configurado para deploy automático no Render:

render.yaml:

yaml
services:
  - type: web
    name: email-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server.app:app
    envVars:
      - key: HF_TOKEN
        sync: false
      - key: PYTHONUNBUFFERED
        value: true
requirements.txt:

txt
Flask==2.3.3
Flask-CORS==4.0.0
gunicorn==21.2.0
requests==2.31.0
python-dotenv==1.0.0
pdfplumber==0.10.3
PyPDF2==3.0.1
chardet==5.2.0
nltk==3.8.1
runtime.txt:

txt
python-3.10.12
Deploy Automático
Conecte o repositório no Render

Use as configurações acima

Deploy automático a cada push para main

URL gerada: https://email-analyzer-*.onrender.com

📊 Exemplo de Uso na Aplicação Online
1. Acesse: https://email-analyzer-dx4v.onrender.com/

2. Digite um exemplo:

text
Olá, envio meu currículo para vaga de desenvolvedor.
Experiência: Python, Django, PostgreSQL.
LinkedIn: linkedin.com/in/exemplo
3. Resultado esperado:

📊 Utilidade: 90%+

🏷️ Categoria: CURRICULO

📝 Resumo: Currículo profissional detectado...

💬 Resposta: ✅ Currículo recebido com sucesso!

🔖 Tags: python, django, profissional

🔍 API Endpoints
POST /analyze
Disponível em: https://email-analyzer-dx4v.onrender.com/analyze

Analisa conteúdo de email.

Parâmetros:

content (texto): Conteúdo do email

file (arquivo): PDF ou TXT (opcional)

Resposta:

json
{
  "utilidade": 0.92,
  "categoria": "CURRICULO",
  "resumo": "Currículo profissional...",
  "acao_necessaria": true,
  "tags": ["python", "django"],
  "resposta": "✅ Currículo recebido com sucesso!",
  "fonte": "huggingface_api"
}
🐛 Troubleshooting
Problemas no Deploy
Aplicação lenta no Render:

Render Free Tier tem cold starts

Primeiro acesso pode demorar 30-60s

Após inicializado, funciona normalmente

Erro "Service Unavailable":

Recarrege a página após 60 segundos

Verifique o status em Render Status

Free Tier tem limites de uso

PDF não processa:

Tamanho máximo: 10MB

Use PDFs com texto (não apenas imagens)

Formatos aceitos: PDF, TXT

Logs e Monitoramento
Logs do Render: Dashboard → Seu Serviço → Logs

Status da API: Acesse /health (se implementado)

Uso de recursos: Render Dashboard → Metrics

📈 Próximos Passos
Adicionar endpoint /health para monitoramento

Implementar cache para melhor performance

Adicionar suporte a mais formatos (DOCX)

Criar dashboard de estatísticas

Adicionar autenticação para API

🤝 Contribuindo
Fork o projeto

Crie uma branch (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Add nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request

📄 Licença
MIT License - veja LICENSE para detalhes.

👨‍💻 Autor
Whandger Wolffenbüttel

GitHub: @Whandger

LinkedIn: whandger

Email: whandger@gmail.com

🌐 Links
Aplicação Online: https://email-analyzer-dx4v.onrender.com/

Repositório: https://github.com/Whandger/Email-analyzer

Issues/Bugs: GitHub Issues

⭐ Gostou do projeto? Dê uma estrela no GitHub! ⭐

https://img.shields.io/github/stars/Whandger/Email-analyzer?style=social
https://img.shields.io/github/forks/Whandger/Email-analyzer?style=social

Teste agora: https://email-analyzer-dx4v.onrender.com/
