# ==============================
# KEYWORDS – CLASSIFICAÇÃO DE DOCUMENTOS / EMAILS
# ==============================

# ------------------------------
# PHISHING / FRAUDE (ALTA PRIORIDADE - BLOQUEAR PRIMEIRO)
# ------------------------------
PHISHING_KEYWORDS = [
    # URGÊNCIA FALSA (muito forte)
    'urgente', 'imediatamente', 'agora mesmo',
    'prazo de 24 horas', 'prazo 24h', 'última chance',
    'ação necessária', 'ação imediata', 'tempo limitado',
    
    # AMEAÇAS DE BLOQUEIO (muito forte)
    'sua conta foi', 'conta comprometida',
    'bloqueada', 'suspensa', 'encerrada',
    'risco de fechamento', 'cancelamento definitivo',
    'perda de acesso', 'acesso revogado',
    
    # SOLICITAÇÕES DE CLIQUE (forte)
    'clique aqui', 'clique no link',
    'clique para verificar', 'clique para confirmar',
    'link seguro', 'acesse o link',
    
    # VERIFICAÇÃO DE DADOS (forte)
    'verificar suas informações',
    'atualizar dados', 'confirmar identidade',
    'validar conta', 'ativar conta',
    'reenviar senha', 'resetar senha',
    
    # TERMOS BANCÁRIOS SUSPEITOS
    'suporte bancário', 'central segurança',
    'departamento fraude', 'atividade suspeita',
    'transação não autorizada', 'tentativa acesso',
    'segurança da conta', 'proteção conta',
    
    # DOMÍNIOS/EMAILS FALSOS
    'banco-seguro', 'security-bank',
    'atualizacao-conta', 'verificacao-online',
    'central-cliente', 'suporte-online',
    
    # OUTROS INDICADORES
    '!!!', 'urgentíssimo', 'importantíssimo',
    'confidencial', 'restrito',
]

PHISHING_PATTERNS = [
    # Padrões de frase completas (muito forte)
    'sua conta foi comprometida',
    'sua conta foi bloqueada',
    'clique aqui para verificar',
    'ação necessária imediata',
    'prazo de 24 horas',
    'última chance de acesso',
    
    # Padrões com variáveis
    'sua conta.*foi.*bloqueada',
    '.*conta.*comprometida.*',
    '.*clique.*aqui.*verificar.*',
    '.*ação.*necessária.*',
    '.*prazo.*24.*horas.*',
    '.*última.*chance.*',
]

# ------------------------------
# SPAM / PROMOÇÕES - VERSÃO ATUALIZADA
# ------------------------------
SPAM_KEYWORDS = [
    # Promoções comerciais
    'promoção', 'promocao', 'desconto', 'oferta', 'oferta imperdível',
    'black friday', 'cyber monday', 'cashback', 'grátis', 'gratuito',
    'cupom', 'cupom de desconto', 'código promocional',
    
    # Urgência falsa comercial
    'apenas hoje', 'por tempo limitado', 'última chance',
    'não perca essa chance', 'vagas limitadas',
    'oferta por tempo limitado', 'promoção relâmpago',
    
    # Chamadas de ação comerciais
    'clique aqui', 'garantir seu desconto', 'compre agora',
    'adquira já', 'faça sua inscrição',
    
    # Termos de marketing
    'marketing', 'newsletter', 'mailing', 'lista de emails',
    'distribuição', 'comercial', 'vendas',
    
    # Estruturas típicas de spam
    'não quer mais receber', 'clique aqui para cancelar',
    'esta é uma mensagem automática',
    
    # Preços e descontos
    'de r$', 'por apenas r$', '12x de', 'parcelamento',
]

# ------------------------------
# IMPORTANTE - VERSÃO ATUALIZADA (mais restrita)
# ------------------------------
IMPORTANT_KEYWORDS = [
    # Termos de negócios REAIS (não promocionais)
    'projeto', 'projetos', 'reunião', 'reuniao',
    'relatório', 'relatorio', 'contrato', 'contratos',
    'proposta comercial', 'proposta técnica',
    'cliente', 'clientes', 'parceria', 'parcerias',
    'prazo de entrega', 'cronograma', 'planejamento',
    'estratégia', 'estrategia', 'gestão', 'gestao',
    'compliance', 'auditoria', 'legal', 'jurídico',
    
    # Urgência REAL (não falsa)
    'urgente', 'prioridade máxima', 'crítico',
    'atenção imediata', 'ação necessária',
]

# ------------------------------
# EDUCAÇÃO/TECNOLOGIA (para contexto adicional)
# ------------------------------
EDUCATION_KEYWORDS = [
    'curso', 'cursos', 'treinamento', 'capacitação',
    'workshop', 'webinar', 'aula', 'módulo',
    'certificado', 'certificação', 'diploma',
    'aprendizado', 'ensino', 'educação',
]

# ------------------------------
# FINANCEIRO (PRIORIDADE MÁXIMA) - VERSÃO REFINADA
# ------------------------------
FINANCIAL_KEYWORDS = [
    # Documentos fiscais específicos
    'nota fiscal', 'nf', 'nfe', 'nf-e', 'danfe',
    'fatura', 'faturas', 'boleto', 'boletos',
    'recibo fiscal', 'comprovante de pagamento',
    
    # Campos específicos de documentos
    'chave de acesso nfe', 'protocolo autorização',
    'número série', 'modelo', 'série',
    'data emissão', 'valor total documento',
    
    # Termos contábeis/documentais
    'demonstração financeira', 'balanço patrimonial',
    'dre', 'demonstração resultado',
    'livro caixa', 'conciliação bancária',
    
    # Impostos específicos
    'icms', 'ipi', 'iss', 'pis', 'cofins',
    
    # Identificadores
    'cnpj', 'cpf', 'inscrição estadual',
    
    # Removidos por serem muito genéricos:
    # 'valor', 'valores', 'total', 'subtotal' (aparecem em spam)
    # 'banco', 'agência', 'conta' (aparecem em phishing)
]

# ------------------------------
# CURRÍCULO (INDICADORES FORTES)
# ------------------------------
RESUME_INDICATORS = [
    # TÍTULOS
    'currículo', 'curriculo', 'curriculum vitae', 'cv', 'resume',

    # SEÇÕES CLÁSSICAS
    'objetivo profissional',
    'resumo profissional',
    'perfil profissional',
    'experiência profissional', 'experiencia profissional',
    'formação acadêmica', 'formacao academica',
    'habilidades técnicas', 'habilidades tecnicas',
    'competências profissionais',
    'histórico profissional', 'historico profissional',

    # EXPERIÊNCIA
    'empregos anteriores',
    'cargos anteriores',
    'responsabilidades',
    'atribuições',
    'realizações', 'conquistas',

    # FORMAÇÃO
    'graduação', 'graduacao',
    'pós-graduação', 'pos-graduacao',
    'especialização', 'especializacao',
    'mestrado', 'doutorado',

    # IDIOMAS E CURSOS
    'idiomas',
    'cursos complementares',
    'certificações', 'certificacoes',

    # LINKS PROFISSIONAIS (EM CONTEXTO)
    'linkedin profissional',
    'github profissional',
    'portfolio profissional'
]

# ------------------------------
# PROFISSIONAL (RH / VAGAS)
# ------------------------------
PROFESSIONAL_KEYWORDS = [
    'vaga', 'vagas', 'emprego', 'empregos',
    'oportunidade de trabalho',
    'processo seletivo',
    'recrutamento', 'seleção', 'selecao',
    'entrevista', 'entrevistas',
    'contratação', 'contratacao',
    'admissão', 'admissao',
    'estágio', 'estagio',
    'trainee', 'jovem aprendiz',

    'carreira', 'crescimento profissional',
    'desenvolvimento profissional',
    'time', 'equipe',
    'cargo', 'função', 'funcao',

    'proposta de trabalho',
    'oferta de emprego',
    'regime de trabalho',
    'clt', 'pj', 'freelancer',
    'presencial', 'remoto', 'híbrido', 'hibrido'
]

# ------------------------------
# TECNOLOGIAS (PARA TAGS)
# ------------------------------
TECH_KEYWORDS = {
    'python': ['python'],
    'javascript': ['javascript', 'js'],
    'typescript': ['typescript', 'ts'],
    'html': ['html', 'html5'],
    'css': ['css', 'css3'],
    'react': ['react', 'reactjs'],
    'nextjs': ['next', 'nextjs'],
    'flask': ['flask'],
    'django': ['django'],
    'node': ['node', 'nodejs'],
    'mysql': ['mysql'],
    'postgresql': ['postgresql', 'postgres'],
    'mongodb': ['mongodb', 'mongo'],
    'git': ['git', 'github'],
    'docker': ['docker'],
    'aws': ['aws', 'amazon web services'],
    'tailwind': ['tailwind', 'tailwindcss']
}

# ------------------------------
# ÁREAS PROFISSIONAIS
# ------------------------------
PROFESSIONAL_AREAS = {
    'backend': ['backend', 'back-end', 'api', 'servidor'],
    'frontend': ['frontend', 'front-end', 'ui', 'ux'],
    'fullstack': ['fullstack', 'full stack'],
    'data': ['dados', 'data', 'analytics', 'machine learning'],
    'devops': ['devops', 'infraestrutura', 'ci/cd'],
    'mobile': ['mobile', 'android', 'ios'],
    'qa': ['qa', 'qualidade', 'testes', 'testing'],
    'security': ['segurança', 'security', 'cybersecurity']
}

# ------------------------------
# PALAVRAS GENÉRICAS (evitar falsos positivos)
# ------------------------------
GENERIC_WORDS_TO_AVOID = [
    'importante',  # Muito genérico, aparece em spam
    'valor',       # Aparece em spam ("valor do curso")
    'total',       # Aparece em spam ("total a pagar")
    'oportunidade', # Pode ser spam ("oportunidade única")
    'sucesso',     # Muito usado em marketing
    'excelente',   # Muito usado em marketing
    'melhor',      # Muito usado em marketing
]