import os
import json
import requests
import re
from typing import Dict, List, Optional, Tuple
from huggingface_hub import InferenceClient
from server.config.config import Config
from .text_processor import TextPreprocessor


class HuggingFaceHandler:
    def __init__(self):
        """Inicializa o cliente Hugging Face com NLP"""
        self.api_key = Config.HF_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Inicializar pré-processador NLP
        self.text_processor = TextPreprocessor(language='portuguese')
        
        # DEBUG: Verificar token
        print(f"🔑 Token HF (primeiros 10 chars): {self.api_key[:10] if self.api_key else 'NONE'}")
        print(f"📝 Token válido? {self.api_key and self.api_key.startswith('hf_')}")
        
        # Modelos
        self.classification_model = "facebook/bart-large-mnli"
        self.summarization_model = "Falconsai/text_summarization"
        self.text_generation_model = "google/flan-t5-large"
        
        # URLs atualizadas
        self.api_base_url = "https://router.huggingface.co"
        self.old_api_base_url = "https://api-inference.huggingface.co"
        
        # Inicializar client
        self.client = None
        if self.api_key and self.api_key.startswith("hf_"):
            try:
                print("🔄 Tentando inicializar InferenceClient...")
                self.client = InferenceClient(token=self.api_key)
                print(f"✅ HuggingFace Handler inicializado com NLP")
                print(f"🔍 Client disponível: {self.client is not None}")
            except Exception as e:
                print(f"⚠️ Erro InferenceClient: {e}")
                self.client = None
        else:
            print("⚠️ Token HF inválido ou ausente")

    def is_available(self):
        """Verifica se está disponível"""
        return self.client is not None and self.api_key and self.api_key.startswith("hf_")

    def analyze_email(self, email_content: str, attachments_text: str = "") -> Dict:
        """
        Analisa um email usando Hugging Face com pré-processamento NLP.
        
        Returns:
            Dict com análise completa
        """
        try:
            print("=" * 60)
            print("🤖 Hugging Face + NLP analisando...")
            
            # PRÉ-PROCESSAMENTO NLP
            print("\n🔧 Pré-processamento NLP...")
            processed_email = self.text_processor.preprocess_for_classification(email_content)
            
            print(f"📧 Conteúdo ORIGINAL: {len(email_content)} chars")
            print(f"📊 Conteúdo PROCESSADO: {len(processed_email)} chars")
            print(f"📋 Amostra processada: {processed_email[:200]}...")
            
            # Processar anexos se houver
            processed_attachments = ""
            if attachments_text:
                processed_attachments = self.text_processor.preprocess_for_classification(attachments_text)
                print(f"📎 Anexos processados: {len(processed_attachments)} chars")
            
            # Extrair metadados
            metadata = self.text_processor.get_email_metadata(email_content)
            print(f"📊 Metadados: {metadata}")
            
            # Preparar conteúdo completo (processado)
            full_content = processed_email
            if processed_attachments:
                full_content += f" [ANEXOS] {processed_attachments}"
            
            # Limitar tamanho para APIs
            if len(full_content) > 1000:
                full_content = full_content[:1000]
                print(f"📝 Conteúdo truncado para 1000 chars")
            
            # 1. CLASSIFICAÇÃO
            print("\n🔍 Iniciando classificação com NLP...")
            classification = self._classify_content(full_content, email_content)
            print(f"📊 Resultado classificação: {classification}")
            
            # 2. RESUMO
            print("\n📝 Gerando resumo...")
            summary_content = self.text_processor.preprocess_for_summarization(email_content[:500])
            summary = self._summarize_content(summary_content)
            print(f"📄 Resumo gerado: {summary[:100]}...")
            
            # Processar resultados
            categoria_hf = classification.get("category", "email normal de rotina")
            confianca = classification.get("confidence", 0.5)
            
            print(f"\n🎯 Categoria HF: {categoria_hf}")
            print(f"📈 Confiança: {confianca:.2f}")
            
            # Mapear categoria
            categoria = self._map_category(categoria_hf, email_content)
            print(f"🗺️ Categoria mapeada: {categoria}")
            
            # HEURÍSTICA MELHORADA COM NLP
            categoria, utilidade = self._apply_heuristics_with_nlp(
                email_content, categoria, confianca, metadata
            )
            
            # 3. RESPOSTA
            print("\n💬 Gerando resposta...")
            response_text = self._generate_response(email_content[:300], categoria, classification)
            print(f"✉️ Resposta gerada: {response_text[:100]}...")
            
            # 4. TAGS COM PALAVRAS-CHAVE NLP
            print("\n🏷️ Gerando tags com NLP...")
            tags = self._generate_tags_with_nlp(email_content, categoria, metadata)
            print(f"🏷️ Tags geradas: {tags}")
            
            # 5. PALAVRAS-CHAVE EXTRAS
            keywords = self.text_processor.extract_keywords(email_content, top_n=5)
            print(f"🔑 Palavras-chave extraídas: {keywords}")
            
            # Resultado final
            resultado = {
                'utilidade': utilidade,
                'categoria': categoria,
                'resumo': summary[:80] if summary else f"Classificado como {categoria}",
                'acao_necessaria': categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "PHISHING", "EDUCACIONAL"],
                'tags': tags,
                'resposta': response_text,
                'fonte': 'huggingface_ia_nlp' if self.is_available() else 'fallback_nlp',
                'metadata': {
                    'palavras_chave': keywords,
                    'contagem_palavras': metadata['word_count'],
                    'tem_anexos': metadata['has_attachments'],
                    'tem_links': metadata['has_links']
                }
            }
            
            print(f"\n✅ ANÁLISE FINALIZADA COM NLP:")
            print(f"   Categoria: {resultado['categoria']}")
            print(f"   Utilidade: {resultado['utilidade']:.2f}")
            print(f"   Tags: {resultado['tags'][:4]}")
            print(f"   Palavras-chave: {resultado['metadata']['palavras_chave']}")
            print("=" * 60)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro HF: {e}")
            import traceback
            traceback.print_exc()
            return self._create_default_analysis(email_content)

    def _classify_content(self, content: str, original_content: str = "") -> Dict:
        """Classificação zero-shot com conteúdo pré-processado"""
        try:
            print(f"\n📊 _classify_content() com NLP")
            print(f"📝 Conteúdo processado: {content[:150]}...")
            
            # LABELS OTIMIZADAS PARA PORTUGUÊS
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
            
            print(f"🏷️ Labels disponíveis: {candidate_labels}")
            
            # PRIMEIRO: Verificar se é reunião/profissional
            if original_content:
                reuniao_keywords = ['reuniao', 'reunião', 'pauta', 'equipe', 'projeto', 'comercial']
                content_lower = original_content.lower()
                reuniao_score = sum(1 for kw in reuniao_keywords if kw in content_lower)
                
                if reuniao_score >= 2:
                    print(f"🎯 HEURÍSTICA REUNIÃO: Score {reuniao_score}")
                    return {
                        "category": "email profissional corporativo trabalho reunião projeto equipe",
                        "confidence": 0.85
                    }
            
            # SEGUNDO: Verificar se é currículo
            if original_content:
                curriculo_keywords = ['curricul', 'cv', 'curriculo', 'resume', 'portfolio', 
                                     'linkedin', 'github', 'experiencia', 'formacao', 
                                     'habilidades', 'competencias', 'objetivo']
                content_lower = original_content.lower()
                curriculo_score = sum(1 for kw in curriculo_keywords if kw in content_lower)
                
                if curriculo_score >= 3:
                    print(f"🎯 HEURÍSTICA CURRÍCULO: Score {curriculo_score}")
                    return {
                        "category": "currículo profissional candidatura emprego vaga trabalho",
                        "confidence": 0.85
                    }
            
            # TENTAR COM InferenceClient
            if self.client and self.is_available():
                print("🔄 Tentando InferenceClient.zero_shot_classification...")
                try:
                    safe_content = content[:800] if len(content) > 800 else content
                    
                    result = self.client.zero_shot_classification(
                        safe_content,
                        candidate_labels=candidate_labels,
                        multi_label=False
                    )
                    
                    print(f"📊 Tipo da resposta: {type(result)}")
                    
                    # Formato novo do InferenceClient
                    if hasattr(result, 'labels') and hasattr(result, 'scores'):
                        labels = result.labels
                        scores = result.scores
                        
                        if labels and scores:
                            best_index = scores.index(max(scores))
                            best_label = labels[best_index]
                            best_score = scores[best_index]
                            
                            print(f"✅ Melhor resultado: {best_label} ({best_score:.3f})")
                            return {
                                "category": best_label,
                                "confidence": float(best_score)
                            }
                    
                    # Formato antigo
                    elif isinstance(result, dict) and 'labels' in result and 'scores' in result:
                        labels = result["labels"]
                        scores = result["scores"]
                        
                        if labels and scores:
                            best_index = scores.index(max(scores))
                            best_label = labels[best_index]
                            best_score = scores[best_index]
                            
                            print(f"✅ Melhor resultado: {best_label} ({best_score:.3f})")
                            return {
                                "category": best_label,
                                "confidence": float(best_score)
                            }
                    
                    else:
                        print("⚠️ Formato de resposta inesperado do InferenceClient")
                        return self._fallback_classification_with_nlp(content, original_content)
                        
                except Exception as e:
                    print(f"⚠️ Erro InferenceClient: {e}")
                    return self._fallback_classification_with_nlp(content, original_content)
            
            # Se InferenceClient não disponível ou falhou, usar heurística NLP
            print("🔄 InferenceClient não disponível, usando heurística NLP...")
            return self._fallback_classification_with_nlp(content, original_content)
                
        except Exception as e:
            print(f"❌ Erro classificação: {e}")
            return self._fallback_classification_with_nlp(content, original_content)

    def _fallback_classification_with_nlp(self, content: str, original_content: str = "") -> Dict:
        """Fallback com heurística e NLP - MELHORADA"""
        print(f"\n🔄 Usando classificação heurística com NLP")
        
        # Usar conteúdo original se disponível
        analysis_content = original_content if original_content else content
        keywords = self.text_processor.extract_keywords(analysis_content, top_n=15)
        print(f"🔑 Palavras-chave extraídas: {keywords}")
        
        content_lower = analysis_content.lower()
        
        # 0. PRIMEIRO: Verificar se é REUNIÃO/PROFISSIONAL
        reuniao_keywords = ['reuniao', 'reunião', 'pauta', 'equipe', 'projeto', 'comercial',
                           'relatorio', 'relatório', 'apresentacao', 'apresentação']
        reuniao_score = sum(1 for kw in reuniao_keywords if kw in content_lower)
        
        if reuniao_score >= 2:
            print(f"✅ HEURÍSTICA REUNIÃO/PROFISSIONAL: Score {reuniao_score}")
            return {
                "category": "email profissional corporativo trabalho reunião projeto equipe",
                "confidence": min(0.95, 0.7 + (reuniao_score * 0.05))
            }
        
        # 1. Verificar se é EDUCACIONAL
        educacional_keywords = ['matricula', 'matrícula', 'curso', 'aluno', 'secretaria', 
                               'universidade', 'faculdade', 'disciplina', 'calendário', 
                               'acadêmico', 'professor', 'academico', 'campus', 'turma',
                               'pós-graduação', 'graduação', 'semestre', 'nota', 'prova']
        
        educacional_score = 0
        for kw in educacional_keywords:
            if kw in content_lower:
                educacional_score += 1
        
        if educacional_score >= 3:
            print(f"✅ HEURÍSTICA EDUCACIONAL: Score {educacional_score}")
            return {
                "category": "comunicação institucional educacional matrícula curso universidade",
                "confidence": min(0.95, 0.7 + (educacional_score * 0.05))
            }
        
        # 2. Verificar se é currículo
        curriculo_keywords = ['curricul', 'cv', 'vag', 'empreg', 'candidatur', 
                             'linkedin', 'entrevist', 'profissional', 'trabalh',
                             'desenvolvedor', 'full', 'stack', 'junior', 'senior',
                             'experiencia', 'formacao', 'habilidades', 'objetivo']
        
        curriculo_score = 0
        for kw in curriculo_keywords:
            if kw in content_lower:
                curriculo_score += 1
        
        if curriculo_score >= 3:
            print(f"✅ HEURÍSTICA CURRÍCULO: Score {curriculo_score}")
            return {
                "category": "currículo profissional candidatura emprego vaga trabalho",
                "confidence": min(0.95, 0.7 + (curriculo_score * 0.04))
            }
        
        # 3. Verificar se é financeiro
        financeiro_keywords = ['nota fiscal', 'nfe', 'bolet', 'fatur', 'pagament', 
                              'financeir', 'impost', 'tribut', 'tax', 'valor', 
                              'reais', 'compra', 'venda', 'transação']
        
        financeiro_score = 0
        for kw in financeiro_keywords:
            if kw in content_lower:
                financeiro_score += 2 if 'nota fiscal' in kw or 'boleto' in kw or 'fatura' in kw else 1
        
        if financeiro_score >= 3:
            print(f"✅ HEURÍSTICA FINANCEIRO: Score {financeiro_score}")
            return {
                "category": "documento financeiro nota fiscal boleto pagamento fatura",
                "confidence": min(0.95, 0.6 + (financeiro_score * 0.05))
            }
        
        # 4. Verificar se é phishing
        phishing_keywords = ['clicar aqui', 'atualizar dados', 'sua conta', 'senha expira',
                            'conta suspensa', 'acesso bloqueado', 'urgentemente',
                            'banco', 'cartão de crédito', 'cpf', 'rg', 'número do cartão',
                            'pix', 'segurança', 'suspeito', 'fraude', 'golpe']
        
        phishing_score = 0
        for kw in phishing_keywords:
            if kw in content_lower:
                phishing_score += 2 if any(word in kw for word in ['senha', 'conta', 'banco', 'cartão', 'cpf', 'rg']) else 1
        
        if phishing_score >= 3:
            print(f"✅ HEURÍSTICA PHISHING: Score {phishing_score}")
            return {
                "category": "phishing fraude golpe segurança suspeito perigoso banco senha",
                "confidence": min(0.95, 0.6 + (phishing_score * 0.05))
            }
        
        # 5. Verificar se é spam/promoção
        spam_keywords = ['descont', 'promoc', 'ofert', 'gratuit', 'fret', 
                        'exclusiv', 'limit', 'aproveit', 'comerc', 'compre agora',
                        'clique para comprar', 'só hoje', 'última chance', 'corra']
        
        spam_score = 0
        for kw in spam_keywords:
            if kw in content_lower:
                spam_score += 2 if any(word in kw for word in ['desconto', 'promoção', 'oferta', 'grátis']) else 1
        
        if spam_score >= 3:
            print(f"✅ HEURÍSTICA SPAM: Score {spam_score}")
            return {
                "category": "promoção comercial spam marketing publicidade oferta",
                "confidence": min(0.95, 0.7 + (spam_score * 0.04))
            }
        
        # 6. Verificar se é importante/urgente
        importante_keywords = ['urgent', 'importante', 'prioridade', 'emergência', 
                              'atenção', 'crítico', 'urgentemente', 'prazo final']
        
        importante_score = 0
        for kw in importante_keywords:
            if kw in content_lower:
                importante_score += 1
        
        if importante_score >= 2:
            print(f"✅ HEURÍSTICA IMPORTANTE: Score {importante_score}")
            return {
                "category": "urgente importante prioridade emergência atenção",
                "confidence": min(0.95, 0.7 + (importante_score * 0.05))
            }
        
        # 7. Default: email normal de rotina
        print(f"📋 HEURÍSTICA DEFAULT: Email de rotina")
        return {
            "category": "email normal rotina comunicação mensagem contato",
            "confidence": 0.5
        }

    def _apply_heuristics_with_nlp(self, content: str, categoria: str, 
                                 confianca: float, metadata: Dict) -> Tuple[str, float]:
        """Aplica heurísticas avançadas com NLP"""
        
        # Utilidade base por categoria - INCLUINDO EDUCACIONAL
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
        content_lower = content.lower()
        
        # DETECÇÃO DE EDUCACIONAL (se não foi detectado antes)
        if categoria != "EDUCACIONAL":
            educacional_indicators = ['matricula', 'matrícula', 'curso', 'aluno', 'secretaria', 
                                     'universidade', 'faculdade', 'disciplina', 'calendário', 
                                     'acadêmico', 'professor', 'campus', 'turma', 'pós-graduação']
            
            educacional_score = sum(1 for indicator in educacional_indicators if indicator in content_lower)
            
            if educacional_score >= 3:
                print(f"🎯 HEURÍSTICA EDUCACIONAL: Score {educacional_score}")
                categoria = "EDUCACIONAL"
                utilidade = 0.82
                confianca = max(confianca, 0.7)
        
        # DETECÇÃO DE CURRÍCULO - MAIS ROBUSTA
        if categoria != "CURRICULO":
            cv_indicators = ['curricul', 'cv', 'vag', 'empreg', 'candidatur', 
                            'linkedin', 'entrevist', 'desenvolvedor', 'full stack',
                            'junior', 'senior', 'pleno', 'github', 'portifolio',
                            'experiencia', 'formacao', 'habilidades']
            cv_score = sum(1 for indicator in cv_indicators if indicator in content_lower)
            
            has_formal_closure = any(word in content_lower for word in 
                                   ['atenciosamente', 'cordialmente', 'sinceramente', 
                                    'grato', 'obrigado', 'prezado', 'prezada'])
            
            has_contact_info = any(word in content_lower for word in 
                                 ['@', 'telefone', 'celular', 'email', 'github', 'linkedin'])
            
            # Se tem muitos indicadores de currículo, reclassificar
            if cv_score >= 5 or (cv_score >= 3 and has_formal_closure and has_contact_info):
                print(f"🎯 HEURÍSTICA CURRÍCULO FORTE: Score {cv_score}")
                categoria = "CURRICULO"
                utilidade = 0.92
                confianca = max(confianca, 0.8)
        
        # DETECÇÃO DE IMPORTANTE (sobrescreve outras categorias exceto PHISHING)
        if categoria not in ["PHISHING", "CURRICULO", "FINANCEIRO"]:
            importante_indicators = ['urgente', 'importante', 'prioridade', 'emergência', 
                                   'crítico', 'urgentemente', 'prazo final', 'imediatamente']
            
            importante_score = sum(1 for indicator in importante_indicators if indicator in content_lower)
            
            if importante_score >= 2:
                print(f"🎯 HEURÍSTICA IMPORTANTE: Score {importante_score}")
                # Se for educacional e importante, manter como EDUCACIONAL mas aumentar utilidade
                if categoria == "EDUCACIONAL":
                    utilidade = 0.88
                else:
                    categoria = "IMPORTANTE"
                    utilidade = 0.85
        
        # Ajustar utilidade baseado na confiança
        utilidade = utilidade * (0.6 + 0.4 * confianca)
        utilidade = min(0.99, max(0.05, utilidade))
        
        print(f"📊 Utilidade final: {utilidade:.2f} (base ajustada para categoria)")
        
        return categoria, utilidade

    def _summarize_content(self, content: str) -> str:
        """Gera resumo do conteúdo"""
        try:
            print(f"\n📝 _summarize_content()")
            
            processed_content = self.text_processor.preprocess_for_summarization(content)
            
            if self.client and self.is_available():
                print(f"🔄 Tentando summarization...")
                try:
                    result = self.client.summarization(
                        processed_content[:600],
                        model=self.summarization_model
                    )
                    
                    if hasattr(result, 'summary_text'):
                        summary = result.summary_text
                    elif isinstance(result, str):
                        summary = result
                    elif isinstance(result, dict) and 'summary_text' in result:
                        summary = result['summary_text']
                    else:
                        summary = self._extract_lead_sentences(content)
                    
                    print(f"📄 Resumo: {summary[:120]}...")
                    return summary
                except Exception as e:
                    print(f"⚠️ Erro summarization: {e}")
            
            return self._extract_lead_sentences(content)
                
        except Exception as e:
            print(f"❌ Erro resumo: {e}")
            return content[:100] + "..."

    def _extract_lead_sentences(self, content: str, num_sentences: int = 3) -> str:
        """Extrai as primeiras frases significativas"""
        if not content:
            return ""
        
        # Usar regex melhorado para separar frases
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        valid_sentences = [
            s.strip() for s in sentences 
            if s.strip() and len(s.strip().split()) >= 4
        ]
        
        lead_sentences = valid_sentences[:num_sentences]
        
        if lead_sentences:
            summary = '. '.join(lead_sentences) + '.'
            if len(summary) > 120:
                summary = summary[:117] + '...'
            return summary
        
        return content[:100] + "..."

    def _generate_response(self, content: str, categoria_real: str, 
                          classification: Optional[Dict] = None) -> str:
        """Gera resposta apropriada"""
        try:
            print(f"\n💬 _generate_response() - Categoria: {categoria_real}")
            
            # Respostas melhoradas - INCLUINDO EDUCACIONAL
            default_responses = {
                "CURRICULO": "✅ **Currículo recebido com sucesso!** Agradecemos o envio do seu currículo. Analisaremos suas qualificações e entraremos em contato em breve. Mantenha seu LinkedIn e GitHub atualizados!",
                "FINANCEIRO": "📄 **Documento financeiro registrado.** Confirmamos o recebimento. Nossa equipe fará a análise e retornará em até 48 horas úteis.",
                "IMPORTANTE": "🚨 **Mensagem importante identificada.** Daremos prioridade à análise deste assunto e retornaremos o mais breve possível.",
                "EDUCACIONAL": "🎓 **Comunicação educacional recebida.** Confirmamos o recebimento da sua mensagem institucional. Retornaremos em breve.",
                "PROFISSIONAL": "💼 **Email profissional recebido.** Agradecemos seu contato. Analisaremos o conteúdo e retornaremos dentro do prazo de 24 horas úteis.",
                "ROTINA": "📧 **Mensagem recebida.** Agradecemos seu contato. Retornaremos em breve.",
                "SPAM": "📭 **Email promocional detectado.** Esta mensagem foi classificada como material promocional. Filtro ativo.",
                "PHISHING": "⚠️ **ALERTA DE SEGURANÇA:** Email suspeito detectado. Não clique em links, não forneça informações pessoais e exclua esta mensagem. Entre em contato com o suporte se necessário."
            }
            
            print(f"📋 Usando resposta padrão para {categoria_real}")
            return default_responses.get(categoria_real, default_responses["ROTINA"])
                
        except Exception as e:
            print(f"❌ Erro resposta: {e}")
            return "Mensagem recebida. Agradecemos seu contato."

    def _map_category(self, hf_category: str, content: str = "") -> str:
        """Mapeia categoria do modelo para categorias internas - COM EDUCACIONAL"""
        hf_lower = hf_category.lower()
        
        # PRIMEIRO: Verificar se é educacional baseado no conteúdo
        if content:
            educacional_keywords = ['matricula', 'matrícula', 'curso', 'aluno', 'secretaria', 
                                   'universidade', 'faculdade', 'disciplina', 'calendário', 
                                   'acadêmico', 'professor', 'campus', 'turma']
            content_lower = content.lower()
            educacional_score = sum(1 for kw in educacional_keywords if kw in content_lower)
            
            if educacional_score >= 3:
                print(f"🎯 MAPEAMENTO EDUCACIONAL: {educacional_score} indicadores")
                return "EDUCACIONAL"
        
        # SEGUNDO: Verificar se é currículo baseado no conteúdo
        if content:
            curriculo_keywords = ['curricul', 'cv', 'resume', 'linkedin', 'github', 
                                 'experiencia', 'formacao', 'habilidades', 'objetivo',
                                 'candidatura', 'vaga', 'emprego']
            content_lower = content.lower()
            curriculo_score = sum(1 for kw in curriculo_keywords if kw in content_lower)
            
            if curriculo_score >= 3:
                print(f"🎯 MAPEAMENTO CURRÍCULO: {curriculo_score} indicadores")
                return "CURRICULO"
        
        # TERCEIRO: Verificar se é profissional/reunião baseado no conteúdo
        if content:
            profissional_keywords = ['reuniao', 'reunião', 'pauta', 'equipe', 'projeto',
                                    'relatorio', 'relatório', 'apresentacao', 'apresentação',
                                    'corporativo', 'comercial', 'empresa', 'negócio']
            content_lower = content.lower()
            profissional_score = sum(1 for kw in profissional_keywords if kw in content_lower)
            
            if profissional_score >= 2 and curriculo_score < 3:  # Só se não for currículo
                print(f"🎯 MAPEAMENTO PROFISSIONAL: {profissional_score} indicadores")
                return "PROFISSIONAL"
        
        # Mapeamento baseado na categoria do modelo (fallback)
        if any(word in hf_lower for word in ['currículo', 'curricul', 'emprego', 'vaga', 'candidatur', 'trabalho']):
            # Verificar se não é falso positivo para profissional
            if content and any(word in content.lower() for word in ['reuniao', 'reunião', 'pauta', 'equipe']):
                print(f"🎯 CORREÇÃO: Reunião detectada, mapeando para PROFISSIONAL")
                return "PROFISSIONAL"
            return "CURRICULO"
        elif any(word in hf_lower for word in ['financeiro', 'nota fiscal', 'boleto', 'pagamento', 'fatura']):
            return "FINANCEIRO"
        elif any(word in hf_lower for word in ['urgente', 'importante', 'prioridade', 'emergência']):
            return "IMPORTANTE"
        elif any(word in hf_lower for word in ['educacional', 'matrícula', 'curso', 'universidade', 'institucional']):
            return "EDUCACIONAL"
        elif any(word in hf_lower for word in ['profissional', 'corporativo', 'reunião', 'projeto', 'equipe']):
            return "PROFISSIONAL"
        elif any(word in hf_lower for word in ['promoção', 'spam', 'marketing', 'publicidade']):
            return "SPAM"
        elif any(word in hf_lower for word in ['phishing', 'fraude', 'golpe', 'segurança', 'suspeito', 'perigoso']):
            return "PHISHING"
        else:
            return "ROTINA"

    def _generate_tags_with_nlp(self, content: str, category: str, metadata: Dict) -> List[str]:
        """Gera tags usando NLP"""
        print(f"\n🏷️ _generate_tags_with_nlp() - Categoria: '{category}'")
        
        tags = [category.lower()]
        
        # Tags específicas por categoria
        if category == "CURRICULO":
            tech_keywords = ['python', 'javascript', 'java', 'react', 'node', 'sql', 
                            'mysql', 'postgresql', 'docker', 'aws', 'github']
            content_lower = content.lower()
            
            tech_tags = [tech for tech in tech_keywords if tech in content_lower]
            tags.extend(tech_tags[:3])
            
            # Adicionar nível profissional
            if 'junior' in content_lower:
                tags.append('junior')
            elif 'senior' in content_lower or 'sênior' in content_lower:
                tags.append('senior')
            elif 'pleno' in content_lower:
                tags.append('pleno')
            
            tags.extend(['curriculo', 'profissional', 'tecnologia'])
        
        elif category == "EDUCACIONAL":
            educacional_tags = ['ensino', 'aprendizado', 'instituição', 'estudos']
            tags.extend(educacional_tags[:2])
        
        # Tags genéricas
        keywords = self.text_processor.extract_keywords(content, top_n=6)
        tags.extend([kw for kw in keywords if len(kw) > 3][:3])
        
        category_tags = {
            "SPAM": ['comercial', 'promocao', 'marketing'],
            "FINANCEIRO": ['documento', 'financeiro', 'pagamento'],
            "PHISHING": ['segurança', 'alerta', 'fraude'],
            "IMPORTANTE": ['urgente', 'prioridade'],
            "PROFISSIONAL": ['corporativo', 'negocios', 'empresa'],
            "EDUCACIONAL": ['ensino', 'academico', 'estudo'],
            "ROTINA": ['comum', 'correspondencia']
        }
        
        tags.extend(category_tags.get(category, []))
        
        # Tags baseadas em metadados
        if metadata.get('has_attachments'):
            tags.append('com_anexo')
        if metadata.get('has_links'):
            tags.append('com_links')
            
        if metadata.get('word_count', 0) > 200:
            tags.append('longo')
        elif metadata.get('word_count', 0) < 50:
            tags.append('curto')
        
        # Remover duplicatas e limitar
        unique_tags = list(dict.fromkeys([tag for tag in tags if tag]))
        print(f"📋 Tags finais: {unique_tags[:8]}")
        
        return unique_tags[:10]

    def _create_default_analysis(self, email_content: str, metadata: Optional[Dict] = None) -> Dict:
        """Análise padrão com heurística NLP"""
        print(f"\n🔄 _create_default_analysis() com NLP")
        
        if not email_content:
            return self._get_fallback_response("ROTINA")
        
        content_lower = email_content.lower()
        
        # Verificar se é educacional
        educacional_indicators = ['matricula', 'matrícula', 'curso', 'aluno', 'secretaria', 
                                 'universidade', 'faculdade', 'disciplina', 'calendário']
        educacional_score = sum(1 for indicator in educacional_indicators if indicator in content_lower)
        
        if educacional_score >= 3:
            print(f"🎯 HEURÍSTICA EDUCACIONAL: Score {educacional_score}")
            return self._get_fallback_response("EDUCACIONAL")
        
        # Verificar se é currículo
        curriculo_indicators = ['curricul', 'cv', 'vaga', 'emprego', 'candidatura',
                               'linkedin', 'github', 'experiencia', 'formacao']
        curriculo_score = sum(1 for indicator in curriculo_indicators if indicator in content_lower)
        
        if curriculo_score >= 3:
            print(f"🎯 HEURÍSTICA CURRÍCULO: Score {curriculo_score}")
            return self._get_fallback_response("CURRICULO")
        
        # Verificar SPAM
        spam_keywords = ['desconto', 'promoção', 'oferta', 'grátis', 'frete', 'promocao']
        spam_count = sum(1 for word in spam_keywords if word in content_lower)
        
        if spam_count >= 3:
            print(f"🎯 HEURÍSTICA SPAM: {spam_count} palavras")
            return self._get_fallback_response("SPAM")
        
        # Verificar phishing
        phishing_indicators = ['clicar aqui', 'atualizar dados', 'sua conta', 'senha expira',
                              'conta suspensa', 'banco', 'cartão', 'cpf', 'rg']
        phishing_count = sum(1 for phrase in phishing_indicators if phrase in content_lower)
        
        if phishing_count >= 3:
            print(f"🎯 HEURÍSTICA PHISHING: {phishing_count} indicadores")
            return self._get_fallback_response("PHISHING")
        
        # Verificar financeiro
        finance_indicators = ['nota fiscal', 'boleto', 'fatura', 'pagamento', 'nfe']
        if any(indicator in content_lower for indicator in finance_indicators):
            print(f"🎯 HEURÍSTICA FINANCEIRO")
            return self._get_fallback_response("FINANCEIRO")
        
        # Verificar importante
        important_indicators = ['urgente', 'importante', 'prioridade', 'emergência']
        if any(indicator in content_lower for indicator in important_indicators):
            print(f"🎯 HEURÍSTICA IMPORTANTE")
            return self._get_fallback_response("IMPORTANTE")
        
        # Verificar profissional
        professional_indicators = ['reunião', 'projeto', 'relatório', 'equipe', 'corporativo']
        professional_count = sum(1 for indicator in professional_indicators if indicator in content_lower)
        
        if professional_count >= 2:
            print(f"🎯 HEURÍSTICA PROFISSIONAL: {professional_count} indicadores")
            return self._get_fallback_response("PROFISSIONAL")
        
        print("📋 Usando fallback ROTINA")
        return self._get_fallback_response("ROTINA")
    
    def _get_fallback_response(self, categoria: str) -> Dict:
        """Resposta de fallback padronizada - INCLUINDO EDUCACIONAL"""
        responses = {
            "CURRICULO": {
                'utilidade': 0.92,
                'categoria': 'CURRICULO',
                'resumo': 'Currículo profissional detectado via análise heurística',
                'acao_necessaria': True,
                'tags': ['curriculo', 'profissional', 'tecnologia', 'fallback_nlp'],
                'resposta': '✅ Currículo recebido com sucesso! Analisaremos suas qualificações.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['curriculo', 'profissional', 'tecnologia']}
            },
            "EDUCACIONAL": {
                'utilidade': 0.82,
                'categoria': 'EDUCACIONAL',
                'resumo': 'Comunicação educacional detectada via análise heurística',
                'acao_necessaria': True,
                'tags': ['educacional', 'ensino', 'academico', 'fallback_nlp'],
                'resposta': '🎓 Comunicação educacional recebida. Processaremos sua solicitação.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['educacional', 'ensino', 'academico']}
            },
            "SPAM": {
                'utilidade': 0.15,
                'categoria': 'SPAM',
                'resumo': 'Email promocional detectado via análise heurística',
                'acao_necessaria': False,
                'tags': ['spam', 'promocao', 'marketing', 'fallback_nlp'],
                'resposta': '[Email promocional detectado]',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['promocao', 'desconto', 'oferta']}
            },
            "PHISHING": {
                'utilidade': 0.05,
                'categoria': 'PHISHING',
                'resumo': 'Possível phishing detectado via heurística de segurança',
                'acao_necessaria': True,
                'tags': ['phishing', 'segurança', 'alerta', 'fallback_nlp'],
                'resposta': '⚠️ Email suspeito detectado. Tome cuidado.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['segurança', 'alerta', 'suspeito']}
            },
            "FINANCEIRO": {
                'utilidade': 0.88,
                'categoria': 'FINANCEIRO',
                'resumo': 'Documento financeiro identificado via heurística',
                'acao_necessaria': True,
                'tags': ['financeiro', 'documento', 'pagamento', 'fallback_nlp'],
                'resposta': 'Documento financeiro recebido para análise.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['financeiro', 'documento', 'pagamento']}
            },
            "IMPORTANTE": {
                'utilidade': 0.85,
                'categoria': 'IMPORTANTE',
                'resumo': 'Email importante detectado via palavras-chave',
                'acao_necessaria': True,
                'tags': ['importante', 'urgente', 'prioridade', 'fallback_nlp'],
                'resposta': 'Email importante recebido. Análise prioritária.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['importante', 'urgente', 'prioridade']}
            },
            "PROFISSIONAL": {
                'utilidade': 0.78,
                'categoria': 'PROFISSIONAL',
                'resumo': 'Email profissional detectado via análise heurística',
                'acao_necessaria': False,
                'tags': ['profissional', 'corporativo', 'trabalho', 'fallback_nlp'],
                'resposta': 'Email profissional recebido. Retornaremos em breve.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': ['profissional', 'trabalho', 'empresa']}
            },
            "ROTINA": {
                'utilidade': 0.45,
                'categoria': 'ROTINA',
                'resumo': 'Email de rotina - análise automática',
                'acao_necessaria': False,
                'tags': ['rotina', 'comum', 'correspondencia', 'fallback_nlp'],
                'resposta': 'Mensagem recebida. Agradecemos seu contato.',
                'fonte': 'fallback_nlp',
                'metadata': {'palavras_chave': []}
            }
        }
        
        return responses.get(categoria, responses["ROTINA"])