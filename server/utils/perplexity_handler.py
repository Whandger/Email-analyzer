# server/utils/perplexity_handler.py - VERSÃO CORRIGIDA
import os
import json
import requests
import time
import re 
from typing import Dict, Optional
from dotenv import load_dotenv
from server.config.config import Config
from .text_processor import TextPreprocessor

# Carregar variáveis de ambiente
load_dotenv()

class PerplexityHandler:
    def __init__(self):
        """Inicializa o cliente Perplexity AI"""
        self.api_key = Config.PERPLEXITY_API_KEY
        self.api_url = Config.PERPLEXITY_API_URL
        
        # Inicializar pré-processador NLP
        self.text_processor = TextPreprocessor(language='português')
        
        # Modelo padrão
        self.model = Config.PERPLEXITY_DEFAULT_MODEL
        
        # Configurações
        self.timeout = 30
        self.max_retries = 2
        
        # Headers
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"🚀 PerplexityHandler inicializado (Modelo: {self.model})")
    
    @property
    def is_available(self):
        """Propriedade que verifica se está disponível"""
        return bool(self.api_key and self.api_key.startswith('pplx-'))
    
    def analyze_email(self, email_content: str, attachments_text: str = "", 
                     from_email: str = "", subject: str = "") -> Dict:
        """
        Analisa email e gera resposta personalizada por IA
        """
        if not self.is_available:
            raise Exception("🚨 Perplexity não disponível. Configure sua API Key.")
        
        try:
            start_time = time.time()
            
            # 1. Classificar o email
            classification = self._classify_email(email_content, from_email, subject)
            categoria = classification['categoria']
            confianca = classification['confianca']
            
            print(f"📊 Classificado como: {categoria} (confiança: {confianca:.2f})")
            
            # 2. Gerar resumo
            summary = self._generate_summary(email_content, categoria)
            
            # 3. Gerar resposta personalizada por IA (COMPLETA, sem placeholders)
            ai_response = self._generate_complete_ai_response(
                email_content, 
                categoria,
                from_email,
                subject,
                summary
            )
            
            # 4. Calcular utilidade REAL
            utilidade = self._calculate_utility(categoria, confianca)
            
            elapsed = time.time() - start_time
            
            # 5. Preparar resultado
            result = {
                'utilidade': utilidade,
                'categoria': categoria,
                'resumo': summary[:120] + "..." if len(summary) > 120 else summary,
                'acao_necessaria': categoria in ["CURRICULO", "FINANCEIRO", "IMPORTANTE", "PHISHING"],
                'tags': self._generate_tags(categoria, email_content),
                'resposta': ai_response,  # ← Já vem completa
                'fonte': 'perplexity_ia',
                'metadata': {
                    'palavras_chave': self.text_processor.extract_keywords(email_content, top_n=3),
                    'modelo_usado': self.model,
                    'tempo_processamento': f"{elapsed:.2f}s",
                    'confianca_classificacao': confianca
                }
            }
            
            print(f"✅ Análise concluída em {elapsed:.2f}s")
            print(f"📝 Resposta gerada (primeiros 100 chars): {ai_response[:100]}...")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro na análise IA: {e}")
            raise Exception(f"Falha na análise IA: {str(e)}")
    
    def _classify_email(self, email_content: str, from_email: str, subject: str) -> Dict:
        """Classifica o email em uma categoria usando IA"""
        processed_content = self.text_processor.preprocess_for_classification(email_content[:1000])
        
        system_prompt = """Você é um classificador de emails corporativos em português. 
        Classifique o email em UMA destas categorias:
        - CURRICULO: Candidaturas, currículos, solicitações de emprego
        - FINANCEIRO: Documentos financeiros, notas fiscais, boletos, pagamentos
        - IMPORTANTE: Emails urgentes, críticos, da diretoria
        - PROFISSIONAL: Propostas comerciais, orçamentos, reuniões profissionais
        - PHISHING: Emails suspeitos, tentativas de fraude, golpes (urgência falsa, links suspeitos)
        - SPAM: Propaganda, marketing não solicitado, promoções
        - ROTINA: Emails administrativos, comunicação interna normal
        
        Responda APENAS no formato JSON:
        {"categoria": "NOME_DA_CATEGORIA", "confianca": 0.95}"""
        
        user_prompt = f"""Classifique este email:
        
        ASSUNTO: {subject}
        REMETENTE: {from_email}
        
        CONTEÚDO:
        {processed_content}"""
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 100,
            "temperature": 0.1
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Parse JSON
                    content_clean = content.strip()
                    if '```json' in content_clean:
                        content_clean = content_clean.split('```json')[1].split('```')[0]
                    elif '```' in content_clean:
                        content_clean = content_clean.split('```')[1].split('```')[0]
                    
                    classification = json.loads(content_clean)
                    
                    # Validar categoria
                    categoria = classification.get("categoria", "ROTINA").upper()
                    valid_cats = ["CURRICULO", "FINANCEIRO", "IMPORTANTE", 
                                 "PROFISSIONAL", "PHISHING", "SPAM", "ROTINA"]
                    
                    if categoria not in valid_cats:
                        categoria = "ROTINA"
                    
                    confianca = float(classification.get("confianca", 0.5))
                    confianca = min(1.0, max(0.0, confianca))
                    
                    return {"categoria": categoria, "confianca": confianca}
                    
                elif attempt < self.max_retries - 1:
                    print(f"⚠️  Tentativa {attempt + 1} falhou, retentando...")
                    time.sleep(1)
                    
            except (requests.exceptions.Timeout, json.JSONDecodeError) as e:
                if attempt < self.max_retries - 1:
                    print(f"⚠️  Erro: {e}, retentando...")
                    time.sleep(1)
                else:
                    raise Exception(f"Falha na classificação: {e}")
        
        raise Exception("Falha na classificação após múltiplas tentativas")
    
    def _generate_summary(self, email_content: str, categoria: str) -> str:
        """Gera um resumo breve do email"""
        if categoria == "PHISHING":
            return "🚨 TENTATIVA DE PHISHING DETECTADA - Este email é uma fraude e deve ser ignorado (0% utilidade)."
        elif categoria == "SPAM":
            return "📭 EMAIL PROMOCIONAL NÃO SOLICITADO - Baixa relevância (5% utilidade máxima)."
        
        try:
            prompt = f"""Faça um resumo muito breve (1-2 frases) deste email classificado como {categoria}:
            
            {email_content[:600]}
            
            Resumo conciso:"""
            
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 80,
                "temperature": 0.3
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                summary = result['choices'][0]['message']['content'].strip()
                return summary.replace("Resumo:", "").replace("resumo:", "").strip()
            else:
                return f"📧 Email classificado como {categoria} (utilidade: {self._calculate_utility_base(categoria):.0%})"
                
        except Exception as e:
            print(f"⚠️  Erro ao gerar resumo: {e}")
            return f"📧 Email classificado como {categoria}"
    
    def _generate_complete_ai_response(self, email_content: str, categoria: str, 
                                      from_email: str, subject: str, resumo: str) -> str:
        """Gera resposta COMPLETA usando IA (sem placeholders)"""
        
        # Extrair nome para personalização
        nome = self._extract_name_from_email(email_content[:500])
        saudacao = f"Prezado(a) {nome}," if nome else "Prezado(a),"
        
        # Assinaturas por departamento
        assinaturas = {
            "CURRICULO": "Departamento de Recursos Humanos",
            "FINANCEIRO": "Departamento Financeiro",
            "PHISHING": "Departamento de Segurança da Informação",
            "IMPORTANTE": "Diretoria",
            "PROFISSIONAL": "Departamento Comercial",
            "SPAM": "Sistema de Filtragem Automática",
            "ROTINA": "Atendimento"
        }
        
        assinatura = assinaturas.get(categoria, "Atendimento")
        
        # Prompts específicos para cada categoria - pedindo resposta COMPLETA
        prompts = {
            "CURRICULO": f"""Você é o Departamento de Recursos Humanos. 
            Gere uma resposta PROFISSIONAL e COMPLETA para um candidato que enviou currículo.
            
            INFORMAÇÕES:
            - Assunto do email: {subject}
            - Resumo do conteúdo: {resumo}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Agradeça pelo envio do currículo
            3. Confirme o recebimento
            4. Explique brevemente o processo de análise
            5. Dê um prazo estimado para retorno
            6. Seja motivador e profissional
            7. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA e PRONTA para enviar, incluindo saudação e assinatura:""",

            "FINANCEIRO": f"""Você é o Departamento Financeiro.
            Gere uma resposta COMPLETA para um documento financeiro recebido.
            
            INFORMAÇÕES:
            - Assunto: {subject}
            - Resumo: {resumo}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Confirme recebimento do documento
            3. Informe sobre processamento
            4. Dê prazo estimado de análise
            5. Ofereça canal para dúvidas
            6. Seja claro e objetivo
            7. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA e PRONTA para enviar:""",

            "PHISHING": f"""Você é o Departamento de Segurança da Informação.
            Detectou um email de PHISHING (tentativa de fraude).
            Gere um ALERTA DE SEGURANÇA COMPLETO.
            
            INFORMAÇÕES:
            - Assunto suspeito: {subject}
            - Conteúdo suspeito: {email_content[:400]}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA O ALERTA COMPLETO:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Alerte que é uma TENTATIVA DE FRAUDE
            3. Destaque que este email tem UTILIDADE ZERO para o usuário
            4. Liste recomendações de segurança específicas
            5. Oriente a NÃO clicar em links ou responder
            6. Informe para deletar imediatamente
            7. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere o ALERTA COMPLETO e PRONTO para enviar:""",

            "IMPORTANTE": f"""Você é a Diretoria.
            Gere resposta COMPLETA para email importante/urgente.
            
            INFORMAÇÕES:
            - Assunto: {subject}
            - Resumo: {resumo}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Reconheça a importância do assunto
            3. Confirme atenção prioritária
            4. Dê prazo para retorno detalhado
            5. Seja formal e respeitoso
            6. Transmita seriedade
            7. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA:""",

            "PROFISSIONAL": f"""Você é o Departamento Comercial/Profissional.
            Gere resposta COMPLETA para email profissional.
            
            INFORMAÇÕES:
            - Assunto: {subject}
            - Resumo: {resumo}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Agradeça o contato profissional
            3. Confirme recebimento
            4. Informe sobre análise interna
            5. Dê prazo para retorno
            6. Seja cordial e profissional
            7. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA:""",

            "SPAM": f"""Você é o Sistema de Filtragem.
            Detectou um email de SPAM/PROMOCIONAL.
            Gere uma resposta COMPLETA.
            
            INFORMAÇÕES:
            - Assunto: {subject}
            - UTILIDADE: BAIXA (não solicitado - máximo 5%)
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Informe que foi identificado como material promocional não solicitado
            3. Destaque que tem baixa utilidade (máximo 5%)
            4. Se for relevante para o usuário, pode ser revisado
            5. Se não, pode ser ignorado/deletado
            6. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA:""",

            "ROTINA": f"""Você é o Atendimento Geral.
            Gere resposta COMPLETA para email de rotina.
            
            INFORMAÇÕES:
            - Assunto: {subject}
            - Resumo: {resumo}
            - Saudação a usar: {saudacao}
            - Assinatura a usar: {assinatura}
            
            INSTRUÇÕES PARA A RESPOSTA COMPLETA:
            1. Use exatamente esta saudação: "{saudacao}"
            2. Confirme recebimento da mensagem
            3. Informe sobre processamento
            4. Dê prazo padrão de resposta
            5. Seja educada e profissional
            6. Use exatamente esta assinatura: "Atenciosamente,\n{assinatura}"
            
            Gere a resposta COMPLETA:"""
        }
        
        prompt = prompts.get(categoria, prompts["ROTINA"])
        
        try:
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system", 
                        "content": "Você é um assistente de email corporativo. Gere respostas COMPLETAS, profissionais e PRONTAS para enviar, incluindo saudação e assinatura."
                    },
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 400,
                "temperature": 0.5,
                "top_p": 0.9
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=25
            )
            
            if response.status_code == 200:
                result = response.json()
                resposta_completa = result['choices'][0]['message']['content'].strip()
                
                # Limpar a resposta (remover códigos, placeholders)
                resposta_completa = resposta_completa.replace('```', '').strip()
                
                # Verificar se a resposta está completa
                if saudacao not in resposta_completa:
                    resposta_completa = f"{saudacao}\n\n{resposta_completa}"
                
                if f"Atenciosamente,\n{assinatura}" not in resposta_completa:
                    resposta_completa = f"{resposta_completa}\n\nAtenciosamente,\n{assinatura}"
                
                print(f"🤖 Resposta IA gerada ({categoria}): {resposta_completa[:100]}...")
                return resposta_completa
            else:
                print(f"⚠️  Erro ao gerar resposta: {response.status_code}")
                return self._get_default_response_complete(categoria, saudacao, assinatura)
                
        except Exception as e:
            print(f"❌ Erro na geração de resposta: {e}")
            return self._get_default_response_complete(categoria, saudacao, assinatura)
    
    def _extract_name_from_email(self, email_content: str) -> str:
        """Extrai nome do remetente do conteúdo do email"""
        try:
            padroes = [
                r'[Mm]eu nome é\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'[Mm]e chamo\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'[Ss]ou o\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'[Ss]ou a\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Atenciosamente,\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
            ]
            
            for padrao in padroes:
                match = re.search(padrao, email_content)
                if match:
                    nome = match.group(1).strip()
                    # Verificar se o nome tem pelo menos 2 caracteres
                    if len(nome) >= 2:
                        return nome
            
            return ""
        except:
            return ""
    
    def _get_default_response_complete(self, categoria: str, saudacao: str, assinatura: str) -> str:
        """Resposta padrão completa se a IA falhar"""
        conteudos = {
            "CURRICULO": f"""{saudacao}

Agradecemos o envio do seu currículo. Confirmamos o recebimento e informamos que nossa equipe de Recursos Humanos analisará suas qualificações.

Em caso de compatibilidade com nossas oportunidades, entraremos em contato em até 10 dias úteis.

Atenciosamente,
{assinatura}""",

            "FINANCEIRO": f"""{saudacao}

Confirmamos o recebimento do seu documento financeiro. Nossa equipe está processando a informação e retornará em até 5 dias úteis.

Para dúvidas, entre em contato pelo canal oficial.

Atenciosamente,
{assinatura}""",

            "PHISHING": f"""{saudacao}

🚨 ALERTA DE SEGURANÇA:

Detectamos que este email é uma tentativa de phishing (fraude eletrônica). 

RECOMENDAÇÕES URGENTES:
1. NÃO clique em links ou anexos
2. NÃO responda ao email
3. DELETE imediatamente
4. Verifique sempre diretamente com a instituição oficial

Este email tem UTILIDADE ZERO e representa risco à segurança.

Atenciosamente,
{assinatura}""",

            "IMPORTANTE": f"""{saudacao}

Recebemos sua mensagem importante. Daremos atenção prioritária a este assunto e retornaremos em breve com uma resposta detalhada.

Atenciosamente,
{assinatura}""",

            "PROFISSIONAL": f"""{saudacao}

Agradecemos seu contato profissional. Analisaremos o conteúdo e retornaremos em até 3 dias úteis.

Atenciosamente,
{assinatura}""",

            "SPAM": f"""{saudacao}

Esta mensagem foi identificada como material promocional não solicitado.

UTILIDADE: BAIXA (máximo 5%) - Pode ser ignorado se não for relevante.

Para assuntos comerciais, utilize nossos canais oficiais.

Atenciosamente,
{assinatura}""",

            "ROTINA": f"""{saudacao}

Confirmamos o recebimento da sua mensagem. Retornaremos em breve.

Atenciosamente,
{assinatura}"""
        }
        
        return conteudos.get(categoria, f"{saudacao}\n\nConfirmamos o recebimento da sua mensagem.\n\nAtenciosamente,\n{assinatura}")
    
    def _calculate_utility_base(self, categoria: str) -> float:
        """Utilitário para calcular utilidade base"""
        base_scores = {
            "CURRICULO": 0.92,
            "FINANCEIRO": 0.88,
            "IMPORTANTE": 0.85,
            "PROFISSIONAL": 0.75,
            "PHISHING": 0.0,
            "SPAM": 0.05,
            "ROTINA": 0.45
        }
        return base_scores.get(categoria, 0.5)
    
    def _calculate_utility(self, categoria: str, confianca: float) -> float:
        """Calcula utilidade REAL do email"""
        utilidade_base = self._calculate_utility_base(categoria)
        utilidade_ajustada = utilidade_base * confianca
        
        if categoria == "PHISHING":
            return 0.0
        elif categoria == "SPAM":
            return min(0.05, utilidade_ajustada)
        
        return min(1.0, max(0.0, utilidade_ajustada))
    
    def _generate_tags(self, categoria: str, content: str) -> list:
        """Gera tags relevantes"""
        tags = [categoria.lower(), 'ia_analisado', 'perplexity']
        
        content_lower = content.lower()
        
        if categoria == "CURRICULO":
            tech_keywords = ['python', 'java', 'javascript', 'react', 'node', 
                            'sql', 'django', 'flask', 'aws', 'docker']
            for tech in tech_keywords:
                if tech in content_lower:
                    tags.append(tech)
                    if len(tags) >= 6:
                        break
        
        elif categoria == "PHISHING":
            phishing_tags = ['segurança', 'fraude', 'risco', 'alerta']
            tags.extend(phishing_tags[:3])
        
        elif categoria == "FINANCEIRO":
            finance_tags = ['documento', 'pagamento', 'fiscal']
            tags.extend(finance_tags)
        
        return tags[:6]
    
    def test_connection(self) -> Dict:
        """Testa conexão com a API Perplexity"""
        if not self.is_available:
            return {
                "success": False,
                "message": "API Key não configurada",
                "model": self.model
            }
        
        try:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Teste de conexão - responda apenas OK"}],
                "max_tokens": 5,
                "temperature": 0.1
            }
            
            start = time.time()
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "message": f"Conexão OK ({elapsed:.2f}s)",
                    "model": self.model,
                    "response_time": f"{elapsed:.2f}s"
                }
            else:
                return {
                    "success": False,
                    "message": f"Erro {response.status_code}: {response.text[:100]}",
                    "response_time": f"{elapsed:.2f}s"
                }
                
        except Exception as e:
            return {"success": False, "message": str(e)}