# server/utils/hugg_handler.py - VERSÃO SIMPLIFICADA SEM FASTTEXT
import os
import json
import requests
import re
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from server.config.config import Config
from .text_processor import TextPreprocessor


class HuggingFaceHandler:
    def __init__(self):
        """Inicializa o handler para usar API REST do Hugging Face"""
        # PEGA O TOKEN CORRETAMENTE
        self.api_key = Config.HF_TOKEN if hasattr(Config, 'HF_TOKEN') else os.getenv('HF_TOKEN', '')
        
        print(f"🔑 Token HF configurado: {'SIM' if self.api_key else 'NÃO'}")
        if self.api_key:
            print(f"   Token (inicia com): {self.api_key[:10]}...")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # URL da API
        self.api_base_url = "https://api-inference.huggingface.co/models"
        
        # Modelos leves que funcionam bem
        self.classification_model = "facebook/bart-large-mnli"
        self.summarization_model = "sshleifer/distilbart-cnn-6-6"  # Mais leve ainda
        
        # Cache
        self.cache = {}
        self.cache_enabled = True
        
        # Pré-processador
        self.text_processor = TextPreprocessor(language='portuguese')
        
        # Session
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = 15  # Timeout menor para Render
        
        # Verificar disponibilidade
        self.api_available = bool(self.api_key and self.api_key.startswith('hf_'))
        print(f"✅ API disponível: {self.api_available}")

    def is_available(self) -> bool:
        """Verifica se a API está disponível para uso"""
        return self.api_available

    def _make_api_request(self, model: str, payload: Dict) -> Optional[Dict]:
        """Faz requisição para API"""
        if not self.api_available:
            print(f"⏩ API não disponível, pulando {model}")
            return None
        
        try:
            url = f"{self.api_base_url}/{model}"
            print(f"🌐 Chamando {model}...")
            
            response = self.session.post(
                url, 
                json=payload, 
                timeout=self.timeout
            )
            
            print(f"📡 Status: {response.status_code}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                print(f"⏳ Modelo {model} carregando...")
                return None
            elif response.status_code in [401, 403]:
                print(f"❌ Problema de autenticação com a API")
                self.api_available = False
                return None
            else:
                print(f"⚠️ API erro {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro na API: {e}")
            return None

    def analyze_email(self, email_content: str, attachments_text: str = "") -> Dict:
        """
        Analisa um email - versão simplificada para Render
        """
        print("=" * 60)
        print("🤖 ANALISANDO EMAIL (Versão Render)...")
        
        try:
            # Conteúdo completo
            full_content = email_content
            if attachments_text:
                full_content += f"\n\n[ANEXOS]\n{attachments_text}"
            
            # 1. TENTAR CLASSIFICAÇÃO SIMPLES
            categoria = "ROTINA"
            utilidade = 0.5
            api_used = False
            
            if self.api_available:
                classification = self._classify_simple(full_content[:500])
                if classification:
                    categoria = classification["category"]
                    utilidade = classification["utility"]
                    api_used = True
                else:
                    # Fallback para análise local
                    categoria, utilidade = self._analyze_local(full_content)
            else:
                # Somente local
                categoria, utilidade = self._analyze_local(full_content)
            
            # 2. GERAR RESULTADO
            summary = self._extract_summary(email_content)
            tags = self._generate_tags(email_content, categoria)
            response_text = self._generate_response(categoria)
            
            resultado = {
                'utilidade': utilidade,
                'categoria': categoria,
                'resumo': summary,
                'acao_necessaria': categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "PHISHING"],
                'tags': tags,
                'resposta': response_text,
                'fonte': 'huggingface_api' if api_used else 'local_nlp',
                'metadata': {
                    'palavras_chave': self._extract_keywords(email_content),
                    'contagem_palavras': len(email_content.split()),
                    'confianca': utilidade
                }
            }
            
            print(f"\n✅ ANÁLISE CONCLUÍDA:")
            print(f"   Categoria: {categoria}")
            print(f"   Utilidade: {utilidade:.2f}")
            print(f"   Fonte: {resultado['fonte']}")
            print("=" * 60)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            return self._create_default_analysis(email_content)

    def _classify_simple(self, content: str) -> Optional[Dict]:
        """Classificação simples com API"""
        try:
            payload = {
                "inputs": content[:400],
                "parameters": {
                    "candidate_labels": ["curriculo emprego", "financeiro", "importante", "normal"],
                    "multi_label": False
                }
            }
            
            result = self._make_api_request(self.classification_model, payload)
            
            if result and isinstance(result, dict) and "labels" in result:
                best_label = result["labels"][0]
                confidence = result["scores"][0]
                
                # Mapear para categorias internas
                category_map = {
                    "curriculo emprego": "CURRICULO",
                    "financeiro": "FINANCEIRO", 
                    "importante": "IMPORTANTE",
                    "normal": "ROTINA"
                }
                
                categoria = category_map.get(best_label, "ROTINA")
                utilidade = confidence * 0.8 + 0.2  # Ajustar utilidade
                
                return {
                    "category": categoria,
                    "utility": min(0.95, utilidade)
                }
                
        except Exception as e:
            print(f"⚠️ Erro na classificação: {e}")
        
        return None

    def _analyze_local(self, content: str) -> Tuple[str, float]:
        """Análise local com keywords"""
        content_lower = content.lower()
        
        # Keywords para cada categoria
        keywords = {
            "CURRICULO": ['curriculo', 'cv', 'emprego', 'vaga', 'linkedin', 'github'],
            "FINANCEIRO": ['nota fiscal', 'boleto', 'fatura', 'pagamento'],
            "IMPORTANTE": ['urgente', 'importante', 'emergencia'],
            "EDUCACIONAL": ['matricula', 'curso', 'universidade', 'faculdade'],
            "SPAM": ['promocao', 'desconto', 'oferta', 'grátis'],
            "PHISHING": ['senha', 'conta', 'banco', 'cartão', 'cpf']
        }
        
        scores = {}
        for category, words in keywords.items():
            score = sum(2 if word in content_lower else 0 for word in words)
            if score > 0:
                scores[category] = score
        
        # Determinar categoria
        if scores:
            categoria = max(scores.items(), key=lambda x: x[1])[0]
            max_score = scores[categoria]
            utilidade = min(0.95, 0.4 + (max_score * 0.1))
        else:
            categoria = "ROTINA"
            utilidade = 0.5
        
        return categoria, utilidade

    def _extract_summary(self, content: str) -> str:
        """Extrai resumo simples"""
        sentences = re.split(r'(?<=[.!?])\s+', content)
        valid = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if valid:
            summary = '. '.join(valid[:2]) + '.'
            return summary[:100] + "..." if len(summary) > 100 else summary
        
        return content[:80] + "..."

    def _generate_tags(self, content: str, category: str) -> List[str]:
        """Gera tags simples"""
        tags = [category.lower()]
        
        # Adicionar algumas tags baseadas em conteúdo
        content_lower = content.lower()
        tech_words = ['python', 'javascript', 'java', 'react']
        for tech in tech_words:
            if tech in content_lower:
                tags.append(tech)
                break
        
        return tags[:3]

    def _extract_keywords(self, content: str) -> List[str]:
        """Extrai palavras-chave simples"""
        words = content.lower().split()
        common_words = {'de', 'em', 'para', 'com', 'que', 'é', 'do', 'da', 'no', 'na'}
        keywords = [w for w in words if len(w) > 4 and w not in common_words]
        return list(set(keywords))[:5]

    def _generate_response(self, category: str) -> str:
        """Gera resposta apropriada"""
        responses = {
            "CURRICULO": "✅ **Currículo recebido com sucesso!**",
            "FINANCEIRO": "📄 **Documento financeiro registrado.**",
            "IMPORTANTE": "🚨 **Mensagem importante identificada.**",
            "EDUCACIONAL": "🎓 **Comunicação educacional recebida.**",
            "PROFISSIONAL": "💼 **Email profissional recebido.**",
            "ROTINA": "📧 **Mensagem recebida.**",
            "SPAM": "📭 **Email promocional detectado.**",
            "PHISHING": "⚠️ **Alerta de segurança!**"
        }
        return responses.get(category, responses["ROTINA"])

    def _create_default_analysis(self, email_content: str) -> Dict:
        """Análise padrão de fallback"""
        return {
            'utilidade': 0.5,
            'categoria': 'ROTINA',
            'resumo': 'Análise não disponível no momento.',
            'acao_necessaria': False,
            'tags': ['rotina'],
            'resposta': 'Mensagem recebida.',
            'fonte': 'fallback',
            'metadata': {
                'palavras_chave': [],
                'contagem_palavras': len(email_content.split())
            }
        }