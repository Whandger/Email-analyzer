📧 Email AI Classifier
Aplicação online: https://email-analyzer-dx4v.onrender.com
Repositório: https://github.com/Whandger/Email-analyzer

Classificador inteligente de emails que usa IA para analisar emails e documentos PDF, categorizando automaticamente e sugerindo respostas.

✨ Funcionalidades
Análise automática de emails (texto e PDF)

Classificação por IA em 8 categorias

Score de utilidade (0-100%)

Tags automáticas baseadas no conteúdo

Resumo inteligente do conteúdo

Sugestão de resposta automática

Deploy em produção no Render

🚀 Como Usar
🟢 Online (Recomendado)
Acesse https://email-analyzer-dx4v.onrender.com

Cole um texto ou envie um arquivo PDF/TXT

Clique em "Analisar Email"

Veja os resultados em tempo real

💻 Localmente
bash
# Clone o repositório
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer

# Instale dependências
pip install -r requirements.txt

# Execute a aplicação
python server/app.py

# Acesse: http://localhost:5000
📁 Estrutura do Projeto
text
Email-analyzer/
├── server/                    # Backend Flask
│   ├── app.py                # Aplicação principal
│   ├── config/               # Configurações
│   ├── utils/                # Utilitários
│   └── routes/               # Rotas da API
├── static/                   # Arquivos estáticos
│   ├── css/                  # Estilos
│   └── js/                   # JavaScript
├── templates/                # Templates HTML
│   └── index.html            # Página principal
├── requirements.txt          # Dependências Python
├── runtime.txt              # Python 3.10.12
├── render.yaml              # Configuração Render
└── README.md                # Documentação
⚙️ Configuração
🔑 Token do Hugging Face (Opcional)
Para melhorar a análise com IA:

Crie conta em huggingface.co

Vá em Settings → Access Tokens → New Token

Copie o token (começa com hf_)

Adicione como variável de ambiente HF_TOKEN no Render

🚀 Configuração Render
O projeto inclui render.yaml para deploy automático:

yaml
services:
  - type: web
    name: email-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server.app:app
🔌 API
Endpoint: POST /analyze
URL: https://email-analyzer-dx4v.onrender.com/analyze

Parâmetros:

content: texto do email

file: arquivo PDF/TXT (opcional)

Resposta:

json
{
  "utilidade": 0.92,
  "categoria": "CURRICULO",
  "resumo": "Currículo profissional...",
  "tags": ["python", "django"],
  "resposta": "✅ Currículo recebido com sucesso!"
}
🐛 Solução de Problemas
⏱️ Aplicação lenta no primeiro acesso
Render Free Tier tem "cold starts"

Aguarde 30-60 segundos na primeira requisição

Funciona normalmente após inicialização

🔴 Erro "Service Unavailable"
Recarregue a página após 60 segundos

Render Free Tier tem limites de uso

Verifique status em status.render.com

📄 PDF não processa
Tamanho máximo: 10MB

Formatos aceitos: PDF, TXT

Atenção: PDFs devem conter texto (não apenas imagens)

📊 Status do Projeto
Componente	Status	Detalhes
Aplicação Web	✅ Online	https://email-analyzer-dx4v.onrender.com
API REST	✅ Funcionando	Endpoint /analyze ativo
Processamento PDF	✅ Ativo	Extração de texto automática
Infraestrutura	🟡 Render Free Tier	Limitações de performance
🤝 Contribuindo
Fork o projeto

Crie uma branch: git checkout -b minha-feature

Commit: git commit -m 'Minha feature'

Push: git push origin minha-feature

Abra um Pull Request

📄 Licença
MIT License - veja LICENSE para detalhes.

👨‍💻 Autor
Whandger Wolffenbüttel

GitHub: @Whandger

LinkedIn: whandger

Links do projeto:

🌐 Aplicação Online: https://email-analyzer-dx4v.onrender.com

📦 Repositório: https://github.com/Whandger/Email-analyzer

🐛 Reportar Bugs: GitHub Issues

⭐ Gostou do projeto? Dê uma estrela no GitHub!

https://img.shields.io/github/stars/Whandger/Email-analyzer?style=for-the-badge
https://img.shields.io/badge/Acessar_Aplica%C3%A7%C3%A3o-Click_Here-brightgreen?style=for-the-badge
