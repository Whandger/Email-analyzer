# install_render.py - INSTALADOR RENDER
import subprocess
import sys
import os

print("🔧 INSTALADOR PARA RENDER")
print("=" * 60)

# Verificar Python
print("\n🐍 Python:")
print(f"  Versão: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

# Lista de pacotes RENDER-SAFE (sem compilação)
packages = [
    "Flask==2.3.3",
    "Flask-CORS==4.0.0", 
    "gunicorn==21.2.0",
    "requests==2.31.0",
    "python-dotenv==1.0.0",
    "pdfplumber==0.10.3",
    "PyPDF2==3.0.1",
    "chardet==5.2.0",
    "beautifulsoup4==4.12.2",
    "nltk==3.8.1",
    "numpy==1.24.3",
    "scikit-learn==1.3.2"
]

print("\n📦 Instalando pacotes...")
for package in packages:
    try:
        print(f"  {package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except Exception as e:
        print(f"    ⚠️ {e}")

# Configurar NLTK
print("\n📚 NLTK:")
try:
    import nltk
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    print("  ✅ Recursos instalados")
except Exception as e:
    print(f"  ⚠️ {e}")

# Criar estrutura mínima
print("\n📁 Estrutura:")
dirs = ["server", "server/config", "server/utils", "static", "static/js", "static/css"]
for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)
    print(f"  📂 {dir_path}")

# Config básica
config_path = "server/config/config.py"
if not os.path.exists(config_path):
    with open(config_path, "w") as f:
        f.write("""
class Config:
    HF_TOKEN = ""
    DEBUG = True
    MAX_FILE_SIZE = 10 * 1024 * 1024
""")
    print(f"  ⚙️  {config_path}")

print("\n" + "=" * 60)
print("✅ PRONTO PARA RENDER")
print("\n🎯 Comandos úteis:")
print("   pip install -r requirements.txt")
print("   python server/app.py")
print("=" * 60)