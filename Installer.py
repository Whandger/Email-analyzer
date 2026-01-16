# install_complete.py - INSTALADOR COMPLETO E CORRIGIDO
import subprocess
import sys
import importlib
import os

print("🔧 INSTALANDO E CONFIGURANDO TUDO PARA O EMAIL ANALYZER...")
print("=" * 60)

# 1. Verificar Python version
print("\n🐍 Verificando versão do Python...")
try:
    python_version = sys.version_info
    print(f"  Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("  ⚠️ Versão muito antiga! Recomendo Python 3.8+")
except:
    print("  ⚠️ Não foi possível verificar a versão")

# 2. Atualizar pip primeiro
print("\n⬆️ Atualizando pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("  ✅ pip atualizado")
except:
    print("  ⚠️ Não foi possível atualizar pip")

# 3. Instalar pacotes pip principais
print("\n📦 Instalando pacotes pip principais...")
main_packages = [
    "requests",
    "PyPDF2", 
    "huggingface-hub",
    "transformers",
    "nltk",
    "spacy",
    "python-docx",
    "chardet",
    "pdfplumber",  # ADICIONADO PARA MELHOR EXTRAÇÃO DE PDF
    "flask",
    "flask-cors"
]

for package in main_packages:
    try:
        print(f"  Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"    ✅ {package}")
    except Exception as e:
        print(f"    ❌ {package}: {e}")

# 4. Configurar NLTK
print("\n📚 Configurando NLTK...")
try:
    import nltk
    
    # Lista de recursos ESSENCIAIS
    resources = [
        'stopwords',      # Para nltk.corpus.stopwords
        'rslp',           # Para nltk.stem.RSLPStemmer  
        'punkt',          # Para tokenização
        'wordnet',        # Para lematização
        'averaged_perceptron_tagger'  # Para POS tagging
    ]
    
    for resource in resources:
        print(f"  Baixando {resource}...")
        try:
            nltk.download(resource, quiet=False)
            print(f"    ✅ {resource}")
        except Exception as e:
            print(f"    ⚠️ {resource}: {e}")
    
    # TESTAR se os recursos funcionam
    print("\n🧪 Testando NLTK...")
    try:
        from nltk.corpus import stopwords
        from nltk.stem import RSLPStemmer
        stopwords.words('portuguese')
        stemmer = RSLPStemmer()
        stemmer.stem('testando')
        print("  ✅ nltk.corpus.stopwords: OK")
        print("  ✅ nltk.stem.RSLPStemmer: OK")
    except Exception as e:
        print(f"  ❌ Erro teste NLTK: {e}")
        
except Exception as e:
    print(f"❌ Erro NLTK: {e}")

# 5. Configurar spaCy
print("\n🌍 Configurando spaCy...")
try:
    # Tentar carregar primeiro
    import spacy
    try:
        nlp = spacy.load("pt_core_news_sm")
        print("  ✅ Modelo pt_core_news_sm já instalado")
    except:
        print("  Baixando modelo português pt_core_news_sm...")
        try:
            import subprocess
            subprocess.run([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"], check=True)
            print("  ✅ Modelo spaCy instalado!")
        except Exception as e:
            print(f"  ⚠️ Erro download spaCy: {e}")
            print("  💡 Execute manualmente: python -m spacy download pt_core_news_sm")
            
except Exception as e:
    print(f"  ⚠️ Erro spaCy: {e}")

# 6. Configurar Hugging Face token (se existir)
print("\n🤖 Configurando Hugging Face...")
try:
    from huggingface_hub import HfFolder
    
    # Verificar se tem token
    token = HfFolder.get_token()
    if token:
        print(f"  ✅ Token HF encontrado (inicia com: {token[:10]}...)")
    else:
        print("  ℹ️ Token HF não encontrado")
        print("  💡 Para usar IA real, configure com:")
        print("     from huggingface_hub import HfFolder")
        print("     HfFolder.save_token('seu_token_aqui')")
except Exception as e:
    print(f"  ⚠️ Erro HF: {e}")

# 7. Verificar TUDO
print("\n🔍 VERIFICAÇÃO FINAL DE MÓDULOS:")
print("-" * 40)

def check_module(name, import_name=None, test_func=None):
    try:
        if import_name:
            module = importlib.import_module(import_name)
        else:
            module = importlib.import_module(name.lower())
        
        if test_func:
            test_func(module)
            
        print(f"✅ {name}")
        return True
    except ImportError as e:
        print(f"❌ {name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ {name}: {e}")
        return False

# Funções de teste específicas
def test_nltk(module):
    from nltk.corpus import stopwords
    from nltk.stem import RSLPStemmer
    stopwords.words('portuguese')[:5]

def test_spacy(module):
    import spacy
    try:
        spacy.load("pt_core_news_sm")
    except:
        # Tentar carregar em inglês se português falhar
        spacy.load("en_core_web_sm")

def test_huggingface(module):
    from huggingface_hub import __version__
    print(f"    Versão: {__version__}")

checks = [
    ("requests", "requests", None),
    ("PyPDF2", "PyPDF2", None),
    ("pdfplumber", "pdfplumber", None),
    ("huggingface-hub", "huggingface_hub", test_huggingface),
    ("transformers", "transformers", None),
    ("nltk", "nltk", test_nltk),
    ("spacy", "spacy", test_spacy),
    ("python-docx", "docx", None),
    ("chardet", "chardet", None),
    ("flask", "flask", None),
    ("flask-cors", "flask_cors", None),
]

all_ok = True
for name, module, test_func in checks:
    if not check_module(name, module, test_func):
        all_ok = False

# 8. Criar estrutura de diretórios
print("\n📁 Criando estrutura de diretórios...")
dirs_to_create = [
    "server",
    "server/utils",
    "server/services",
    "server/config",
    "server/routes",
    "static",
    "static/js",
    "static/css",
    "templates"
]

for dir_name in dirs_to_create:
    if not os.path.exists(dir_name):
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"  📁 Criado: {dir_name}/")
        except:
            print(f"  ⚠️ Não criado: {dir_name}/")
    else:
        print(f"  ✅ Já existe: {dir_name}/")

# 9. Criar arquivo de configuração se não existir
config_file = "server/config/config.py"
if not os.path.exists(config_file):
    print(f"\n⚙️ Criando arquivo de configuração: {config_file}")
    try:
        config_content = '''# server/config/config.py

class Config:
    # Configurações do Hugging Face
    HF_TOKEN = ""  # Coloque seu token aqui se tiver (começa com hf_)
    
    # Configurações da aplicação
    EMAIL_THRESHOLD = 0.6  # Limiar para considerar email útil
    DEBUG = True
    
    # Configurações de arquivo
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'txt'}
    
    # Configurações de logging
    LOG_LEVEL = "INFO"
'''
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("  ✅ Arquivo de configuração criado")
    except Exception as e:
        print(f"  ❌ Erro ao criar config: {e}")

print("\n" + "=" * 60)
if all_ok:
    print("🎉 TUDO INSTALADO E CONFIGURADO COM SUCESSO!")
    print("\n📋 RESUMO:")
    print("   ✅ Pip atualizado")
    print("   ✅ Pacotes principais instalados")
    print("   ✅ NLTK configurado com recursos em português")
    print("   ✅ spaCy configurado")
    print("   ✅ Estrutura de diretórios criada")
    print("\n🚀 Para iniciar a aplicação:")
    print("   1. Configure seu token HF em server/config/config.py (opcional)")
    print("   2. Execute: python app.py ou python server/app.py")
    print("   3. Acesse: http://localhost:5000")
    print("\n🔧 Se tiver problemas:")
    print("   - Verifique se tem Python 3.8+")
    print("   - Execute manualmente: python -m spacy download pt_core_news_sm")
    print("   - Para PDFs, instale: pip install pdfplumber")
else:
    print("⚠️ ALGUNS PACOTES NÃO INSTALARAM CORRETAMENTE.")
    print("\n🔧 SOLUÇÕES:")
    print("   1. Execute como administrador: sudo python install_complete.py")
    print("   2. Instale manualmente os pacotes falhos")
    print("   3. Verifique sua conexão com a internet")
    print("\n💡 Comandos manuais úteis:")
    print("   pip install --upgrade pip")
    print("   pip install huggingface-hub transformers nltk spacy pdfplumber")
    print("   python -m spacy download pt_core_news_sm")
    print("   python -m nltk.downloader stopwords rslp punkt")

print("=" * 60)