# server/config/config.py - VERSÃO PRODUÇÃO
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 🔐 API Keys (obrigatório em produção)
    PERPLEXITY_API_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
    
    # ⚙️ Configurações
    EMAIL_THRESHOLD = float(os.environ.get("EMAIL_THRESHOLD", "0.3"))
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # 🔧 Modelos
    PERPLEXITY_DEFAULT_MODEL = os.environ.get("PERPLEXITY_MODEL", "sonar")
    PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
    
    # 🚀 Configurações de produção
    REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "30"))
    MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "2"))
    
    # 📊 Rate limiting (produção)
    RATE_LIMIT_PER_MINUTE = int(os.environ.get("RATE_LIMIT", "60"))
    
    @staticmethod
    def is_perplexity_available():
        """Verifica se a API está disponível"""
        key = Config.PERPLEXITY_API_KEY
        return bool(key and key.startswith("pplx-"))
    
    @staticmethod
    def get_headers():
        """Headers para API com timeout"""
        if Config.is_perplexity_available():
            return {
                "Authorization": f"Bearer {Config.PERPLEXITY_API_KEY}",
                "Content-Type": "application/json",
                "User-Agent": f"Perplexity-Email-Analyzer/1.0"
            }
        return {}
    
    @staticmethod
    def validate_production():
        """Validação rigorosa para produção"""
        errors = []
        
        if not Config.PERPLEXITY_API_KEY:
            errors.append("PERPLEXITY_API_KEY não configurada")
        elif not Config.PERPLEXITY_API_KEY.startswith("pplx-"):
            errors.append("PERPLEXITY_API_KEY inválida (deve começar com 'pplx-')")
        
        # Verificar limite de arquivo
        if Config.MAX_FILE_SIZE > 25 * 1024 * 1024:  # 25MB máximo
            errors.append("MAX_FILE_SIZE muito grande")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "config": {
                "model": Config.PERPLEXITY_DEFAULT_MODEL,
                "timeout": Config.REQUEST_TIMEOUT,
                "rate_limit": Config.RATE_LIMIT_PER_MINUTE
            }
        }