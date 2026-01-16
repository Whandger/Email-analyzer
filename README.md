📧 Email AI Classifier
Aplicação online: https://email-analyzer-dx4v.onrender.com

Repositório: https://github.com/Whandger/Email-analyzer

Classificador inteligente de emails que usa IA para analisar emails e documentos PDF, categorizando automaticamente e sugerindo respostas.

✨ Funcionalidades
Análise automática de emails (texto e PDF)

Classificação por IA em 8 categorias: CURRICULO, FINANCEIRO, IMPORTANTE, EDUCACIONAL, PROFISSIONAL, SPAM, PHISHING, ROTINA

Score de utilidade (0-100%)

Tags automáticas baseadas no conteúdo

Resumo inteligente do conteúdo

Sugestão de resposta automática

Deploy em produção no Render

🚀 Como Usar
Online (Recomendado)
Acesse https://email-analyzer-dx4v.onrender.com e:

Cole um texto na área de texto

Ou envie um arquivo PDF/TXT

Clique em "Analisar Email"

Veja os resultados em tempo real

Localmente
bash
# Clone o repositório
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer

# Instale dependências
pip install -r requirements.txt

# Execute
python server/app.py

# Acesse: http://localhost:5000
📁 Estrutura do Projeto
text
Email-analyzer/
├── server/              # Backend Flask
├── static/             # CSS/JS
├── templates/          # HTML
├── requirements.txt    # Dependências
├── runtime.txt        # Python 3.10.12
├── render.yaml        # Configuração Render
└── README.md
🔧 Configuração
Token do Hugging Face (Opcional)
Para melhorar a análise com IA:

Crie conta em huggingface.co

Gere um token em Settings → Access Tokens

Adicione como variável HF_TOKEN no Render

Render Configuration
O projeto está configurado para deploy automático no Render. A configuração principal está em render.yaml:

yaml
services:
  - type: web
    name: email-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server.app:app
🔍 API
Endpoint: POST /analyze
URL: https://email-analyzer-dx4v.onrender.com/analyze

Parâmetros:

content: texto do email

file: arquivo PDF/TXT (opcional)

Resposta JSON:

json
{
  "utilidade": 0.92,
  "categoria": "CURRICULO",
  "resumo": "Currículo profissional...",
  "tags": ["python", "django"],
  "resposta": "✅ Currículo recebido com sucesso!"
}
🐛 Solução de Problemas
Aplicação lenta no primeiro acesso
Render Free Tier tem "cold starts". Aguarde 30-60 segundos na primeira requisição.

Erro "Service Unavailable"
Recarregue a página após 60 segundos

Free Tier tem limites de uso (512MB RAM, 100GB/mês)

Verifique status: status.render.com

PDF não processa
Tamanho máximo: 10MB

Formatos: PDF ou TXT

PDFs devem conter texto (não apenas imagens)

📈 Status e Monitoramento
Aplicação: ✅ Online em https://email-analyzer-dx4v.onrender.com
API: ✅ Funcionando
PDF Processing: ✅ Ativo
Limitações: Render Free Tier (pode ter cold starts)

Para verificar logs e métricas:

Acesse Render Dashboard

Selecione o serviço "email-analyzer"

Navegue para "Logs" ou "Metrics"

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
Projeto Online: https://email-analyzer-dx4v.onrender.com

⭐ Gostou? Dê uma estrela no repositório!
GitHub Repo | Aplicação Online
