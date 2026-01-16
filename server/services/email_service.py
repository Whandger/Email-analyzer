# server/services/email_service.py - VERSÃO SIMPLIFICADA FUNCIONAL
DEMO_MODE = False  # MODO PRODUÇÃO

import os
import tempfile
import re
import random
import time
from datetime import datetime

from server.utils.file_handler import FileHandler
from server.utils.hugg_handler import HuggingFaceHandler
from server.config.config import Config

# Inicializar handlers
file_handler = FileHandler()
hf_handler = HuggingFaceHandler()

# ======================================================
# CONSTANTES ATUALIZADAS COM EDUCACIONAL
# ======================================================

CATEGORIAS = {
    "PHISHING": {"nome": "Phishing", "emoji": "🚫", "prioridade": "CRÍTICA", "departamento": "Segurança"},
    "CURRICULO": {"nome": "Currículo", "emoji": "📄", "prioridade": "ALTA", "departamento": "RH"},
    "FINANCEIRO": {"nome": "Financeiro", "emoji": "💰", "prioridade": "ALTA", "departamento": "Financeiro"},
    "IMPORTANTE": {"nome": "Importante", "emoji": "⭐", "prioridade": "ALTA", "departamento": "Diretoria"},
    "EDUCACIONAL": {"nome": "Educacional", "emoji": "🎓", "prioridade": "ALTA", "departamento": "Educação"},
    "PROFISSIONAL": {"nome": "Profissional", "emoji": "💼", "prioridade": "MÉDIA", "departamento": "Comercial"},
    "SPAM": {"nome": "Spam", "emoji": "📢", "prioridade": "BAIXA", "departamento": "Filtragem"},
    "ROTINA": {"nome": "Rotina", "emoji": "📋", "prioridade": "BAIXA", "departamento": "Atendimento"}
}

# ======================================================
# FUNÇÕES UTILITÁRIAS
# ======================================================

def allowed_file(filename):
    return filename and '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'txt'}

def extrair_informacoes_email(conteudo):
    info = {"nome": None, "email": None, "telefone": None, "empresa": None}
    
    # Nome
    padroes_nome = [
        r'[Mm]e chamo\s+([A-Za-zÀ-ÿ\s]+)[\.\n,]',
        r'[Mm]eu nome é\s+([A-Za-zÀ-ÿ\s]+)[\.\n,]',
        r'Atenciosamente,\s*([A-Za-zÀ-ÿ\s]+)'
    ]
    
    for padrao in padroes_nome:
        match = re.search(padrao, conteudo, re.IGNORECASE)
        if match:
            nome = match.group(1).strip()
            if len(nome.split()) > 0:
                info["nome"] = nome.title()
                break
    
    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', conteudo)
    if email_match:
        info["email"] = email_match.group(0).lower()
    
    # Telefone
    telefone_match = re.search(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', conteudo)
    if telefone_match:
        info["telefone"] = telefone_match.group(0)
    
    return info

def detectar_phishing(conteudo, assunto=""):
    conteudo_lower = conteudo.lower()
    
    # Padrões de phishing
    padroes = [
        (r'google.*update\.com', 100),
        (r'48.*horas.*(acesse|clique)', 90),
        (r'conta.*será.*suspensa', 85),
    ]
    
    phishing_score = 0
    for padrao, score in padroes:
        if re.search(padrao, conteudo_lower, re.IGNORECASE):
            phishing_score += score
    
    dominios_falsos = ['google-workspace-security-update.com']
    for dominio in dominios_falsos:
        if dominio in conteudo_lower:
            phishing_score += 100
            break
    
    return phishing_score >= 80, phishing_score

# ======================================================
# ANÁLISE COM IA REAL
# ======================================================

def analise_ia_real(conteudo_email, conteudo_anexo="", remetente="", assunto=""):
    """Usa Hugging Face REAL"""
    print("🤖 IA REAL: Analisando...")
    
    # Verificar phishing
    is_phishing, phishing_score = detectar_phishing(conteudo_email, assunto)
    
    if is_phishing:
        print(f"🚨 PHISHING DETECTADO")
        categoria = "PHISHING"
        confianca = 0.95
        resumo = f"Phishing detectado (score: {phishing_score})"
    else:
        # Usar Hugging Face Handler
        conteudo_completo = conteudo_email + " " + conteudo_anexo
        analysis = hf_handler.analyze_email(conteudo_email, conteudo_anexo)
        
        categoria = analysis['categoria']
        confianca = analysis['utilidade']
        resumo = analysis['resumo']
    
    # Protocolo
    protocolo = f"HF-{random.randint(10000, 99999)}"
    
    # Info remetente
    conteudo_completo = conteudo_email + " " + conteudo_anexo
    info_remetente = extrair_informacoes_email(conteudo_completo)
    
    # Gerar resposta (usar do handler ou padrão)
    if is_phishing or 'resposta' not in analysis:
        resposta = gerar_resposta_padrao(categoria, protocolo, info_remetente)
    else:
        resposta = analysis['resposta']
    
    return {
        "categoria": categoria,
        "categoria_nome": CATEGORIAS[categoria]["nome"],
        "categoria_emoji": CATEGORIAS[categoria]["emoji"],
        "utilidade": round(confianca, 2),
        "confianca_ia": round(confianca, 3),
        "resumo": resumo,
        "acao_necessaria": categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "PHISHING", "EDUCACIONAL"],
        "prioridade": CATEGORIAS[categoria]["prioridade"],
        "protocolo": protocolo,
        "tags": ['ia_real', categoria.lower()],
        "resposta_completa": resposta,
        "departamento": CATEGORIAS[categoria]["departamento"],
        "info_remetente": info_remetente,
        "fonte": "huggingface_ia"
    }

def analise_ia_demo(conteudo_email, conteudo_anexo="", remetente="", assunto=""):
    """Análise simulada"""
    print("🧠 IA DEMO: Analisando...")
    time.sleep(0.5)
    
    # Simulação simples
    conteudo_lower = (conteudo_email + " " + conteudo_anexo).lower()
    
    if any(word in conteudo_lower for word in ['currículo', 'cv', 'candidatura', 'vaga']):
        categoria = "CURRICULO"
        confianca = 0.85
    elif any(word in conteudo_lower for word in ['matricula', 'matrícula', 'curso', 'universidade']):
        categoria = "EDUCACIONAL"
        confianca = 0.80
    elif any(word in conteudo_lower for word in ['nota fiscal', 'boleto', 'pagamento']):
        categoria = "FINANCEIRO"
        confianca = 0.80
    elif any(word in conteudo_lower for word in ['urgente', 'importante', 'contrato']):
        categoria = "IMPORTANTE"
        confianca = 0.75
    elif any(word in conteudo_lower for word in ['proposta', 'orçamento', 'serviço']):
        categoria = "PROFISSIONAL"
        confianca = 0.65
    else:
        categoria = "ROTINA"
        confianca = 0.50
    
    # Protocolo
    protocolo = f"DEMO-{random.randint(10000, 99999)}"
    
    # Info remetente
    conteudo_completo = conteudo_email + " " + conteudo_anexo
    info_remetente = extrair_informacoes_email(conteudo_completo)
    
    # Resposta
    resposta = gerar_resposta_padrao(categoria, protocolo, info_remetente)
    
    return {
        "categoria": categoria,
        "categoria_nome": CATEGORIAS[categoria]["nome"],
        "categoria_emoji": CATEGORIAS[categoria]["emoji"],
        "utilidade": confianca,
        "confianca_ia": confianca,
        "resumo": f"Classificado como {categoria}",
        "acao_necessaria": categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "EDUCACIONAL"],
        "prioridade": CATEGORIAS[categoria]["prioridade"],
        "protocolo": protocolo,
        "tags": ['demo', categoria.lower()],
        "resposta_completa": resposta,
        "departamento": CATEGORIAS[categoria]["departamento"],
        "info_remetente": info_remetente,
        "fonte": "ia_simulada"
    }

def gerar_resposta_padrao(categoria, protocolo, info_remetente):
    """Gera resposta padrão"""
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    nome = info_remetente.get("nome", "")
    saudacao = f"Prezado(a) {nome}," if nome else "Prezado(a),"
    
    respostas = {
        "CURRICULO": f"{saudacao}\n\nConfirmamos recebimento do seu currículo.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nAtenciosamente,\nRH",
        "EDUCACIONAL": f"{saudacao}\n\nConfirmamos recebimento da sua comunicação educacional.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nAtenciosamente,\nSecretaria Acadêmica",
        "FINANCEIRO": f"{saudacao}\n\nConfirmamos recebimento do documento.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nAtenciosamente,\nFinanceiro",
        "PHISHING": f"{saudacao}\n\n🚨 ALERTA: Possível phishing detectado.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nNão clique em links suspeitos.\n\nAtenciosamente,\nSegurança",
        "IMPORTANTE": f"{saudacao}\n\nRecebemos sua mensagem importante.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nAtenciosamente,\nDiretoria",
        "DEFAULT": f"{saudacao}\n\nConfirmamos recebimento.\n\nProtocolo: {protocolo}\nData: {data_atual}\n\nAtenciosamente,\nAtendimento"
    }
    
    return respostas.get(categoria, respostas["DEFAULT"])

# ======================================================
# FUNÇÃO PRINCIPAL
# ======================================================

def process_email_analysis(email_text, uploaded_file, from_email="", subject=""):
    """Processa análise de email"""
    
    print(f"\n🔧 CONFIGURAÇÃO:")
    print(f"   DEMO_MODE: {DEMO_MODE}")
    print(f"   HF disponível: {hf_handler.is_available()}")
    
    # Validação
    if not email_text and (not uploaded_file or not uploaded_file.filename):
        raise ValueError('Insira texto ou arquivo.')
    
    attachments_text = ""
    temp_file_path = None
    
    # Processar arquivo
    if uploaded_file and uploaded_file.filename:
        if not allowed_file(uploaded_file.filename):
            raise ValueError('Apenas PDF ou TXT.')
        
        uploaded_file.seek(0, os.SEEK_END)
        if uploaded_file.tell() > 10 * 1024 * 1024:
            raise ValueError('Arquivo muito grande.')
        uploaded_file.seek(0)
        
        # Usar extensão original
        original_ext = os.path.splitext(uploaded_file.filename)[1]
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=original_ext)
        temp_file_path = temp_file.name
        uploaded_file.save(temp_file_path)
        temp_file.close()
        
        try:
            # Extrair texto do arquivo
            print(f"📄 Extraindo texto de: {uploaded_file.filename}")
            file_text = file_handler.extract_text_from_file(temp_file_path, preprocess=False)
            
            print(f"📄 Texto extraído: {len(file_text)} caracteres")
            print(f"📄 Amostra: {file_text[:200]}...")
            
            # Se o email estiver vazio, usar o texto do arquivo
            if not email_text.strip():
                email_text = file_text
                print(f"📄 Usando conteúdo do arquivo como email")
            else:
                attachments_text = file_text
                
        except Exception as e:
            print(f"❌ ERRO CRÍTICO na extração de arquivo: {e}")
            import traceback
            traceback.print_exc()
            
            # Tentar abordagem mais simples
            try:
                if temp_file_path and os.path.exists(temp_file_path):
                    # Ler como texto puro
                    with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        simple_text = f.read()
                    
                    if not email_text.strip():
                        email_text = simple_text
                    else:
                        attachments_text = simple_text
            except:
                attachments_text = f"[Erro ao processar arquivo: {e}]"
    
    # SE NÃO HOUVER NENHUM TEXTO
    if not email_text.strip() and not attachments_text.strip():
        raise ValueError('Não foi possível extrair texto do arquivo.')
    
    try:
        print(f"\n{'='*60}")
        
        # ESCOLHER MÉTODO DE ANÁLISE
        use_real_ia = hf_handler.is_available() and not DEMO_MODE
        
        if use_real_ia:
            print("🤖 USANDO HUGGING FACE IA REAL")
            analysis = analise_ia_real(email_text, attachments_text, from_email, subject)
            source = "huggingface_ia"
        else:
            print("🎯 USANDO MODO DEMO/LOCAL")
            analysis = analise_ia_demo(email_text, attachments_text, from_email, subject)
            source = "demo" if DEMO_MODE else "local"
        
        # Verificar utilidade
        utilidade = analysis.get("utilidade", 0.5)
        is_useful = utilidade >= Config.EMAIL_THRESHOLD
        
        print(f"\n✅ ANÁLISE CONCLUÍDA:")
        print(f"   Categoria: {analysis['categoria_nome']}")
        print(f"   Utilidade: {utilidade:.0%}")
        print(f"   Fonte: {source}")
        
        return {
            'is_useful': is_useful,
            'analysis': analysis,
            'auto_response': analysis.get("resposta_completa", ""),
            'analysis_source': source
        }
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        
        # Resposta de emergência
        protocolo = f"ERR-{random.randint(1000, 9999)}"
        emergency_response = f"""Prezado(a),

Erro no processamento.

Protocolo: {protocolo}
Data: {datetime.now().strftime("%d/%m/%Y")}

Tente novamente.

Atenciosamente,
Sistema"""

        return {
            'is_useful': False,
            'analysis': {
                'categoria': 'ROTINA',
                'categoria_nome': 'Rotina',
                'utilidade': 0.5,
                'resumo': 'Erro processamento',
                'protocolo': protocolo,
                'fonte': 'erro'
            },
            'auto_response': emergency_response,
            'analysis_source': 'error'
        }
    
    finally:
        # Limpar arquivo
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# ======================================================
# TESTE
# ======================================================

if __name__ == "__main__":
    print("\n🧪 TESTE RÁPIDO")
    print("="*60)
    
    class FakeFile:
        filename = ""
    
    email_teste = """Prezada Sra. Carla,

Meu nome é João Silva e estou interessado na vaga de Analista.

Atenciosamente,
João Silva"""
    
    try:
        resultado = process_email_analysis(email_teste, FakeFile(), 
                                          "joao@email.com", 
                                          "Candidatura")
        
        print(f"\n✅ RESULTADO:")
        print(f"   Categoria: {resultado['analysis']['categoria_nome']}")
        print(f"   Utilidade: {resultado['analysis']['utilidade']:.0%}")
        print(f"   Fonte: {resultado['analysis_source']}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")