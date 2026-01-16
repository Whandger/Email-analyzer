# utils/file_handler.py - VERSÃO CORRIGIDA

import os
import re
import PyPDF2
from typing import Optional, Tuple
import pdfplumber  # ADICIONAR ESTE IMPORT
from server.utils.text_processor import TextPreprocessor

class FileHandler:
    def __init__(self):
        """Inicializa FileHandler com pré-processador"""
        self.text_processor = TextPreprocessor(language='portuguese')
    
    @staticmethod
    def extract_text_from_file(file_path: str, preprocess: bool = True) -> str:
        """
        Extrai texto de arquivos PDF ou TXT - VERSÃO CORRIGIDA
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.pdf':
            raw_text = FileHandler._read_pdf_robust(file_path) 
        elif ext == '.txt':
            raw_text = FileHandler._read_txt(file_path)
        else:
            raise ValueError(f"Formato não suportado: {ext}")
        
        print(f"📄 Texto extraído: {len(raw_text)} caracteres")
        
        # Aplicar pré-processamento se solicitado
        if preprocess and raw_text:
            processor = TextPreprocessor(language='portuguese')
            # Pré-processar para extração de texto
            processed_text = processor.clean_text(raw_text)
            processed_text = processor.normalize_text(processed_text)
            return processed_text
        
        return raw_text
    
    @staticmethod
    def _read_pdf_robust(file_path: str) -> str:
        """Lê texto de arquivo PDF com MÚLTIPLAS TENTATIVAS"""
        text = ""
        
        # TENTATIVA 1: pdfplumber (mais robusto)
        try:
            import pdfplumber
            print("🔄 Tentando extrair PDF com pdfplumber...")
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            text += page_text + "\n\n"
                            print(f"   📄 Página {page_num}: {len(page_text)} caracteres")
                    except Exception as e:
                        print(f"   ⚠️ Erro página {page_num}: {e}")
                        continue
        except ImportError:
            print("⚠️ pdfplumber não instalado. Instale com: pip install pdfplumber")
        except Exception as e:
            print(f"⚠️ Erro pdfplumber: {e}")
        
        # Se pdfplumber extraiu texto, usar
        if text.strip() and len(text.strip()) > 100:
            print(f"✅ pdfplumber extraiu {len(text)} caracteres")
            return text
        
        # TENTATIVA 2: PyPDF2 (fallback)
        print("🔄 Tentando extrair PDF com PyPDF2...")
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                print(f"📄 PDF tem {len(reader.pages)} páginas")
                
                for page_num, page in enumerate(reader.pages, 1):
                    try:
                        page_text = page.extract_text()
                        if page_text and page_text.strip():
                            cleaned = FileHandler._clean_pdf_text(page_text)
                            text += cleaned + "\n\n"
                            print(f"   📄 Página {page_num}: {len(page_text)} caracteres")
                    except Exception as e:
                        print(f"   ⚠️ Erro página {page_num}: {e}")
                        continue
        except Exception as e:
            print(f"⚠️ Erro PyPDF2: {e}")
        
        # Se ainda não tem texto, tentar OCR básico
        if not text.strip() or len(text.strip()) < 50:
            print("⚠️ Pouco texto extraído. Tentando abordagem alternativa...")
            text = FileHandler._try_alternative_extraction(file_path)
        
        return text.strip()
    
    @staticmethod
    def _clean_pdf_text(text: str) -> str:
        """Limpa texto extraído do PDF"""
        # Remover múltiplos espaços e quebras de linha desnecessárias
        text = re.sub(r'\s+', ' ', text)
        
        # Remover caracteres de controle
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Corrigir quebras de palavras (hífens no final da linha)
        text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
        
        return text.strip()
    
    @staticmethod
    def _try_alternative_extraction(file_path: str) -> str:
        """Tenta extração alternativa de PDF"""
        try:
            # Tenta usar pdftotext se disponível
            import subprocess
            import tempfile
            
            temp_txt = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_txt_path = temp_txt.name
            temp_txt.close()
            
            # Usar pdftotext do sistema (se instalado)
            result = subprocess.run(
                ['pdftotext', file_path, temp_txt_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and os.path.exists(temp_txt_path):
                with open(temp_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                os.remove(temp_txt_path)
                
                if text.strip():
                    print(f"✅ pdftotext extraiu {len(text)} caracteres")
                    return text
        except Exception as e:
            print(f"⚠️ Falha na extração alternativa: {e}")
        
        return "[PDF - texto não pôde ser extraído automaticamente. Tente copiar o texto manualmente.]"
    
    @staticmethod
    def _read_txt(file_path: str) -> str:
        """Lê texto de arquivo TXT com múltiplas tentativas de encoding"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-8-sig']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                    if content.strip():
                        print(f"✅ TXT lido com encoding: {encoding}")
                        return content
            except UnicodeDecodeError:
                continue
            except Exception as e:
                print(f"⚠️ Erro com encoding {encoding}: {e}")
                continue
        
        # Última tentativa: modo binário com chardet
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                import chardet
                result = chardet.detect(content)
                encoding = result['encoding'] if result['encoding'] else 'latin-1'
                return content.decode(encoding, errors='ignore')
        except Exception as e:
            raise Exception(f"Erro ao ler TXT: {str(e)}")