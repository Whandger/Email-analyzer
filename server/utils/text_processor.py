# utils/text_processor.py
import re
import string
import unicodedata
from typing import List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
import spacy
from collections import Counter
import os

class TextPreprocessor:
    def __init__(self, language='portuguese'):
        """Inicializa pré-processador para português"""
        self.language = language
        
        # Verificar e baixar recursos NLTK se necessário
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("📥 Baixando recursos NLTK...")
            nltk.download('stopwords', quiet=True)
            nltk.download('rslp', quiet=True)
            nltk.download('punkt', quiet=True)
        
        # Inicializar recursos
        self.stop_words = set(stopwords.words('portuguese'))
        self.stemmer = RSLPStemmer()
        
        # Adicionar stop words específicas de email
        email_stopwords = {
            'att', 'attach', 'attachment', 'anexo', 'anexado', 'encaminhado', 
            'forwarded', 're:', 'fw:', 'de:', 'para:', 'assunto:', 'subject:',
            'from:', 'to:', 'date:', 'data:', 'enviado', 'sent', 'message',
            'mensagem', 'email', 'e-mail', 'dear', 'caro', 'prezado', 'cordiais',
            'atenciosamente', 'sinceramente', 'grato', 'obrigado', 'obrigada',
            'cumprimentos', 'saudações', 'regards', 'best', 'thanks', 'thank'
        }
        self.stop_words.update(email_stopwords)
        
        # Carregar spaCy para lematização (se disponível)
        self.nlp = None
        try:
            import spacy
            # Tentar carregar modelo português
            try:
                self.nlp = spacy.load("pt_core_news_sm")
                print("✅ spaCy para português carregado")
            except:
                # Se modelo português não disponível, usar inglês e desabilitar lematização
                print("⚠️ spaCy português não disponível. Usando stemming.")
                self.nlp = None
        except ImportError:
            print("ℹ️ spaCy não instalado. Usando NLTK para pré-processamento.")
            self.nlp = None
    
    def clean_text(self, text: str, remove_html: bool = True) -> str:
        """Limpeza completa do texto"""
        if not text:
            return ""
        
        # Converter para string se necessário
        text = str(text)
        
        # Remover HTML tags
        if remove_html:
            text = re.sub(r'<[^>]+>', '', text)
        
        # Remover URLs
        text = re.sub(r'https?://\S+|www\.\S+', '[URL]', text)
        
        # Remover endereços de email
        text = re.sub(r'\S+@\S+', '[EMAIL]', text)
        
        # Remover números de telefone
        text = re.sub(r'\(?\d{2,3}\)?[\s-]?\d{4,5}[\s-]?\d{4}', '[TELEFONE]', text)
        
        # Remover caracteres especiais mas manter pontuação básica
        text = re.sub(r'[^\w\s.,!?;:()\-\[\]{}"\']', ' ', text)
        
        # Normalizar espaços
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """Normalização do texto (acentos, caixa, etc.)"""
        # Remover acentos
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        
        # Converter para minúsculas
        text = text.lower()
        
        # Remover números isolados (mas manter números em palavras)
        text = re.sub(r'\b\d+\b', '', text)
        
        return text
    
    def tokenize(self, text: str, remove_stopwords: bool = True) -> List[str]:
        """Tokeniza o texto"""
        # Limpar e normalizar primeiro
        text = self.clean_text(text)
        text = self.normalize_text(text)
        
        # Tokenização simples (pode ser melhorada com nltk.word_tokenize)
        tokens = text.split()
        
        if remove_stopwords:
            tokens = [token for token in tokens if token not in self.stop_words and len(token) > 2]
        
        return tokens
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Aplica stemming aos tokens"""
        return [self.stemmer.stem(token) for token in tokens if token]
    
    def lemmatize_text(self, text: str) -> str:
        """Aplica lematização usando spaCy se disponível"""
        if self.nlp:
            doc = self.nlp(text)
            lemmas = [token.lemma_ for token in doc if not token.is_stop and len(token.text) > 2]
            return " ".join(lemmas)
        else:
            # Fallback para stemming
            tokens = self.tokenize(text, remove_stopwords=True)
            stemmed = self.stem_tokens(tokens)
            return " ".join(stemmed)
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extrai palavras-chave mais frequentes"""
        tokens = self.tokenize(text, remove_stopwords=True)
        
        # Filtrar tokens por comprimento e conteúdo
        filtered_tokens = [
            token for token in tokens 
            if len(token) > 3 and token.isalpha()
        ]
        
        # Contar frequência
        freq_dist = Counter(filtered_tokens)
        
        # Retornar as top_n mais frequentes
        return [word for word, _ in freq_dist.most_common(top_n)]
    
    def preprocess_for_classification(self, text: str) -> str:
        """Pré-processamento otimizado para classificação"""
        # Pipeline completo
        cleaned = self.clean_text(text)
        normalized = self.normalize_text(cleaned)
        lemmatized = self.lemmatize_text(normalized)
        
        return lemmatized
    
    def preprocess_for_summarization(self, text: str) -> str:
        """Pré-processamento otimizado para sumarização"""
        # Manter mais estrutura para sumarização
        cleaned = self.clean_text(text, remove_html=True)
        normalized = self.normalize_text(cleaned)
        
        # Não lematizar/stemming para sumarização (preserva significado)
        return normalized
    
    def get_email_metadata(self, text: str) -> dict:
        """Extrai metadados úteis de emails"""
        metadata = {
            'has_attachments': False,
            'has_links': False,
            'has_dates': False,
            'has_numbers': False,
            'word_count': 0,
            'sentence_count': 0
        }
        
        # Verificar anexos
        attachment_keywords = ['anexo', 'attachment', 'attach', 'encaminhado', 'forward']
        if any(keyword in text.lower() for keyword in attachment_keywords):
            metadata['has_attachments'] = True
        
        # Verificar links
        if re.search(r'https?://|www\.', text):
            metadata['has_links'] = True
        
        # Verificar datas
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{2,4}',
            r'\d{1,2}-\d{1,2}-\d{2,4}',
            r'\d{1,2} de [a-z]+ de \d{4}'
        ]
        for pattern in date_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                metadata['has_dates'] = True
                break
        
        # Verificar números
        if re.search(r'\b\d+\b', text):
            metadata['has_numbers'] = True
        
        # Contar palavras e sentenças
        words = self.tokenize(text, remove_stopwords=False)
        metadata['word_count'] = len(words)
        
        sentences = re.split(r'[.!?]+', text)
        metadata['sentence_count'] = len([s for s in sentences if s.strip()])
        
        return metadata