# 📧 Email AI Classifier

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![Deploy on Render](https://img.shields.io/badge/Render-Deploy-blueviolet)](https://render.com)

**Classificador inteligente de emails** que usa IA para analisar emails e documentos PDF, categorizando automaticamente e sugerindo respostas.
Deploy https://email-analyzer-dx4v.onrender.com/

![Screenshot](https://img.shields.io/badge/Live-Demo-brightgreen)

## ✨ Funcionalidades

- ✅ **Análise automática de emails** (texto e PDF)
- 🤖 **Classificação por IA** em 8 categorias:
  - 📄 **CURRICULO** - Currículos e candidaturas
  - 💰 **FINANCEIRO** - Faturas, boletos, documentos
  - 🚨 **IMPORTANTE** - Emails urgentes
  - 🎓 **EDUCACIONAL** - Comunicação acadêmica
  - 💼 **PROFISSIONAL** - Emails corporativos
  - 📭 **SPAM** - Promoções e marketing
  - ⚠️ **PHISHING** - Emails suspeitos
  - 📧 **ROTINA** - Emails normais
- 📊 **Score de utilidade** (0-100%)
- 🏷️ **Tags automáticas** baseadas no conteúdo
- 📝 **Resumo inteligente** do conteúdo
- 💬 **Sugestão de resposta** automática
- 🌐 **Deploy pronto** para Render

## 🚀 Deploy Rápido no Render

### Método 1: Deploy Automático (Recomendado)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Whandger/Email-analyzer)

1. Clique no botão acima
2. Configure o nome do serviço
3. Adicione a variável `HF_TOKEN` (opcional):
   - Vá em Dashboard → Seu Serviço → Environment
   - Adicione: `HF_TOKEN = seu_token_huggingface`
4. Clique em **Apply** e depois **Deploy**

### Método 2: Deploy Manual

1. **Crie conta no Render** (render.com)
2. **Crie novo Web Service**
3. **Conecte seu repositório GitHub**
4. **Configure:**
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT server.app:app

text
5. **Adicione variáveis de ambiente:**
- `HF_TOKEN`: (opcional) Token do Hugging Face
- `PYTHONUNBUFFERED`: `true`
6. **Clique em Deploy**

## 🛠️ Instalação Local

### Pré-requisitos
- Python 3.10+
- pip (gerenciador de pacotes)
- Git (opcional)

### Passo a Passo

1. **Clone o repositório:**
```bash
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer
Instale dependências:

bash
# Usando o instalador automático:
python install_render.py

# Ou manualmente:
pip install -r requirements.txt
Configure (opcional):
Edite server/config/config.py para adicionar seu token:

python
HF_TOKEN = "hf_seu_token_aqui"  # Token do Hugging Face (opcional)
Execute a aplicação:

bash
# Modo desenvolvimento:
python server/app.py

# Modo produção:
gunicorn --bind 0.0.0.0:5000 server.app:app
Acesse no navegador:

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
├── install_render.py       # Instalador automático
└── README.md               # Este arquivo
🔧 Configuração da IA
Com Token do Hugging Face (Recomendado)
Crie conta em huggingface.co

Vá em Settings → Access Tokens → New Token

Copie o token (começa com hf_)

Adicione em server/config/config.py ou variável de ambiente

Sem Token (Modo Local)
Usa análise por keywords

Funciona para categorização básica

Não requer configuração adicional

📊 Como Usar
Acesse a aplicação (localhost:5000 ou seu deploy)

Digite um texto ou envie um arquivo PDF

Clique em "Analisar Email"

Veja os resultados:

📊 Score de utilidade

🏷️ Categoria automática

📝 Resumo do conteúdo

💬 Sugestão de resposta

🔖 Tags relevantes

Exemplo de Análise
Entrada:

text
Olá, envio meu currículo para a vaga de desenvolvedor Python.
Experiência com Django, Flask, AWS.
Portfólio: github.com/usuario
Saída:

📊 Utilidade: 92%

🏷️ Categoria: CURRICULO

📝 Resumo: Currículo profissional para vaga de desenvolvedor Python...

💬 Resposta: ✅ Currículo recebido com sucesso!

🔖 Tags: python, django, github

🐛 Troubleshooting
Problemas Comuns
Erro no deploy do Render:

bash
# Verifique os logs:
Render Dashboard → Seu Serviço → Logs

# Solução comum:
- Verifique requirements.txt
- Confirme variáveis de ambiente
- Use Python 3.10+ (runtime.txt)
Erro "Module not found":

bash
pip install -r requirements.txt
python -m pip install --upgrade pip
PDF não processa:

Verifique se é PDF válido

Tamanho máximo: 10MB

Use PDFs com texto (não apenas imagens)

IA não funciona:

Sem token: usa modo local

Com token: verifique se é válido

Teste em: https://huggingface.co/settings/tokens

Logs Importantes
bash
# No Render:
Render Dashboard → Seu Serviço → Logs

# Localmente:
python server/app.py  # Mostra logs no terminal
🔍 API Endpoints
POST /analyze
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
📈 Roadmap
Suporte a mais formatos (DOCX, XLSX)

Dashboard com estatísticas

Exportação de relatórios

Integração com Gmail/Outlook

Modelos de IA customizados

API REST completa

Sistema de plugins

🤝 Contribuindo
Fork o projeto

Crie uma branch (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Add nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request

Código de Conduta
Respeite todos os contribuidores

Mantenha o foco técnico

Use inglês para issues e PRs

📄 Licença
MIT License - veja LICENSE para detalhes.

👨‍💻 Autor
Whandger Wolffenbüttel

GitHub: @Whandger

LinkedIn: whandger

Email: whandger@gmail.com

🙏 Agradecimentos
Hugging Face por modelos de IA

Render por hospedagem gratuita

Comunidade open-source pelas bibliotecas

⭐ Gostou do projeto? Dê uma estrela no GitHub! ⭐

https://img.shields.io/github/stars/Whandger/Email-analyzer?style=social
https://img.shields.io/github/forks/Whandger/Email-analyzer?style=social

text

## 📋 Checklist de Deploy

### Antes do Deploy:
- [ ] `requirements.txt` atualizado
- [ ] `runtime.txt` com Python 3.10+
- [ ] `render.yaml` configurado
- [ ] Testado localmente
- [ ] HF_TOKEN configurado (opcional)

### Após o Deploy:
- [ ] Acessar URL do Render
- [ ] Testar upload de PDF
- [ ] Testar análise de texto
- [ ] Verificar logs no dashboard

### Se Der Erro:
1. ✅ Verificar `requirements.txt`
2. ✅ Conferir `runtime.txt` (3.10.12)
3. ✅ Checar variáveis de ambiente
4. ✅ Examinar logs do Render

O projeto está pronto para deploy no Render! 🚀
