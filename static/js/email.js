// static/js/email.js - VERSÃO ATUALIZADA
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
          // Não processar se clicar no botão de remover (se existir)
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
          
          // Mostrar nome do arquivo selecionado
          showFileSelected(file);
          
          // Feedback visual sutil
          pdfContainer.style.border = '2px solid #28a745';
          setTimeout(() => {
              pdfContainer.style.border = '';
          }, 1000);
      }
      
      function showFileSelected(file) {
          // Remover indicador anterior se existir
          const oldIndicator = document.getElementById('fileSelectedIndicator');
          if (oldIndicator) oldIndicator.remove();
          
          // Criar indicador de arquivo selecionado
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
          
          // Formatar tamanho do arquivo
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
          
          // Evento para remover arquivo
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
          // Prevenir comportamentos padrão
          ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
              pdfContainer.addEventListener(eventName, preventDefaults, false);
          });
          
          function preventDefaults(e) {
              e.preventDefault();
              e.stopPropagation();
          }
          
          // Feedback visual sutil durante drag
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
          
          // Evento de soltar arquivo
          pdfContainer.addEventListener('drop', function(e) {
              const dt = e.dataTransfer;
              const files = dt.files;
              
              if (files.length > 0) {
                  const file = files[0];
                  
                  // Validar antes de processar
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
                  
                  // Atribuir o arquivo ao input
                  const dataTransfer = new DataTransfer();
                  dataTransfer.items.add(file);
                  fileInput.files = dataTransfer.files;
              }
          }, false);
      }
  }
  
  // Função para mostrar notificações temporárias
  function showNotification(message, type = 'info') {
      // Remover notificação anterior se existir
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
      
      // Cor baseada no tipo
      if (type === 'error') {
          notification.style.background = '#dc3545';
      } else if (type === 'success') {
          notification.style.background = '#28a745';
      } else {
          notification.style.background = '#007bff';
      }
      
      notification.textContent = message;
      
      // Adicionar animação
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
      
      // Remover após 3 segundos
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
      
      // Coletar dados
      const emailText = textarea ? textarea.value.trim() : '';
      const fileInput = document.getElementById('fileInput');
      const file = fileInput && fileInput.files.length > 0 ? fileInput.files[0] : null;
      
      // Validação
      if (!emailText && !file) {
          showNotification('Por favor, insira o texto do email ou selecione um arquivo para análise.', 'error');
          return;
      }
      
      // Mostrar loading discreto
      showLoading();
      
      try {
          // Preparar FormData
          const formData = new FormData();
          
          if (emailText) {
              formData.append('email_text', emailText);
          }
          
          if (file) {
              formData.append('file', file);
          }
          
          console.log('Enviando para análise...');
          
          // Enviar para o servidor
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
      // Remover loading anterior se existir
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
      
      // Adicionar animação
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
  
  // MODAL para mostrar resultados - VERSÃO ATUALIZADA
  function showResultsModal(data) {
      // Remover modal anterior se existir
      const oldModal = document.getElementById('resultsModal');
      if (oldModal) {
          oldModal.remove();
      }
      
      // Criar modal
      const modal = document.createElement('div');
      modal.id = 'resultsModal';
      
      // Estilos do modal - usando as cores do body
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
      
      // Conteúdo do modal - usando o mesmo estilo do container original
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
      
      // Extrair dados do NOVO formato
      const isUseful = data.is_useful;
      const analysis = data.analysis || {};
      const response = data.auto_response || '';
      const analysisSource = data.analysis_source || 'local';
      
      // Dados específicos da nova estrutura
      const categoria = analysis.categoria || 'ROTINA';
      const categoriaNome = analysis.categoria_nome || analysis.categoria || 'Rotina';
      const categoriaEmoji = analysis.categoria_emoji || '📋';
      const utilidade = analysis.utilidade || 0.5;
      const utilidadePercent = Math.round(utilidade * 100);
      const departamento = analysis.departamento || 'Sistema';
      const prioridade = analysis.prioridade || 'BAIXA';
      const acaoNecessaria = analysis.acao_necessaria || false;
      const confiancaIA = analysis.confianca_ia || 0.5;
      const tags = analysis.tags || [];
      
      // Cor baseado na categoria (usando cores do tema)
      const categoriaCores = {
          'CURRICULO': 'rgb(124, 58, 237)',    // Roxo
          'FINANCEIRO': 'rgb(0, 140, 255)',    // Azul
          'IMPORTANTE': 'rgb(255, 193, 7)',    // Amarelo
          'PROFISSIONAL': 'rgb(25, 135, 84)',  // Verde
          'SPAM': 'rgb(108, 117, 125)',        // Cinza
          'ROTINA': 'rgb(13, 110, 253)'        // Azul claro
      };
      
      const categoriaCor = categoriaCores[categoria] || 'rgb(133, 57, 255)';
      
      // Cor baseado na utilidade
      let usefulnessColor = 'rgb(236, 72, 153)'; // Rosa
      if (utilidadePercent > 70) usefulnessColor = categoriaCor;
      else if (utilidadePercent > 40) usefulnessColor = 'rgb(0, 140, 255)'; // Azul
      
      // Cor da prioridade
      const prioridadeCores = {
          'ALTA': 'rgb(220, 53, 69)',
          'MÉDIA': 'rgb(255, 193, 7)',
          'BAIXA': 'rgb(108, 117, 125)'
      };
      const prioridadeCor = prioridadeCores[prioridade] || 'rgb(108, 117, 125)';
      
      // Texto da fonte da análise
      let fonteTexto = '';
      let fonteIcon = '';
      let fonteCor = '';
      
      if (analysisSource === 'ia_real' || analysis.fonte === 'huggingface_ia') {
          fonteTexto =' Análise por IA';
          fonteCor = 'rgb(124, 58, 237)';
      } else if (analysisSource === 'ia_demo' || analysis.fonte === 'ia_semantica_demo') {
          fonteTexto = '🎯 IA de Demonstração';
          fonteIcon = '🎯';
          fonteCor = 'rgb(0, 140, 255)';
      } else if (analysis.fonte === 'analise_contextual') {
          fonteTexto = '🔍 Análise Contextual';
          fonteIcon = '🔍';
          fonteCor = 'rgb(25, 135, 84)';
      } else {
          fonteTexto = '⚡ Análise Inteligente';
          fonteIcon = '⚡';
          fonteCor = 'rgb(255, 193, 7)';
      }
      
      // Gerar HTML do conteúdo ATUALIZADO
      modalContent.innerHTML = `
          <!-- Cabeçalho do modal -->
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
          
          <!-- Indicador de utilidade -->
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
                  ${isUseful ? '✅ Email Relevante' : '⚠️ Precisa de Análise Manual'}
                  ${confiancaIA ? ` (Confiança: ${Math.round(confiancaIA * 100)}%)` : ''}
              </div>
          </div>
          
          <!-- Grid de informações -->
          <div style="
              display: grid;
              grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
              gap: 20px;
              margin-bottom: 25px;
          ">
              <!-- Categoria -->
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
              
              <!-- Ação Necessária -->
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
              
              <!-- Prioridade -->
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
                      ${prioridade === 'ALTA' ? '🔴' : prioridade === 'MÉDIA' ? '🟡' : '⚪'}
                  </div>
                  <div style="
                      font-size: 22px;
                      font-weight: bold;
                      color: ${prioridadeCor};
                  ">
                      ${prioridade}
                  </div>
              </div>
              
              <!-- Departamento -->
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
          
          <!-- Resumo -->
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
                  ${analysis.resumo || 'Não disponível'}
              </div>
          </div>
          
          <!-- Tags -->
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
          
          <!-- Protocolo e Informações -->
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
                      ${analysis.protocolo || 'N/A'}
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
          
          <!-- Resposta Sugerida -->
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
              
              <div style="
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
                  ${response.replace(/\n/g, '<br>')}
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
      
      // Adicionar animações CSS
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
      
      // Adicionar ao modal
      modal.appendChild(modalContent);
      
      // Adicionar ao body
      document.body.appendChild(modal);
      
      // Configurar eventos dos botões
      const closeBtn = document.getElementById('closeModalBtn');
      const copyBtn = document.getElementById('copyResponseBtn');
      const newAnalysisBtn = document.getElementById('newAnalysisBtn');
      
      if (closeBtn) {
          closeBtn.addEventListener('click', closeModal);
      }
      
      // Fechar modal ao clicar fora do conteúdo
      modal.addEventListener('click', function(e) {
          if (e.target === modal) {
              closeModal();
          }
      });
      
      // Fechar com ESC
      document.addEventListener('keydown', function(e) {
          if (e.key === 'Escape') {
              closeModal();
          }
      });
      
      if (copyBtn) {
          copyBtn.addEventListener('click', function() {
              navigator.clipboard.writeText(response).then(() => {
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
      }
      
      if (newAnalysisBtn) {
          newAnalysisBtn.addEventListener('click', function() {
              closeModal();
              clearForm();
          });
      }
      
      // Função para fechar modal
      function closeModal() {
          modal.style.animation = 'fadeOut 0.3s ease';
          modalContent.style.animation = 'slideDown 0.3s ease';
          
          // Adicionar animações de saída
          const fadeOutCSS = document.createElement('style');
          fadeOutCSS.textContent = `
              @keyframes fadeOut {
                  from { opacity: 1; }
                  to { opacity: 0; }
              }
              
              @keyframes slideDown {
                  from { transform: translateY(0); opacity: 1; }
                  to { transform: translateY(30px); opacity: 0; }
              }
          `;
          document.head.appendChild(fadeOutCSS);
          
          setTimeout(() => {
              if (modal.parentNode) {
                  modal.remove();
              }
          }, 300);
      }
  }
  
  // Função para limpar formulário
  function clearForm() {
      // Limpar textarea
      if (textarea) {
          textarea.value = '';
      }
      
      // Limpar arquivo selecionado
      const fileInput = document.getElementById('fileInput');
      if (fileInput) {
          fileInput.value = '';
      }
      
      // Remover indicador de arquivo selecionado
      const fileIndicator = document.getElementById('fileSelectedIndicator');
      if (fileIndicator) {
          fileIndicator.remove();
      }
      
      // Focar no textarea para nova análise
      if (textarea) {
          textarea.focus();
      }
      
      showNotification('Formulário limpo. Pronto para nova análise!', 'success');
  }
});