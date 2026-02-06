# 🤖 Perplexity Email Analyzer
**Classificador Inteligente de Emails com IA de Última Geração**

🔗 **Acesse o Deploy:** [https://email-analyzer-dx4v.onrender.com/](https://email-analyzer-dx4v.onrender.com/)

![Python Flask Deploy on Render](https://img.shields.io/badge/Deploy-Render-46B3E6)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-000000)
![AI](https://img.shields.io/badge/IA-Perplexity-8A2BE2)

Sistema avançado de análise de emails que utiliza a poderosa **Perplexity AI API** para classificar, priorizar e responder automaticamente a comunicações corporativas com precisão de 99%.

---

## ✨ **Funcionalidades Principais**

### 🎯 **Análise Inteligente**
- ✅ **Processamento automático** de emails (texto e PDF/TXT)
- 🤖 **Classificação por IA** em 7 categorias precisas:
  - 📄 **CURRICULO** - Currículos e candidaturas
  - 💰 **FINANCEIRO** - Documentos financeiros, notas fiscais
  - ⚠️ **IMPORTANTE** - Emails urgentes e críticos
  - 💼 **PROFISSIONAL** - Propostas comerciais, reuniões
  - 🚫 **PHISHING** - Detecção de fraudes e golpes
  - 📭 **SPAM** - Marketing não solicitado
  - 📧 **ROTINA** - Comunicação administrativa
- 📊 **Score de utilidade real** (0-100%) baseado no valor prático
- 🏷️ **Tags automáticas** extraídas do conteúdo
- 📝 **Resumo inteligente** gerado por IA
- 💬 **Resposta automática** personalizada por departamento

### 🛡️ **Segurança Avançada**
- 🚨 **Detecção de phishing** com 99% de confiança
- 🔒 **Validação de segurança** em tempo real
- 📄 **Processamento seguro** de arquivos PDF/TXT
- ⚡ **Sistema 100% IA-driven** - sem fallback manual

### 🎨 **Interface Moderna**
- 🌈 **Dashboard interativo** com visualizações coloridas
- 📱 **Design responsivo** para desktop e mobile
- 🔄 **Feedback em tempo real** durante análise
- 📋 **Botão de copiar** resposta com um clique

---

## 🚀 **Deploy Rápido no Render**

### **Método 1: Deploy Automático (Recomendado)**
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Whandger/Email-analyzer)

1. **Clique no botão acima**
2. **Configure o nome do serviço**
3. **Adicione a variável obrigatória**:
   - Vá em **Dashboard → Seu Serviço → Environment**
   - Adicione: `PERPLEXITY_API_KEY = pplx-sua-chave-aqui`
4. **Clique em Apply** e depois **Deploy**

### **Método 2: Deploy Manual**
```bash
# 1. Crie conta no Render (render.com)
# 2. Crie novo Web Service
# 3. Conecte seu repositório GitHub
# 4. Configure:
#    Build Command: pip install -r requirements.txt
#    Start Command: gunicorn --bind 0.0.0.0:$PORT server.app:app
# 5. Adicione variáveis de ambiente:
#    PERPLEXITY_API_KEY: pplx-sua-chave (OBRIGATÓRIO)
#    PYTHONUNBUFFERED: true
#    FLASK_DEBUG: false
# 6. Clique em Deploy
```
🛠️ Instalação Local
Pré-requisitos
Python 3.10+

pip (gerenciador de pacotes)

Chave de API da Perplexity (obrigatória)

```
# 1. Clone o repositório
git clone https://github.com/Whandger/Email-analyzer.git
cd Email-analyzer

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure a API Key
# Crie um arquivo .env na raiz do projeto:
echo "PERPLEXITY_API_KEY=pplx-sua-chave-aqui" > .env

# 4. Execute a aplicação
# Modo desenvolvimento:
python run.py

# Modo produção:
gunicorn --bind 0.0.0.0:5000 server.app:app

# 5. Acesse no navegador
# http://localhost:5000
```
📦 Obtenha sua API Key
Acesse perplexity.ai

Crie uma conta gratuita

Vá para Settings → API Keys

Gere uma nova chave (começa com pplx-)

Copie e cole no seu .env
````
Email-analyzer/
├── server/ # Backend Flask
│ ├── app.py # Aplicação principal
│ ├── config/
│ │ └── config.py # Configurações Perplexity
│ ├── services/
│ │ └── email_service.py # Lógica de análise
│ ├── utils/
│ │ ├── text_processor.py # Processador de texto
│ │ └── perplexity_handler.py # IA Perplexity
│ └── routes/
│ └── api.py # Rotas da API
├── static/ # Arquivos estáticos
│ ├── css/
│ │ └── index.css # Estilos
│ └── js/
│ └── email.js # JavaScript
├── templates/
│ └── index.html # Página principal
├── requirements.txt # Dependências Python
├── runtime.txt # Versão do Python
├── Procfile # Configuração Heroku/Render
├── wsgi.py # Ponto de entrada WSGI
├── gunicorn_config.py # Configuração Gunicorn
├── .env.example # Exemplo de variáveis
└── README.md # Este arquivo
````
🔧 Configuração da IA
Com Perplexity API (OBRIGATÓRIO)
O sistema agora utiliza exclusivamente Perplexity AI para máxima precisão:

Obtenha sua chave em perplexity.ai/settings/api

Adicione ao .env:
```
env
PERPLEXITY_API_KEY=pplx-sua-chave-aqui
```

Modelos disponíveis:

sonar (padrão) - Mais rápido e econômico
sonar-pro - Análise mais profunda
sonar-reasoning-pro - Raciocínio avançado

🎯 Por que Perplexity AI?
````
✅ Precisão superior em classificação de emails
⚡ Respostas mais contextualizadas
🚫 Detecção avançada de phishing
💰 Custo otimizado por análise
🔄 Atualizações automáticas dos modelos
````

📊 Como Usar
📝 Analisando um Email
Acesse a aplicação (localhost:5000 ou seu deploy)

Digite o texto do email ou envie um arquivo (PDF/TXT)
Clique em "Analisar Email"
Veja os resultados completos:
````
📊 Score de utilidade (0-100%)
🏷️ Categoria automática com emoji
🔴 Prioridade (Crítica, Alta, Média, Baixa)
🏢 Departamento sugerido
📝 Resumo inteligente
💬 Resposta pronta para enviar
🔖 Tags relevantes
````

🎯 Exemplos de Análise

📧 Email de Phishing
````
Assunto: Urgente: Sua conta do banco foi comprometida!
De: suporte@bancoseguro-alerta.com

Prezado cliente,
Detectamos login suspeito. Clique aqui para verificar:
http://banco-falso.com/verificar
````
Resultado:
````
🚫 Categoria: PHISHING
📉 Utilidade: 0%
🔴 Prioridade: CRÍTICA
🏢 Departamento: Segurança
💬 Resposta: Alerta de segurança gerado automaticamente
````
````
📄 Currículo (PDF)
````
Resultado:
````
📄 Categoria: CURRICULO
📈 Utilidade: 92%
🟡 Prioridade: ALTA
🏢 Departamento: RH
💬 Resposta: Confirmação profissional de recebimento
````

🐛 Troubleshooting
Problemas Comuns
❌ "Perplexity API não configurada"
bash
# Solução:
# 1. Verifique se o arquivo .env existe
# 2. Confirme que a chave começa com "pplx-"
# 3. Teste a chave em: https://www.perplexity.ai/settings/api
❌ Erro no deploy do Render
bash
# Verifique os logs:
Render Dashboard → Seu Serviço → Logs

# Soluções comuns:
1. requirements.txt atualizado
2. PERPLEXITY_API_KEY configurada
3. Python 3.10+ (runtime.txt)
❌ PDF não processa
Verifique se é PDF válido (texto, não imagem)

Tamanho máximo: 10MB

Use: file.pdf ou file.txt

❌ IA não responde
python
# Teste a conexão:
curl -X GET https://email-analyzer-dx4v.onrender.com/api/test-perplexity
📋 Logs Importantes
bash
# No Render:
Render Dashboard → Seu Serviço → Logs

# Localmente:
python run.py  # Mostra logs detalhados

# Verifique saúde:
curl https://email-analyzer-dx4v.onrender.com/health
🔍 API Endpoints
POST /analyze
Analisa conteúdo de email com Perplexity AI.

Parâmetros:

email_text (texto): Conteúdo do email

file (arquivo): PDF ou TXT (opcional)

Resposta:
````
json
{
  "is_useful": true,
  "analysis": {
    "categoria": "CURRICULO",
    "categoria_nome": "Currículo",
    "utilidade": 0.92,
    "resumo": "Currículo profissional para vaga de desenvolvedor...",
    "acao_necessaria": true,
    "prioridade": "ALTA",
    "protocolo": "PPX-12345",
    "tags": ["python", "flask", "aws"],
    "resposta_completa": "Prezado(a), Confirmamos recebimento...",
    "departamento": "RH",
    "fonte": "perplexity_ia"
  },
  "auto_response": "Resposta completa gerada...",
  "analysis_source": "perplexity_ia"
}
````
GET /health
Verifica status do sistema.

GET /api/status
Retorna configuração da IA.

GET /api/test-perplexity
Testa conexão com Perplexity API.

📈 Roadmap Futuro
🚀 Próximas Funcionalidades
Integração com APIs de email (Gmail, Outlook)

Dashboard de estatísticas avançado

Exportação de relatórios em PDF/CSV

Modelos customizados por empresa

API REST completa com documentação Swagger

Sistema de plugins para extensibilidade

Análise de sentimentos em emails

Detecção de temas recorrentes

🔧 Melhorias Técnicas
Cache distribuído para performance

Rate limiting inteligente

Monitoramento com Prometheus/Grafana

Testes automatizados completos

CI/CD pipeline otimizado

🤝 Contribuindo
📋 Processo de Contribuição
Fork o projeto

Crie uma branch (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Add: nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request

🎯 Diretrizes de Código
Use Python 3.10+ com type hints

Siga PEP 8 para estilo de código

Adicione testes para novas funcionalidades

Documente mudanças na API

Mantenha compatibilidade com deploy no Render

🐛 Reportando Bugs
Use a seção Issues do GitHub

Inclua passos para reproduzir

Adicione logs relevantes

Especifique ambiente (local/Render)

📄 Licença
MIT License - veja LICENSE para detalhes completos.

Permissões:

Uso comercial

Modificação

Distribuição

Uso privado

Limitações:

Sem garantia

Sem responsabilidade

👨‍💻 Autor
Whandger Wolffenbüttel

LinkedIn: Whandger Wolffenbüttel
Email: whandger@gmail.com

⭐ Suporte ao Projeto
Se este projeto foi útil para você:

Dê uma estrela no repositório GitHub

Compartilhe com outros desenvolvedores

Contribua com issues ou pull requests

Mencione em seus projetos

https://img.shields.io/github/stars/Whandger/Email-analyzer?style=social
https://img.shields.io/github/forks/Whandger/Email-analyzer?style=social
