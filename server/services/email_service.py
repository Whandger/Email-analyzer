# server/services/email_service.py - VERSÃO SOMENTE IA
import os
import tempfile
import re
import random
import time
from datetime import datetime

from server.utils.file_handler import FileHandler
from server.utils.perplexity_handler import PerplexityHandler
from server.config.config import Config

# Inicializar handlers
file_handler = FileHandler()
perplexity_handler = PerplexityHandler()

# ======================================================
# CONSTANTES
# ======================================================

CATEGORIAS = {
    "PHISHING": {"nome": "Phishing", "emoji": "🚫", "prioridade": "CRÍTICA", "departamento": "Segurança"},
    "CURRICULO": {"nome": "Currículo", "emoji": "📄", "prioridade": "ALTA", "departamento": "RH"},
    "FINANCEIRO": {"nome": "Financeiro", "emoji": "💰", "prioridade": "ALTA", "departamento": "Financeiro"},
    "IMPORTANTE": {"nome": "Importante", "emoji": "⭐", "prioridade": "ALTA", "departamento": "Diretoria"},
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
    """Extrai informações do remetente usando regex"""
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

# ======================================================
# FUNÇÃO DE ANÁLISE COM PERPLEXITY
# ======================================================

def analise_ia_perplexity(conteudo_email, conteudo_anexo="", remetente="", assunto=""):
    """Usa APENAS Perplexity API para análise"""
    print("🤖 PERPLEXITY IA: Analisando...")
    
    start_time = time.time()
    
    # Usar Perplexity Handler para análise completa
    analysis = perplexity_handler.analyze_email(conteudo_email, conteudo_anexo, remetente, assunto)
    
    # Extrair informações do remetente
    conteudo_completo = conteudo_email + " " + conteudo_anexo
    info_remetente = extrair_informacoes_email(conteudo_completo)
    
    # Gerar protocolo
    protocolo = f"PPX-{random.randint(10000, 99999)}"
    
    # Obter categoria da análise do Perplexity
    categoria = analysis['categoria']
    
    # Tempo de análise
    elapsed_time = time.time() - start_time
    print(f"✅ Análise concluída em {elapsed_time:.2f}s")
    
    # ✅ CORREÇÃO: Retornar estrutura compatível com o JavaScript
    return {
        "categoria": categoria,
        "categoria_nome": CATEGORIAS[categoria]["nome"],
        "categoria_emoji": CATEGORIAS[categoria]["emoji"],
        "utilidade": analysis['utilidade'],  # Já calculada pelo Perplexity
        "confianca_ia": analysis['metadata']['confianca_classificacao'],
        "resumo": analysis['resumo'],
        "acao_necessaria": analysis['acao_necessaria'],
        "prioridade": CATEGORIAS[categoria]["prioridade"],
        "protocolo": protocolo,
        "tags": analysis['tags'],
        "resposta_completa": analysis['resposta'],
        "departamento": CATEGORIAS[categoria]["departamento"],
        "info_remetente": info_remetente,
        "fonte": "perplexity_ia",
        "detalhes": analysis.get('metadata', {})
    }

# ======================================================
# FUNÇÃO PRINCIPAL
# ======================================================

def process_email_analysis(email_text, uploaded_file, from_email="", subject=""):
    """Processa análise de email usando SOMENTE IA"""
    
    print(f"\n🔧 CONFIGURAÇÃO:")
    print(f"   Usar Perplexity: Sim")
    print(f"   Perplexity disponível: {perplexity_handler.is_available}")
    
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
            
            # Se o email estiver vazio, usar o texto do arquivo
            if not email_text.strip():
                email_text = file_text
                print(f"📄 Usando conteúdo do arquivo como email")
            else:
                attachments_text = file_text
                
        except Exception as e:
            print(f"❌ ERRO na extração de arquivo: {e}")
            import traceback
            traceback.print_exc()
            
            # Tentar abordagem mais simples
            try:
                if temp_file_path and os.path.exists(temp_file_path):
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
        print("🤖 USANDO PERPLEXITY IA REAL")
        
        # Usar SOMENTE Perplexity
        analysis = analise_ia_perplexity(email_text, attachments_text, from_email, subject)
        
        # Verificar utilidade
        utilidade = analysis.get("utilidade", 0.5)
        is_useful = utilidade >= Config.EMAIL_THRESHOLD
        
        print(f"\n✅ ANÁLISE CONCLUÍDA:")
        print(f"   Categoria: {analysis['categoria_nome']}")
        print(f"   Utilidade: {utilidade:.0%}")
        print(f"   Fonte: perplexity_ia")
        
        return {
            'is_useful': is_useful,
            'analysis': analysis,
            'auto_response': analysis.get("resposta_completa", ""),
            'analysis_source': 'perplexity_ia'
        }
    
    except Exception as e:
        print(f"❌ Erro na análise IA: {e}")
        import traceback
        traceback.print_exc()
        
        # Resposta de emergência
        protocolo = f"ERR-{random.randint(1000, 9999)}"
        emergency_response = f"""Prezado(a),

Erro no processamento da análise.

Protocolo: {protocolo}
Data: {datetime.now().strftime("%d/%m/%Y")}

Erro: {str(e)[:100]}

Atenciosamente,
Sistema de Análise"""

        return {
            'is_useful': False,
            'analysis': {
                'categoria': 'ROTINA',
                'categoria_nome': 'Rotina',
                'utilidade': 0.1,  # Baixa utilidade em caso de erro
                'resumo': f'Erro: {str(e)[:50]}',
                'protocolo': protocolo,
                'fonte': 'erro_ia'
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
    print("\n🧪 TESTE DO SISTEMA (SOMENTE IA)")
    print("="*60)
    
    # Validar configuração
    Config.validate()
    
    class FakeFile:
        filename = ""
    
    # Teste com phishing
    email_phishing = """Assunto: Urgente: Sua conta do banco foi comprometida!
De: suporte@bancoseguro-alerta.com

Prezado(a) cliente,

Detectamos uma tentativa de login suspeita na sua conta bancária. Para evitar bloqueio, você deve verificar sua identidade imediatamente.

Clique aqui para confirmar seus dados:
http://bancoseguro-alerta.com/verificacao-urgente

Caso não acesse o link em até 24 horas, sua conta será suspensa.

Atenciosamente,
Departamento de Segurança – Banco Seguro"""
    
    try:
        print("\n📧 Testando análise de phishing...")
        resultado = process_email_analysis(email_phishing, FakeFile(), 
                                          "suporte@bancoseguro-alerta.com", 
                                          "Urgente: Sua conta do banco foi comprometida!")
        
        print(f"\n✅ RESULTADO:")
        print(f"   Categoria: {resultado['analysis']['categoria_nome']}")
        print(f"   Utilidade: {resultado['analysis']['utilidade']:.0%}")
        print(f"   Ação Necessária: {resultado['analysis']['acao_necessaria']}")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")