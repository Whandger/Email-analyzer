# server/config/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # APIs
    HF_TOKEN = os.getenv("HF_TOKEN", "")
    
    # Configurações
    EMAIL_THRESHOLD = 0.6
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def is_huggingface_available():
        """Verifica se Hugging Face está disponível"""
        return bool(Config.HF_TOKEN and 
                   Config.HF_TOKEN.startswith("hf_"))
    
    
    @staticmethod
    def validate():
        print("🔍 Validando configurações...")
        
        if Config.is_huggingface_available():
            masked = Config.HF_TOKEN[:6] + "..." + Config.HF_TOKEN[-4:]
            print(f"✅ Hugging Face: {masked}")
        else:
            print("❌ Hugging Face não configurado")
        
        return True