# 📧 Email AI Classifier

![GitHub stars](https://img.shields.io/github/stars/Whandger/Email-analyzer?style=for-the-badge)
[![Aplicação Online](https://img.shields.io/badge/Acessar_Aplicação-Click_Here-brightgreen?style=for-the-badge)](https://email-analyzer-dx4v.onrender.com)

🔗 **Aplicação Online:** https://email-analyzer-dx4v.onrender.com  
📦 **Repositório:** https://github.com/Whandger/Email-analyzer  

---

## 🧠 Sobre o Projeto

O **Email AI Classifier** é uma aplicação web que utiliza **Inteligência Artificial** para analisar emails e documentos (PDF/TXT), classificando automaticamente o conteúdo, gerando resumos, tags, score de utilidade e sugerindo respostas automáticas.

Ideal para automação de triagem de emails, RH, atendimento ao cliente e organização de mensagens.

---

## ✨ Funcionalidades

- 📩 **Análise automática de emails** (texto e PDF/TXT)
- 🤖 **Classificação por IA** em 8 categorias
- 📊 **Score de utilidade** (0 a 100%)
- 🏷️ **Geração automática de tags**
- 📝 **Resumo inteligente** do conteúdo
- 💬 **Sugestão de resposta automática**
- 🚀 **Deploy em produção** no Render

---

## 🚀 Como Usar

### 🟢 Online (Recomendado)

1. **Acesse:** https://email-analyzer-dx4v.onrender.com
2. **Cole um texto** ou envie um arquivo **PDF/TXT**
3. **Clique** em **"Analisar Email"**
4. **Veja os resultados** em tempo real

### 💻 Executando Localmente

```bash
# Clone o repositório
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python server/app.py

# Acesse no navegador: http://localhost:5000
📁 Estrutura do Projeto
text
autoU_ia/
├── server/
│   ├── config/
│   │   └── config.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   └── email_service.py
│   ├── utils/
│   │   ├── file_handler.py
│   │   ├── hugg_handler.py
│   │   ├── keywords.py
│   │   └── text_processor.py
│   └── app.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   └── index.html
├── .build.sh
├── .env
├── .gitignore
├── Exemplos.docx
├── gunicorn_config.py
├── Installer.py
├── procfile
├── render.yaml
├── requirements.txt
├── run_app.bat
├── run.py
└── README.md
⚙️ Configuração
🔑 Token do Hugging Face (Opcional)
Para melhorar a análise com IA:

Crie uma conta em https://huggingface.co

Vá em Settings → Access Tokens → New Token

Copie o token (começa com hf_)

Adicione como variável de ambiente:

bash
HF_TOKEN=seu_token_aqui
No Render, configure em Environment Variables.

🚀 Deploy no Render
O projeto já inclui o arquivo render.yaml:

yaml
services:
  - type: web
    name: email-analyzer
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT server.app:app
🔌 API REST
Endpoint
POST /analyze

text
https://email-analyzer-dx4v.onrender.com/analyze
Parâmetros
content: texto do email

file: arquivo PDF ou TXT (opcional)

Resposta
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
Render Free Tier possui cold start

Aguarde 30–60 segundos na primeira requisição

🔴 Erro "Service Unavailable"
Recarregue após alguns segundos

Status do Render: https://status.render.com

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
bash
git checkout -b minha-feature
git commit -m "Minha feature"
git push origin minha-feature
Abra um Pull Request.

📄 Licença
Este projeto está sob a licença MIT.
Veja o arquivo LICENSE para mais detalhes.

👨‍💻 Autor
Whandger Wolffenbüttel
GitHub: https://github.com/Whandger
LinkedIn: https://linkedin.com/in/whandger

⭐ Gostou do projeto?
Dê uma estrela no GitHub e ajude o projeto a crescer!
