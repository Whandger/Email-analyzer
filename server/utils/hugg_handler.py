# server/utils/hugg_handler.py - VERSÃO FINAL COM ENDPOINT CORRETO
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
            print(f"   Token válido?: {self.api_key.startswith('hf_')}")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # ⚠️⚠️⚠️ URL CORRIGIDA - NOVO ENDPOINT ⚠️⚠️⚠️
        # Conforme erro da API: "Please use https://router.huggingface.co instead"
        self.api_base_url = "https://router.huggingface.co"
        
        # Modelos

        self.classification_model = "typeform/distilbert-base-uncased-mnli"  # Alternativa que funciona
        self.summarization_model = "sshleifer/distilbart-cnn-12-6"  # Modelo mais leve
        
        # Cache
        self.cache = {}
        self.cache_enabled = True
        
        # Pré-processador
        self.text_processor = TextPreprocessor(language='portuguese')
        
        # Session
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = 30
        
        # Sempre considera API disponível se tem token
        if self.api_key and self.api_key.startswith('hf_'):
            self.api_available = True
            print("✅ API considerada disponível (token válido presente)")
        else:
            self.api_available = False
            print("⚠️  API indisponível (sem token válido)")

    def is_available(self) -> bool:
        """Verifica se a API está disponível para uso"""
        return self.api_available

    def _make_api_request(self, model: str, payload: Dict, use_cache: bool = True, retry_count: int = 0) -> Optional[Dict]:
        """Faz requisição para API com cache e retry - ENDPOINT CORRETO"""
        if not self.api_available:
            print(f"⏩ API não disponível, pulando {model}")
            return None
        
        # Cache
        cache_key = None
        if use_cache and self.cache_enabled:
            cache_str = f"{model}:{json.dumps(payload, sort_keys=True)}"
            cache_key = hashlib.md5(cache_str.encode()).hexdigest()
            
            if cache_key in self.cache:
                print(f"📦 Usando cache para {model}")
                return self.cache[cache_key]
        
        try:
            # ⚠️⚠️⚠️ URL ATUALIZADA PARA NOVO ENDPOINT ⚠️⚠️⚠️
            # Formato correto: https://router.huggingface.co/{model}
            url = f"{self.api_base_url}/{model}"
            print(f"🌐 Chamando {model} via router API...")
            
            response = self.session.post(
                url, 
                json=payload, 
                timeout=self.timeout
            )
            
            print(f"📡 Status da API: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ API respondeu com sucesso")
                
                # Cache
                if cache_key and self.cache_enabled:
                    self.cache[cache_key] = result
                    if len(self.cache) > 100:
                        self.cache.pop(next(iter(self.cache)))
                
                return result
                
            elif response.status_code == 503:
                # Modelo carregando
                print(f"⏳ Modelo {model} carregando...")
                if retry_count < 2:
                    time.sleep(3)
                    return self._make_api_request(model, payload, use_cache, retry_count + 1)
                return None
                
            elif response.status_code == 401:
                print("❌ Token HF inválido ou expirado")
                self.api_available = False
                return None
                
            elif response.status_code == 404:
                print(f"⚠️ Modelo {model} não encontrado na nova API")
                return None
                
            elif response.status_code == 410:
                print(f"❌ Endpoint antigo não suportado. Já estamos usando o correto: {self.api_base_url}")
                return None
                
            else:
                print(f"⚠️ API erro {response.status_code}: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout na chamada para {model}")
            return None
        except Exception as e:
            print(f"❌ Erro na API {model}: {e}")
            return None

    def analyze_email(self, email_content: str, attachments_text: str = "") -> Dict:
        """
        Analisa um email usando API do Hugging Face com pré-processamento NLP.
        
        Returns:
            Dict com análise completa
        """
        try:
            print("=" * 60)
            
            # SEMPRE mostrar se está usando API ou local
            if self.api_available:
                print("🤖 ANALISANDO EMAIL COM API HUGGING FACE...")
            else:
                print("🧠 ANALISANDO EMAIL COM NLP LOCAL...")
            
            # PRÉ-PROCESSAMENTO NLP
            print("\n🔧 Pré-processamento NLP...")
            processed_email = self.text_processor.preprocess_for_classification(email_content)
            
            print(f"📧 Conteúdo original: {len(email_content)} chars")
            print(f"📊 Conteúdo processado: {len(processed_email)} chars")
            
            # Processar anexos se houver
            processed_attachments = ""
            if attachments_text:
                processed_attachments = self.text_processor.preprocess_for_classification(attachments_text)
                print(f"📎 Anexos processados: {len(processed_attachments)} chars")
            
            # Extrair metadados
            metadata = self.text_processor.get_email_metadata(email_content)
            
            # Preparar conteúdo completo
            full_content = processed_email
            if processed_attachments:
                full_content += f" [ANEXOS] {processed_attachments}"
            
            # Limitar tamanho
            if len(full_content) > 1000:
                full_content = full_content[:1000]
                print(f"📝 Conteúdo truncado para 1000 chars")
            
            # 1. CLASSIFICAÇÃO
            print("\n🔍 Classificando email...")
            classification = self._classify_with_api(full_content, email_content)
            categoria_hf = classification.get("category", "email normal de rotina")
            confianca = classification.get("confidence", 0.5)
            api_used = classification.get("api_used", False)
            
            print(f"🎯 Categoria: {categoria_hf}")
            print(f"📈 Confiança: {confianca:.2f}")
            print(f"🌐 API usada: {api_used}")
            
            # 2. MAPEAR CATEGORIA
            categoria = self._map_category(categoria_hf, email_content)
            print(f"🗺️ Categoria mapeada: {categoria}")
            
            # 3. APLICAR HEURÍSTICAS
            categoria, utilidade = self._apply_heuristics_with_nlp(
                email_content, categoria, confianca, metadata
            )
            
            # 4. GERAR RESUMO
            print("\n📝 Gerando resumo...")
            summary_content = self.text_processor.preprocess_for_summarization(email_content[:500])
            summary = ""
            if self.api_available and api_used:
                summary = self._summarize_with_api(summary_content)
            else:
                summary = self._extract_lead_sentences(email_content)
            
            print(f"📄 Resumo: {summary[:80] if summary else 'N/A'}...")
            
            # 5. GERAR RESPOSTA
            print("\n💬 Gerando resposta...")
            response_text = self._generate_response(email_content[:300], categoria, classification)
            
            # 6. GERAR TAGS
            print("\n🏷️ Gerando tags...")
            tags = self._generate_tags_with_nlp(email_content, categoria, metadata)
            
            # 7. PALAVRAS-CHAVE
            keywords = self.text_processor.extract_keywords(email_content, top_n=5)
            
            # Resultado final
            resultado = {
                'utilidade': round(utilidade, 2),
                'categoria': categoria,
                'resumo': summary[:80] + "..." if summary and len(summary) > 80 else summary,
                'acao_necessaria': categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "PHISHING", "EDUCACIONAL"],
                'tags': tags,
                'resposta': response_text,
                'fonte': 'huggingface_api' if api_used else 'local_nlp',
                'metadata': {
                    'palavras_chave': keywords,
                    'contagem_palavras': metadata.get('word_count', 0),
                    'tem_anexos': metadata.get('has_attachments', False),
                    'tem_links': metadata.get('has_links', False),
                    'confianca_classificacao': confianca
                }
            }
            
            print(f"\n✅ ANÁLISE COMPLETA:")
            print(f"   Categoria: {resultado['categoria']}")
            print(f"   Utilidade: {resultado['utilidade']:.2f}")
            print(f"   Fonte: {resultado['fonte']}")
            print(f"   Tags: {', '.join(resultado['tags'][:4])}")
            print("=" * 60)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            import traceback
            traceback.print_exc()
            return self._create_default_analysis(email_content)

    def _classify_with_api(self, content: str, original_content: str = "") -> Dict:
        """Classificação usando API REST com fallback para heurística local"""
        
        # TENTAR API PRIMEIRO (se disponível)
        if self.api_available:
            try:
                # Labels otimizadas
                candidate_labels = [
                    "currículo profissional candidatura emprego vaga trabalho",
                    "email profissional corporativo trabalho reunião projeto equipe",
                    "documento financeiro nota fiscal boleto pagamento fatura",
                    "urgente importante prioridade emergência atenção", 
                    "comunicação institucional educacional matrícula curso universidade",
                    "promoção comercial spam marketing publicidade oferta",
                    "phishing fraude golpe segurança suspeito perigoso banco senha",
                    "email normal rotina comunicação mensagem contato"
                ]
                
                payload = {
                    "inputs": content[:800],
                    "parameters": {
                        "candidate_labels": candidate_labels,
                        "multi_label": False
                    }
                }
                
                print(f"🌐 Tentando API para classificação...")
                api_result = self._make_api_request(self.classification_model, payload)
                
                if api_result:
                    # Processar resposta
                    if isinstance(api_result, list):
                        api_result = api_result[0] if api_result else {}
                    
                    if isinstance(api_result, dict) and "labels" in api_result and "scores" in api_result:
                        labels = api_result["labels"]
                        scores = api_result["scores"]
                        
                        if labels and scores:
                            best_idx = scores.index(max(scores))
                            best_label = labels[best_idx]
                            best_score = scores[best_idx]
                            
                            print(f"✅ API: {best_label} (confiança: {best_score:.3f})")
                            
                            if best_score > 0.5:  # Confiança mínima
                                return {
                                    "category": best_label,
                                    "confidence": float(best_score),
                                    "api_used": True
                                }
                            else:
                                print(f"⚠️ Confiança baixa da API ({best_score:.3f}), usando heurística local")
                    
                    else:
                        print(f"⚠️ Formato inesperado da API: {type(api_result)}")
                
                print("ℹ️ API não retornou resultado válido, usando heurística local")
                
            except Exception as e:
                print(f"⚠️ Erro na API: {e}")
        
        # FALLBACK para heurística local
        print("🔄 Usando classificação heurística local...")
        local_result = self._fallback_classification_with_nlp(content, original_content)
        local_result["api_used"] = False
        return local_result

    def _fallback_classification_with_nlp(self, content: str, original_content: str = "") -> Dict:
        """Classificação local com heurísticas NLP"""
        analysis_content = original_content if original_content else content
        content_lower = analysis_content.lower()
        
        # Verificar currículo PRIMEIRO (mais importante)
        curriculo_keywords = ['curricul', 'cv', 'vag', 'empreg', 'candidatur', 
                             'linkedin', 'entrevist', 'profissional', 'trabalh',
                             'desenvolvedor', 'full', 'stack', 'junior', 'senior']
        curriculo_score = sum(1 for kw in curriculo_keywords if kw in content_lower)
        
        if curriculo_score >= 2:
            return {
                "category": "currículo profissional candidatura emprego vaga trabalho",
                "confidence": min(0.95, 0.6 + (curriculo_score * 0.05))
            }
        
        # Verificar educacional
        educacional_keywords = ['matricula', 'matrícula', 'curso', 'aluno', 'secretaria', 
                               'universidade', 'faculdade', 'disciplina']
        educacional_score = sum(1 for kw in educacional_keywords if kw in content_lower)
        
        if educacional_score >= 2:
            return {
                "category": "comunicação institucional educacional matrícula curso universidade",
                "confidence": min(0.95, 0.6 + (educacional_score * 0.05))
            }
        
        # Verificar financeiro
        financeiro_keywords = ['nota fiscal', 'boleto', 'fatura', 'pagamento', 'financeir']
        financeiro_score = sum(2 if 'nota fiscal' in kw or 'boleto' in kw else 1 
                              for kw in financeiro_keywords if kw in content_lower)
        
        if financeiro_score >= 2:
            return {
                "category": "documento financeiro nota fiscal boleto pagamento fatura",
                "confidence": min(0.95, 0.6 + (financeiro_score * 0.05))
            }
        
        # Verificar spam
        spam_keywords = ['descont', 'promoc', 'ofert', 'gratuit', 'marketing']
        spam_score = sum(1 for kw in spam_keywords if kw in content_lower)
        
        if spam_score >= 3:
            return {
                "category": "promoção comercial spam marketing publicidade oferta",
                "confidence": min(0.95, 0.6 + (spam_score * 0.04))
            }
        
        # Default
        return {
            "category": "email normal rotina comunicação mensagem contato",
            "confidence": 0.5
        }

    def _summarize_with_api(self, content: str) -> str:
        """Gera resumo usando API"""
        if not self.api_available or not content:
            return self._extract_lead_sentences(content)
        
        try:
            payload = {
                "inputs": content[:600],
                "parameters": {
                    "max_length": 150,
                    "min_length": 50
                }
            }
            
            api_result = self._make_api_request(self.summarization_model, payload)
            
            if api_result:
                if isinstance(api_result, list) and api_result and isinstance(api_result[0], dict):
                    return api_result[0].get("summary_text", "")
                elif isinstance(api_result, dict):
                    return api_result.get("summary_text", "")
                elif isinstance(api_result, str):
                    return api_result
        
        except Exception as e:
            print(f"⚠️ Erro na API de sumarização: {e}")
        
        return self._extract_lead_sentences(content)

    def _extract_lead_sentences(self, content: str, num_sentences: int = 2) -> str:
        """Extrai as primeiras frases significativas"""
        if not content:
            return ""
        
        sentences = re.split(r'(?<=[.!?])\s+', content)
        valid_sentences = [s.strip() for s in sentences if s.strip() and len(s.strip().split()) >= 3]
        lead_sentences = valid_sentences[:num_sentences]
        
        if lead_sentences:
            summary = '. '.join(lead_sentences) + '.'
            return summary[:100] + "..." if len(summary) > 100 else summary
        
        return content[:80] + "..."

    def _apply_heuristics_with_nlp(self, content: str, categoria: str, 
                                 confianca: float, metadata: Dict) -> Tuple[str, float]:
        """Aplica heurísticas avançadas com NLP"""
        # Utilidade base
        utility_base = {
            "CURRICULO": 0.92,
            "FINANCEIRO": 0.88,
            "IMPORTANTE": 0.85,
            "EDUCACIONAL": 0.82,
            "PROFISSIONAL": 0.78,
            "ROTINA": 0.45,
            "SPAM": 0.15,
            "PHISHING": 0.05
        }
        
        utilidade = utility_base.get(categoria, 0.5)
        
        # Ajustar pela confiança
        utilidade = utilidade * (0.6 + 0.4 * confianca)
        utilidade = min(0.99, max(0.05, utilidade))
        
        return categoria, round(utilidade, 2)

    def _generate_response(self, content: str, categoria_real: str, 
                          classification: Optional[Dict] = None) -> str:
        """Gera resposta apropriada"""
        responses = {
            "CURRICULO": "✅ **Currículo recebido com sucesso!** Agradecemos o envio do seu currículo. Analisaremos suas qualificações e entraremos em contato em breve.",
            "FINANCEIRO": "📄 **Documento financeiro registrado.** Confirmamos o recebimento. Nossa equipe fará a análise e retornará em até 48 horas úteis.",
            "IMPORTANTE": "🚨 **Mensagem importante identificada.** Daremos prioridade à análise deste assunto e retornaremos o mais breve possível.",
            "EDUCACIONAL": "🎓 **Comunicação educacional recebida.** Confirmamos o recebimento da sua mensagem institucional. Retornaremos em breve.",
            "PROFISSIONAL": "💼 **Email profissional recebido.** Agradecemos seu contato. Analisaremos o conteúdo e retornaremos dentro do prazo de 24 horas úteis.",
            "ROTINA": "📧 **Mensagem recebida.** Agradecemos seu contato. Retornaremos em breve.",
            "SPAM": "📭 **Email promocional detectado.** Esta mensagem foi classificada como material promocional. Filtro ativo.",
            "PHISHING": "⚠️ **ALERTA DE SEGURANÇA:** Email suspeito detectado. Não clique em links, não forneça informações pessoais e exclua esta mensagem."
        }
        
        return responses.get(categoria_real, responses["ROTINA"])

    def _map_category(self, hf_category: str, content: str = "") -> str:
        """Mapeia categoria do modelo para categorias internas"""
        hf_lower = hf_category.lower()
        
        # Mapeamento simples
        if any(word in hf_lower for word in ['currículo', 'curricul', 'emprego', 'vaga']):
            return "CURRICULO"
        elif any(word in hf_lower for word in ['financeiro', 'nota fiscal', 'boleto', 'pagamento']):
            return "FINANCEIRO"
        elif any(word in hf_lower for word in ['urgente', 'importante', 'prioridade']):
            return "IMPORTANTE"
        elif any(word in hf_lower for word in ['educacional', 'matrícula', 'curso', 'universidade']):
            return "EDUCACIONAL"
        elif any(word in hf_lower for word in ['profissional', 'corporativo', 'reunião']):
            return "PROFISSIONAL"
        elif any(word in hf_lower for word in ['promoção', 'spam', 'marketing']):
            return "SPAM"
        elif any(word in hf_lower for word in ['phishing', 'fraude', 'golpe']):
            return "PHISHING"
        else:
            return "ROTINA"

    def _generate_tags_with_nlp(self, content: str, category: str, metadata: Dict) -> List[str]:
        """Gera tags usando NLP"""
        tags = [category.lower()]
        
        # Tags específicas
        if category == "CURRICULO":
            tech_words = ['python', 'javascript', 'java', 'react', 'node', 'sql']
            content_lower = content.lower()
            tech_tags = [tech for tech in tech_words if tech in content_lower]
            tags.extend(tech_tags[:2])
            tags.extend(['curriculo', 'profissional'])
        
        # Tags genéricas
        keywords = self.text_processor.extract_keywords(content, top_n=4)
        tags.extend([kw for kw in keywords if len(kw) > 3][:2])
        
        return tags[:6]

    def _create_default_analysis(self, email_content: str) -> Dict:
        """Análise padrão com heurística NLP"""
        if not email_content:
            return self._get_fallback_response("ROTINA")
        
        content_lower = email_content.lower()
        
        # Verificar categorias simples
        if any(word in content_lower for word in ['curricul', 'cv', 'emprego']):
            return self._get_fallback_response("CURRICULO")
        elif any(word in content_lower for word in ['nota fiscal', 'boleto', 'fatura']):
            return self._get_fallback_response("FINANCEIRO")
        elif any(word in content_lower for word in ['matricula', 'curso', 'universidade']):
            return self._get_fallback_response("EDUCACIONAL")
        elif any(word in content_lower for word in ['urgente', 'importante']):
            return self._get_fallback_response("IMPORTANTE")
        elif any(word in content_lower for word in ['desconto', 'promoção', 'oferta']):
            return self._get_fallback_response("SPAM")
        else:
            return self._get_fallback_response("ROTINA")
    
    def _get_fallback_response(self, categoria: str) -> Dict:
        """Resposta de fallback padronizada"""
        responses = {
            "CURRICULO": {
                'utilidade': 0.92,
                'categoria': 'CURRICULO',
                'resumo': 'Currículo profissional detectado',
                'acao_necessaria': True,
                'tags': ['curriculo', 'profissional'],
                'resposta': '✅ Currículo recebido com sucesso!',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['curriculo']}
            },
            "EDUCACIONAL": {
                'utilidade': 0.82,
                'categoria': 'EDUCACIONAL',
                'resumo': 'Comunicação educacional detectada',
                'acao_necessaria': True,
                'tags': ['educacional', 'ensino'],
                'resposta': '🎓 Comunicação educacional recebida.',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['educacional']}
            },
            "SPAM": {
                'utilidade': 0.15,
                'categoria': 'SPAM',
                'resumo': 'Email promocional detectado',
                'acao_necessaria': False,
                'tags': ['spam', 'promocao'],
                'resposta': '[Email promocional detectado]',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['promocao']}
            },
            "FINANCEIRO": {
                'utilidade': 0.88,
                'categoria': 'FINANCEIRO',
                'resumo': 'Documento financeiro identificado',
                'acao_necessaria': True,
                'tags': ['financeiro', 'documento'],
                'resposta': 'Documento financeiro recebido para análise.',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['financeiro']}
            },
            "IMPORTANTE": {
                'utilidade': 0.85,
                'categoria': 'IMPORTANTE',
                'resumo': 'Email importante detectado',
                'acao_necessaria': True,
                'tags': ['importante', 'urgente'],
                'resposta': 'Email importante recebido. Análise prioritária.',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['importante']}
            },
            "PROFISSIONAL": {
                'utilidade': 0.78,
                'categoria': 'PROFISSIONAL',
                'resumo': 'Email profissional detectado',
                'acao_necessaria': False,
                'tags': ['profissional', 'corporativo'],
                'resposta': 'Email profissional recebido. Retornaremos em breve.',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': ['profissional']}
            },
            "ROTINA": {
                'utilidade': 0.45,
                'categoria': 'ROTINA',
                'resumo': 'Email de rotina - análise automática',
                'acao_necessaria': False,
                'tags': ['rotina', 'comum'],
                'resposta': 'Mensagem recebida. Agradecemos seu contato.',
                'fonte': 'local_nlp',
                'metadata': {'palavras_chave': []}
            }
        }
        
        return responses.get(categoria, responses["ROTINA"])

    def clear_cache(self):
        """Limpa o cache"""
        self.cache.clear()
        print("🧹 Cache limpo")