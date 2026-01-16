📧 Email AI Classifier




🔗 Aplicação Online:
https://email-analyzer-dx4v.onrender.com

📦 Repositório:
https://github.com/Whandger/Email-analyzer

🧠 Sobre o Projeto

O Email AI Classifier é um classificador inteligente de emails que utiliza Inteligência Artificial para analisar conteúdos de emails e documentos (PDF/TXT), categorizando automaticamente e sugerindo respostas inteligentes.

Ideal para automação de triagem de emails, RH, atendimento ao cliente e organização de mensagens.

✨ Funcionalidades

📩 Análise automática de emails (texto e PDF)

🤖 Classificação por IA em 8 categorias

📊 Score de utilidade (0 a 100%)

🏷️ Geração automática de tags

📝 Resumo inteligente do conteúdo

💬 Sugestão de resposta automática

🚀 Deploy em produção no Render

🚀 Como Usar
🟢 Online (Recomendado)

Acesse
👉 https://email-analyzer-dx4v.onrender.com

Cole um texto ou envie um arquivo PDF/TXT

Clique em "Analisar Email"

Veja os resultados em tempo real

💻 Executando Localmente
# Clone o repositório
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python server/app.py


Acesse no navegador:
👉 http://localhost:5000

📁 Estrutura do Projeto
autoU_ia/
├── server/                     # Backend (Flask)
│   ├── config/                 # Configurações da aplicação
│   │   └── config.py
│   ├── routes/                 # Rotas da API
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/               # Lógica de negócio
│   │   └── email_service.py
│   ├── utils/                  # Utilitários e helpers
│   │   ├── file_handler.py     # Manipulação de arquivos (PDF/TXT)
│   │   ├── hugg_handler.py     # Integração com Hugging Face
│   │   ├── keywords.py         # Palavras-chave e categorias
│   │   └── text_processor.py   # Processamento de texto
│   └── app.py                  # Inicialização do Flask
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/                  # Templates HTML
│   └── index.html
│
├── .build.sh                   # Script de build
├── .env                        # Variáveis de ambiente (local)
├── .gitignore
├── Exemplos.docx               # Arquivo de exemplo
├── gunicorn_config.py          # Configuração do Gunicorn
├── Installer.py                # Script de instalação
├── procfile                    # Configuração de processo
├── render.yaml                 # Deploy automático no Render
├── requirements.txt            # Dependências Python
├── run_app.bat                 # Execução no Windows
├── run.py                      # Script de inicialização
└── README.md                   # Documentação

⚙️ Configuração
🔑 Token do Hugging Face (Opcional)

Para melhorar a análise com IA:

Crie uma conta em https://huggingface.co

Vá em Settings → Access Tokens → New Token

Copie o token (começa com hf_)

Adicione como variável de ambiente:

HF_TOKEN=seu_token_aqui


No Render, configure em Environment Variables.

🚀 Deploy no Render

O projeto já inclui o arquivo render.yaml:

services:
  - type: web
    name: email-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server.app:app

🔌 API REST
Endpoint

POST /analyze

https://email-analyzer-dx4v.onrender.com/analyze

Parâmetros

content: texto do email

file: arquivo PDF ou TXT (opcional)

Resposta
{
  "utilidade": 0.92,
  "categoria": "CURRICULO",
  "resumo": "Currículo profissional...",
  "tags": ["python", "django"],
  "resposta": "✅ Currículo recebido com sucesso!"
}

🐛 Solução de Problemas
⏱️ Aplicação lenta no primeiro acesso

Render Free Tier possui cold start

Aguarde 30–60 segundos na primeira requisição

🔴 Erro "Service Unavailable"

Recarregue após alguns segundos

Status: https://status.render.com

📄 PDF não processa

Tamanho máximo: 10MB

Formatos aceitos: PDF, TXT

PDFs precisam conter texto (não apenas imagens)

📊 Status do Projeto
Componente	Status	Detalhes
Aplicação Web	✅ Online	Render
API REST	✅ Funcionando	/analyze
Processamento PDF	✅ Ativo	Extração automática
Infraestrutura	🟡 Free Tier	Limitações
🤝 Contribuindo
git checkout -b minha-feature
git commit -m "Minha feature"
git push origin minha-feature


Abra um Pull Request 🚀

📄 Licença

Licença MIT — veja o arquivo LICENSE.

👨‍💻 Autor

Whandger Wolffenbüttel

GitHub: https://github.com/Whandger

LinkedIn: whandger

⭐ Gostou do projeto?
Dê uma estrela no GitHub!
