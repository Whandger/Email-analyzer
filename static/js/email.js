// static/js/email.js - VERSÃO FINAL CORRIGIDA
document.addEventListener('DOMContentLoaded', function() {
    console.log('Script de análise de email carregado');
    
    // Elementos do DOM
    const emailForm = document.getElementById('form');
    const textarea = document.getElementById('text');
    const analyzeBtn = document.getElementById('button');
    const pdfContainer = document.getElementById('Pdf_container');
    
    if (!emailForm || !analyzeBtn || !pdfContainer) {
        console.error('Elementos do formulário não encontrados!');
        return;
    }
    
    // Inicializar upload de arquivo na Pdf_container existente
    initFileUpload();
    
    // Configurar eventos
    analyzeBtn.addEventListener('click', handleSubmit);
    
    // Adicionar também ao formulário para capturar Enter
    emailForm.addEventListener('submit', function(e) {
        e.preventDefault();
        handleSubmit(e);
    });
    
    function initFileUpload() {
        // Criar input de arquivo escondido
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.id = 'fileInput';
        fileInput.accept = '.pdf,.txt';
        fileInput.style.display = 'none';
        
        // Adicionar à página
        document.body.appendChild(fileInput);
        
        // Adicionar indicador visual discreto à Pdf_container
        const uploadIndicator = document.createElement('div');
        uploadIndicator.id = 'uploadIndicator';
        uploadIndicator.style.cssText = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: #007bff;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        `;
        uploadIndicator.innerHTML = '📎';
        pdfContainer.style.position = 'relative';
        pdfContainer.appendChild(uploadIndicator);
        
        // Adicionar cursor pointer e efeito hover
        pdfContainer.style.cursor = 'pointer';
        pdfContainer.style.transition = 'background-color 0.3s';
        
        // Manter o conteúdo HTML original, apenas adicionar funcionalidade
        const originalContent = pdfContainer.innerHTML;
        
        pdfContainer.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(0, 123, 255, 0.05)';
            uploadIndicator.style.opacity = '1';
        });
        
        pdfContainer.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
            uploadIndicator.style.opacity = '0';
        });
        
        // Evento: Clicar na área
        pdfContainer.addEventListener('click', function(e) {
            if (!e.target.closest('#removeFileBtn')) {
                fileInput.click();
            }
        });
        
        // Evento: Arquivo selecionado
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFileSelection(this.files[0]);
            }
        });
        
        // Configurar Drag & Drop sutil
        setupDragAndDrop();
        
        function handleFileSelection(file) {
            // Validar tamanho (10MB)
            if (file.size > 10 * 1024 * 1024) {
                showNotification('Arquivo muito grande! Tamanho máximo: 10MB.', 'error');
                return;
            }
            
            // Validar extensão
            const ext = file.name.split('.').pop().toLowerCase();
            if (!['pdf', 'txt'].includes(ext)) {
                showNotification('Formato não suportado! Use apenas PDF ou TXT.', 'error');
                return;
            }
            
            showFileSelected(file);
            
            pdfContainer.style.border = '2px solid #28a745';
            setTimeout(() => {
                pdfContainer.style.border = '';
            }, 1000);
        }
        
        function showFileSelected(file) {
            const oldIndicator = document.getElementById('fileSelectedIndicator');
            if (oldIndicator) oldIndicator.remove();
            
            const fileIndicator = document.createElement('div');
            fileIndicator.id = 'fileSelectedIndicator';
            fileIndicator.style.cssText = `
                position: absolute;
                bottom: 10px;
                right: 10px;
                background: rgba(40, 167, 69, 0.9);
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 12px;
                max-width: 80%;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                display: flex;
                align-items: center;
                gap: 5px;
            `;
            
            const sizeInMB = (file.size / (1024 * 1024)).toFixed(2);
            
            fileIndicator.innerHTML = `
                <span>📄</span>
                <span>${file.name}</span>
                <span style="font-size: 10px; opacity: 0.8;">(${sizeInMB} MB)</span>
                <button id="removeFileBtn" type="button" style="
                    background: none;
                    border: none;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                    padding: 0 5px;
                    line-height: 1;
                ">×</button>
            `;
            
            pdfContainer.appendChild(fileIndicator);
            
            document.getElementById('removeFileBtn').addEventListener('click', function(e) {
                e.stopPropagation();
                fileInput.value = '';
                fileIndicator.remove();
                pdfContainer.style.border = '2px solid #dc3545';
                setTimeout(() => {
                    pdfContainer.style.border = '';
                }, 500);
            });
        }
        
        function setupDragAndDrop() {
            ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
                pdfContainer.addEventListener(eventName, preventDefaults, false);
            });
            
            function preventDefaults(e) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            ['dragenter', 'dragover'].forEach(eventName => {
                pdfContainer.addEventListener(eventName, function() {
                    this.style.border = '2px dashed #007bff';
                    this.style.backgroundColor = 'rgba(0, 123, 255, 0.1)';
                }, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                pdfContainer.addEventListener(eventName, function() {
                    this.style.border = '';
                    this.style.backgroundColor = '';
                }, false);
            });
            
            pdfContainer.addEventListener('drop', function(e) {
                const dt = e.dataTransfer;
                const files = dt.files;
                
                if (files.length > 0) {
                    const file = files[0];
                    const ext = file.name.split('.').pop().toLowerCase();
                    
                    if (!['pdf', 'txt'].includes(ext)) {
                        showNotification('Formato não suportado! Use apenas PDF ou TXT.', 'error');
                        return;
                    }
                    
                    if (file.size > 10 * 1024 * 1024) {
                        showNotification('Arquivo muito grande! Tamanho máximo: 10MB.', 'error');
                        return;
                    }
                    
                    handleFileSelection(file);
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    fileInput.files = dataTransfer.files;
                }
            }, false);
        }
    }
    
    function showNotification(message, type = 'info') {
        const oldNotification = document.getElementById('tempNotification');
        if (oldNotification) oldNotification.remove();
        
        const notification = document.createElement('div');
        notification.id = 'tempNotification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 5px;
            color: white;
            font-size: 14px;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
        `;
        
        if (type === 'error') {
            notification.style.background = '#dc3545';
        } else if (type === 'success') {
            notification.style.background = '#28a745';
        } else {
            notification.style.background = '#007bff';
        }
        
        notification.textContent = message;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }, 3000);
    }
    
    async function handleSubmit(event) {
        event.preventDefault();
        
        console.log('Iniciando análise de email...');
        
        const emailText = textarea ? textarea.value.trim() : '';
        const fileInput = document.getElementById('fileInput');
        const file = fileInput && fileInput.files.length > 0 ? fileInput.files[0] : null;
        
        if (!emailText && !file) {
            showNotification('Por favor, insira o texto do email ou selecione um arquivo para análise.', 'error');
            return;
        }
        
        showLoading();
        
        try {
            const formData = new FormData();
            
            if (emailText) {
                formData.append('email_text', emailText);
            }
            
            if (file) {
                formData.append('file', file);
            }
            
            console.log('Enviando para análise...');
            
            const response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `Erro ${response.status}`);
            }
            
            console.log('Análise recebida:', data);
            showResultsModal(data);
            showNotification('Análise concluída com sucesso!', 'success');
            
        } catch (error) {
            console.error('Erro na análise:', error);
            showNotification('Erro: ' + error.message, 'error');
        } finally {
            hideLoading();
        }
    }
    
    function showLoading() {
        hideLoading();
        
        const loadingDiv = document.createElement('div');
        loadingDiv.id = 'loadingIndicator';
        loadingDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            z-index: 9998;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        `;
        
        const style = document.createElement('style');
        style.textContent = `
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(loadingDiv);
    }
    
    function hideLoading() {
        const loadingDiv = document.getElementById('loadingIndicator');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }
    
    function showResultsModal(data) {
        const oldModal = document.getElementById('resultsModal');
        if (oldModal) oldModal.remove();
        
        const modal = document.createElement('div');
        modal.id = 'resultsModal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-color: rgba(0, 0, 0, 0.85);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeIn 0.3s ease;
        `;
        
        const modalContent = document.createElement('div');
        modalContent.style.cssText = `
            background-color: rgb(0, 0, 0);
            width: 90%;
            max-width: 1000px;
            max-height: 90vh;
            border-radius: 10px;
            padding: 30px;
            overflow-y: auto;
            position: relative;
            box-shadow: 0 0 30px rgba(140, 80, 255, 0.8);
            border: 2px solid rgb(133, 57, 255);
            animation: slideUp 0.3s ease;
        `;
        
        // ✅ CORREÇÃO CRÍTICA: Extração de dados corrigida
        const analysis = data.analysis || {};
        const autoResponse = data.auto_response || '';
        
        console.log('🔍 DEBUG - Dados recebidos:', data);
        console.log('📊 Análise object:', analysis);
        console.log('✉️ Auto Response:', autoResponse);
        
        // ✅ CORREÇÃO: Utilidade correta (evita usar 0.5 quando utilidade é 0)
        const utilidade = analysis.utilidade !== undefined ? analysis.utilidade : 0.5;
        const utilidadePercent = Math.round(utilidade * 100);
        
        console.log(`📈 Utilidade calculada: ${utilidade} (${utilidadePercent}%)`);
        
        const categoria = analysis.categoria || 'ROTINA';
        const categoriaNome = analysis.categoria_nome || getCategoriaNome(categoria);
        const categoriaEmoji = analysis.categoria_emoji || getCategoriaEmoji(categoria);
        
        const confiancaIA = analysis.confianca_ia || 0.5;
        const confiancaPercent = Math.round(confiancaIA * 100);
        
        const resumo = analysis.resumo || 'Análise concluída.';
        const acaoNecessaria = analysis.acao_necessaria || false;
        const prioridade = analysis.prioridade || getPrioridade(categoria, utilidade);
        const departamento = analysis.departamento || getDepartamento(categoria);
        const tags = analysis.tags || [];
        
        // ✅ CORREÇÃO: Resposta com prioridade correta
        let resposta = autoResponse || analysis.resposta_completa || analysis.resposta || '';
        
        // Verificar se resposta está incompleta ou tem placeholders
        if (!resposta.trim() || resposta.includes('{conteudo}') || resposta.includes('{assinatura}')) {
            console.warn('⚠️ Resposta incompleta detectada, usando fallback');
            resposta = gerarRespostaFallback(categoria, utilidadePercent);
        }
        
        const protocolo = analysis.protocolo || 'PPX-' + Math.floor(Math.random() * 100000);
        const fonte = data.analysis_source || analysis.fonte || 'perplexity_ia';
        
        function getCategoriaNome(cat) {
            const nomes = {
                'CURRICULO': 'Currículo',
                'FINANCEIRO': 'Financeiro',
                'IMPORTANTE': 'Importante',
                'PROFISSIONAL': 'Profissional',
                'PHISHING': 'Phishing',
                'SPAM': 'Spam',
                'ROTINA': 'Rotina'
            };
            return nomes[cat] || cat;
        }
        
        function getCategoriaEmoji(cat) {
            const emojis = {
                'CURRICULO': '📄',
                'FINANCEIRO': '💰',
                'IMPORTANTE': '⚠️',
                'PROFISSIONAL': '🤝',
                'PHISHING': '🚫',
                'SPAM': '📧',
                'ROTINA': '📋'
            };
            return emojis[cat] || '📋';
        }
        
        function getDepartamento(cat) {
            const departamentos = {
                'CURRICULO': 'Recursos Humanos',
                'FINANCEIRO': 'Financeiro',
                'IMPORTANTE': 'Diretoria',
                'PROFISSIONAL': 'Comercial',
                'PHISHING': 'Segurança',
                'SPAM': 'Sistema',
                'ROTINA': 'Atendimento'
            };
            return departamentos[cat] || 'Sistema';
        }
        
        function getPrioridade(cat, util) {
            if (cat === 'PHISHING') return 'CRÍTICA';
            if (cat === 'IMPORTANTE') return 'ALTA';
            if (cat === 'FINANCEIRO' || cat === 'CURRICULO') return 'MÉDIA';
            if (util < 0.1) return 'BAIXA';
            return 'MÉDIA';
        }
        
        function gerarRespostaFallback(categoria, utilidadePercent) {
            const dataAtual = new Date().toLocaleDateString('pt-BR');
            const horaAtual = new Date().toLocaleTimeString('pt-BR');
            
            const respostasFallback = {
                'CURRICULO': `Prezado(a),

Confirmamos o recebimento do seu currículo. Nossa equipe de Recursos Humanos analisará suas qualificações e retornará em breve.

Utilidade da mensagem: ${utilidadePercent}%
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Departamento de Recursos Humanos`,

                'FINANCEIRO': `Prezado(a),

Recebemos seu documento financeiro. Nossa equipe processará a informação e retornará em breve.

Utilidade da mensagem: ${utilidadePercent}%
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Departamento Financeiro`,

                'PHISHING': `Prezado(a),

⚠️ ALERTA DE SEGURANÇA

Detectamos que este email é uma tentativa de phishing (fraude eletrônica). 

RECOMENDAÇÕES URGENTES:
1. NÃO clique em links ou anexos
2. NÃO responda ao email
3. DELETE imediatamente
4. Verifique sempre diretamente com a instituição oficial

Utilidade da mensagem: 0% (fraude)
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Departamento de Segurança da Informação`,

                'IMPORTANTE': `Prezado(a),

Recebemos sua mensagem importante. Daremos atenção prioritária a este assunto e retornaremos em breve.

Utilidade da mensagem: ${utilidadePercent}%
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Diretoria`,

                'PROFISSIONAL': `Prezado(a),

Agradecemos seu contato profissional. Analisaremos o conteúdo e retornaremos em breve.

Utilidade da mensagem: ${utilidadePercent}%
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Departamento Comercial`,

                'SPAM': `Prezado(a),

Esta mensagem foi identificada como material promocional não solicitado.

Utilidade: BAIXA (${utilidadePercent}%) - Pode ser ignorado se não for relevante.

Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Sistema de Filtragem Automática`,

                'ROTINA': `Prezado(a),

Confirmamos o recebimento da sua mensagem. Retornaremos em breve.

Utilidade da mensagem: ${utilidadePercent}%
Data: ${dataAtual} ${horaAtual}

Atenciosamente,
Atendimento`
            };
            
            return respostasFallback[categoria] || respostasFallback['ROTINA'];
        }
        
        let fonteTexto = '';
        let fonteIcon = '';
        let fonteCor = '';
        
        if (fonte === 'perplexity_ia') {
            fonteTexto = 'Perplexity IA';
            fonteIcon = '🤖';
            fonteCor = 'rgb(124, 58, 237)';
        } else if (fonte === 'huggingface_ia') {
            fonteTexto = 'Hugging Face IA';
            fonteIcon = '🧠';
            fonteCor = 'rgb(0, 140, 255)';
        } else if (fonte === 'fallback_nlp') {
            fonteTexto = 'Análise NLP';
            fonteIcon = '🔍';
            fonteCor = 'rgb(25, 135, 84)';
        } else {
            fonteTexto = 'Sistema Inteligente';
            fonteIcon = '⚡';
            fonteCor = 'rgb(255, 193, 7)';
        }
        
        const categoriaCores = {
            'CURRICULO': 'rgb(124, 58, 237)',
            'FINANCEIRO': 'rgb(0, 140, 255)',
            'IMPORTANTE': 'rgb(255, 193, 7)',
            'PROFISSIONAL': 'rgb(25, 135, 84)',
            'PHISHING': 'rgb(220, 53, 69)',
            'SPAM': 'rgb(108, 117, 125)',
            'ROTINA': 'rgb(13, 110, 253)'
        };
        
        const categoriaCor = categoriaCores[categoria] || 'rgb(133, 57, 255)';
        
        // ✅ CORREÇÃO: Cor da utilidade baseada no valor REAL
        let usefulnessColor = 'rgb(236, 72, 153)';
        if (utilidadePercent >= 70) usefulnessColor = categoriaCor;
        else if (utilidadePercent >= 40) usefulnessColor = 'rgb(0, 140, 255)';
        else if (utilidadePercent > 0) usefulnessColor = 'rgb(108, 117, 125)';
        else usefulnessColor = 'rgb(220, 53, 69)';
        
        const prioridadeCores = {
            'CRÍTICA': 'rgb(220, 53, 69)',
            'ALTA': 'rgb(255, 193, 7)',
            'MÉDIA': 'rgb(13, 110, 253)',
            'BAIXA': 'rgb(108, 117, 125)'
        };
        const prioridadeCor = prioridadeCores[prioridade] || 'rgb(108, 117, 125)';
        
        const protocoloFinal = protocolo;
        
        // ✅ CORREÇÃO: Mensagem de relevância baseada no valor REAL da utilidade
        let relevanciaMsg = '';
        if (utilidadePercent >= 70) {
            relevanciaMsg = '✅ Email Relevante';
        } else if (utilidadePercent >= 40) {
            relevanciaMsg = '⚠️ Email de Rotina';
        } else if (utilidadePercent > 0) {
            relevanciaMsg = '📩 Email de Baixa Relevância';
        } else {
            relevanciaMsg = '🚫 Email Perigoso/Inútil';
        }
        
        modalContent.innerHTML = `
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 25px;
                border-bottom: 2px solid rgb(85, 85, 85);
                padding-bottom: 15px;
            ">
                <div>
                    <h1 style="
                        color: rgb(133, 57, 255);
                        font-size: 2.2rem;
                        margin: 0;
                        margin-bottom: 5px;
                    ">
                        Resultados da Análise
                    </h1>
                    <div style="
                        font-size: 14px;
                        color: ${fonteCor};
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    ">
                        <span>${fonteIcon}</span>
                        <span>${fonteTexto}</span>
                    </div>
                </div>
                
                <button id="closeModalBtn" style="
                    background: none;
                    border: none;
                    color: rgb(216, 216, 216);
                    font-size: 28px;
                    cursor: pointer;
                    padding: 0;
                    line-height: 1;
                    transition: color 0.3s;
                ">
                    ×
                </button>
            </div>
            
            <div style="text-align: center; margin-bottom: 25px;">
                <div style="
                    display: inline-block;
                    padding: 12px 35px;
                    background: ${usefulnessColor};
                    color: aliceblue;
                    border-radius: 25px;
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    box-shadow: 0 0 20px ${usefulnessColor}80;
                    animation: pulse 2s infinite;
                ">
                    ${utilidadePercent}% Útil
                </div>
                
                <div style="font-size: 18px; color: rgb(216, 216, 216); margin-bottom: 10px;">
                    ${relevanciaMsg} (Confiança: ${confiancaPercent}%)
                </div>
            </div>
            
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-bottom: 25px;
            ">
                <div style="
                    padding: 20px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    border-left: 4px solid ${categoriaCor};
                    text-align: center;
                ">
                    <div style="font-size: 14px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        CATEGORIA
                    </div>
                    <div style="
                        font-size: 48px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: ${categoriaCor};
                    ">
                        ${categoriaEmoji}
                    </div>
                    <div style="
                        font-size: 18px;
                        font-weight: bold;
                        color: rgb(216, 216, 216);
                        text-transform: uppercase;
                    ">
                        ${categoriaNome}
                    </div>
                </div>
                
                <div style="
                    padding: 20px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    border-left: 4px solid ${acaoNecessaria ? 'rgb(236, 72, 153)' : 'rgb(0, 140, 255)'};
                    text-align: center;
                ">
                    <div style="font-size: 14px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        AÇÃO NECESSÁRIA
                    </div>
                    <div style="
                        font-size: 48px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: ${acaoNecessaria ? 'rgb(236, 72, 153)' : 'rgb(0, 140, 255)'};
                    ">
                        ${acaoNecessaria ? '⚠️' : '✅'}
                    </div>
                    <div style="
                        font-size: 22px;
                        font-weight: bold;
                        color: ${acaoNecessaria ? 'rgb(236, 72, 153)' : 'rgb(0, 140, 255)'};
                    ">
                        ${acaoNecessaria ? 'SIM' : 'NÃO'}
                    </div>
                </div>
                
                <div style="
                    padding: 20px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    border-left: 4px solid ${prioridadeCor};
                    text-align: center;
                ">
                    <div style="font-size: 14px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        PRIORIDADE
                    </div>
                    <div style="
                        font-size: 48px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: ${prioridadeCor};
                    ">
                        ${prioridade === 'CRÍTICA' ? '🔴' : prioridade === 'ALTA' ? '🟡' : prioridade === 'MÉDIA' ? '🔵' : '⚪'}
                    </div>
                    <div style="
                        font-size: 22px;
                        font-weight: bold;
                        color: ${prioridadeCor};
                    ">
                        ${prioridade}
                    </div>
                </div>
                
                <div style="
                    padding: 20px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    border-left: 4px solid rgb(133, 57, 255);
                    text-align: center;
                ">
                    <div style="font-size: 14px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        DEPARTAMENTO
                    </div>
                    <div style="
                        font-size: 48px;
                        font-weight: bold;
                        margin-bottom: 10px;
                        color: rgb(133, 57, 255);
                    ">
                        🏢
                    </div>
                    <div style="
                        font-size: 18px;
                        font-weight: bold;
                        color: rgb(216, 216, 216);
                    ">
                        ${departamento}
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 25px;">
                <div style="
                    font-size: 16px;
                    color: rgb(133, 57, 255);
                    margin-bottom: 10px;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                ">
                    <span>📋</span>
                    <span>RESUMO DA ANÁLISE</span>
                </div>
                <div style="
                    padding: 20px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    color: rgb(215, 215, 215);
                    font-size: 16px;
                    line-height: 1.6;
                    border: 1px solid rgb(85, 85, 85);
                ">
                    ${resumo}
                </div>
            </div>
            
            ${tags.length > 0 ? `
                <div style="margin-bottom: 25px;">
                    <div style="
                        font-size: 16px;
                        color: rgb(133, 57, 255);
                        margin-bottom: 10px;
                        font-weight: bold;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    ">
                        <span>🏷️</span>
                        <span>TAGS IDENTIFICADAS</span>
                    </div>
                    <div style="
                        display: flex;
                        flex-wrap: wrap;
                        gap: 12px;
                        padding: 20px;
                        background: rgb(21, 21, 21);
                        border-radius: 10px;
                        border: 1px solid rgb(85, 85, 85);
                    ">
                        ${tags.map(tag => `
                            <span style="
                                padding: 8px 16px;
                                background: linear-gradient(135deg, ${categoriaCor}, rgb(133, 57, 255));
                                color: white;
                                border-radius: 20px;
                                font-size: 14px;
                                font-weight: bold;
                                box-shadow: 0 2px 10px ${categoriaCor}80;
                            ">
                                ${tag}
                            </span>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 25px;
                padding: 15px;
                background: rgb(21, 21, 21);
                border-radius: 10px;
                border: 1px solid rgb(85, 85, 85);
            ">
                <div>
                    <div style="font-size: 12px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        PROTOCOLO
                    </div>
                    <div style="font-size: 18px; color: rgb(216, 216, 216); font-family: monospace;">
                        ${protocoloFinal}
                    </div>
                </div>
                
                <div style="text-align: right;">
                    <div style="font-size: 12px; color: rgb(170, 170, 170); margin-bottom: 5px;">
                        DATA DA ANÁLISE
                    </div>
                    <div style="font-size: 16px; color: rgb(216, 216, 216);">
                        ${new Date().toLocaleDateString('pt-BR')} ${new Date().toLocaleTimeString('pt-BR')}
                    </div>
                </div>
            </div>
            
            <div>
                <div style="
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 15px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid rgb(85, 85, 85);
                ">
                    <div style="
                        font-size: 18px;
                        color: rgb(133, 57, 255);
                        font-weight: bold;
                        display: flex;
                        align-items: center;
                        gap: 10px;
                    ">
                        <span>✉️</span>
                        <span>RESPOSTA SUGERIDA</span>
                    </div>
                    
                    <div style="display: flex; gap: 10px;">
                        <button id="copyResponseBtn" style="
                            padding: 10px 20px;
                            background: linear-gradient(135deg, rgb(0, 140, 255), rgb(124, 58, 237));
                            color: aliceblue;
                            border: none;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 14px;
                            font-weight: bold;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                            transition: transform 0.2s;
                        ">
                            <span>📋</span>
                            <span>Copiar Resposta</span>
                        </button>
                        
                        <button id="newAnalysisBtn" style="
                            padding: 10px 20px;
                            background: linear-gradient(135deg, rgb(236, 72, 153), rgb(124, 58, 237));
                            color: aliceblue;
                            border: none;
                            border-radius: 8px;
                            cursor: pointer;
                            font-size: 14px;
                            font-weight: bold;
                            display: flex;
                            align-items: center;
                            gap: 8px;
                            transition: transform 0.2s;
                        ">
                            <span>🔄</span>
                            <span>Nova Análise</span>
                        </button>
                    </div>
                </div>
                
                <div id="responseContent" style="
                    padding: 25px;
                    background: rgb(21, 21, 21);
                    border-radius: 10px;
                    color: rgb(215, 215, 215);
                    font-family: 'Courier New', monospace;
                    white-space: pre-wrap;
                    line-height: 1.6;
                    max-height: 300px;
                    overflow-y: auto;
                    border: 1px solid rgb(85, 85, 85);
                    font-size: 15px;
                ">
                    ${resposta.replace(/\n/g, '<br>')}
                </div>
                
                <div style="
                    margin-top: 15px;
                    font-size: 12px;
                    color: rgb(170, 170, 170);
                    text-align: center;
                    font-style: italic;
                ">
                    Resposta automática gerada pela IA. Ajuste conforme necessário antes de enviar.
                </div>
            </div>
        `;
        
        const animationsCSS = document.createElement('style');
        animationsCSS.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            @keyframes pulse {
                0% { box-shadow: 0 0 20px ${usefulnessColor}80; }
                50% { box-shadow: 0 0 30px ${usefulnessColor}; }
                100% { box-shadow: 0 0 20px ${usefulnessColor}80; }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            
            @keyframes slideDown {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(30px); opacity: 0; }
            }
            
            #copyResponseBtn:hover, #newAnalysisBtn:hover {
                transform: translateY(-2px);
            }
            
            #closeModalBtn:hover {
                color: rgb(236, 72, 153);
            }
            
            ::-webkit-scrollbar {
                width: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: rgb(21, 21, 21);
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, rgb(124, 58, 237), rgb(133, 57, 255));
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, rgb(133, 57, 255), rgb(236, 72, 153));
            }
        `;
        document.head.appendChild(animationsCSS);
        
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
        
        const closeBtn = document.getElementById('closeModalBtn');
        const copyBtn = document.getElementById('copyResponseBtn');
        const newAnalysisBtn = document.getElementById('newAnalysisBtn');
        const responseContent = document.getElementById('responseContent');
        
        if (!resposta.trim()) {
            if (responseContent) {
                responseContent.innerHTML = '<em style="color: rgb(170,170,170);">Nenhuma resposta sugerida disponível.</em>';
            }
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', closeModal);
        }
        
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeModal();
            }
        });
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
        
        if (copyBtn && resposta.trim()) {
            copyBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(resposta).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<span>✓</span><span>Copiado!</span>';
                    this.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.style.background = 'linear-gradient(135deg, rgb(0, 140, 255), rgb(124, 58, 237))';
                    }, 2000);
                }).catch(err => {
                    console.error('Erro ao copiar:', err);
                    showNotification('Não foi possível copiar para a área de transferência.', 'error');
                });
            });
        } else if (copyBtn) {
            copyBtn.disabled = true;
            copyBtn.style.opacity = '0.5';
            copyBtn.style.cursor = 'not-allowed';
        }
        
        if (newAnalysisBtn) {
            newAnalysisBtn.addEventListener('click', function() {
                closeModal();
                clearForm();
            });
        }
        
        function closeModal() {
            modal.style.animation = 'fadeOut 0.3s ease';
            modalContent.style.animation = 'slideDown 0.3s ease';
            
            setTimeout(() => {
                if (modal.parentNode) {
                    modal.remove();
                }
            }, 300);
        }
    }
    
    function clearForm() {
        if (textarea) {
            textarea.value = '';
        }
        
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.value = '';
        }
        
        const fileIndicator = document.getElementById('fileSelectedIndicator');
        if (fileIndicator) {
            fileIndicator.remove();
        }
        
        if (textarea) {
            textarea.focus();
        }
        
        showNotification('Formulário limpo. Pronto para nova análise!', 'success');
    }
});