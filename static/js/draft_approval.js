// Dados reais vindos da API
let draftsData = [];
let scheduledData = [];
let approvedData = [];
let rejectedData = [];

// Função para carregar dados reais da API
async function loadRealData() {
    try {
        showNotification('Carregando posts reais...', 'info');
        
        // Buscar posts da API
        const response = await fetch('/api/social/posts?limit=100');
        const data = await response.json();
        
        if (data.success && data.posts) {
            // Separar posts por status
            draftsData = data.posts.filter(p => p.status === 'rascunho' || p.status === 'pendente');
            scheduledData = data.posts.filter(p => p.status === 'agendado');
            approvedData = data.posts.filter(p => p.status === 'aprovado');
            rejectedData = data.posts.filter(p => p.status === 'rejeitado');
            
            showNotification(`${data.posts.length} posts carregados do banco de dados`, 'success');
        } else {
            showNotification('Nenhum post encontrado no banco de dados', 'warning');
        }
    } catch (error) {
        console.error('Erro ao carregar posts:', error);
        showNotification('Erro ao carregar posts reais. Usando dados locais.', 'danger');
    }
}



let mediaLibraryData = [
    {
        id: 1,
        type: "audio",
        title: "Voz Demo - Alex Professional",
        url: "https://example.com/audio/alex-demo.mp3",
        duration: "2:30",
        size: "3.2 MB"
    },
    {
        id: 2,
        type: "video",
        title: "Tutorial Completo",
        url: "https://example.com/video/tutorial.mp4",
        duration: "15:45",
        size: "125 MB"
    },
    {
        id: 3,
        type: "audio",
        title: "Voz Demo - Maria Amigável",
        url: "https://example.com/audio/maria-demo.mp3",
        duration: "1:45",
        size: "2.1 MB"
    }
];

let currentSchedulingId = null;

// Inicialização
document.addEventListener('DOMContentLoaded', async function() {
    // Carregar dados reais da API primeiro
    await loadRealData();
    
    // Depois renderizar a interface
    renderDrafts();
    renderScheduled();
    renderApproved();
    renderRejected();
    renderMediaLibrary();
    updateTabCounts();
});

// Renderizar rascunhos
function renderDrafts() {
    const container = document.getElementById('draftsContent');
    container.innerHTML = '';
    
    draftsData.forEach(draft => {
        const card = createDraftCard(draft);
        container.appendChild(card);
    });
}

// Renderizar programados
function renderScheduled() {
    const container = document.getElementById('scheduledContent');
    container.innerHTML = '';
    
    scheduledData.forEach(item => {
        const card = createScheduledCard(item);
        container.appendChild(card);
    });
}

// Renderizar aprovados
function renderApproved() {
    const container = document.getElementById('approvedContent');
    container.innerHTML = '';
    
    approvedData.forEach(item => {
        const card = createApprovedCard(item);
        container.appendChild(card);
    });
}

// Renderizar rejeitados
function renderRejected() {
    const container = document.getElementById('rejectedContent');
    container.innerHTML = '';
    
    rejectedData.forEach(item => {
        const card = createRejectedCard(item);
        container.appendChild(card);
    });
}

// Renderizar biblioteca de mídia
function renderMediaLibrary() {
    const container = document.getElementById('mediaLibrary');
    container.innerHTML = '';
    
    mediaLibraryData.forEach(media => {
        const card = createMediaCard(media);
        container.appendChild(card);
    });
}

// Criar card de rascunho
function createDraftCard(draft) {
    const card = document.createElement('div');
    card.className = 'draft-card';
    card.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <img src="${draft.image}" alt="${draft.title}" class="img-fluid rounded" style="cursor: pointer;" onclick="makeEditable(this, 'image')">
            </div>
            <div class="col-md-8">
                <h4 class="editable-text" onclick="makeEditable(this, 'title')" data-original="${draft.title}">${draft.title}</h4>
                <p class="editable-text" onclick="makeEditable(this, 'caption')" data-original="${draft.caption}">${draft.caption}</p>
                <div class="d-flex flex-wrap gap-2 mb-2">
                    ${draft.hashtags.map(tag => `<span class="badge bg-secondary">${tag}</span>`).join('')}
                </div>
                <small class="text-muted">Criado em: ${new Date(draft.createdAt).toLocaleString('pt-BR')}</small>
                
                <div class="action-buttons">
                    <button class="btn btn-approve btn-sm" onclick="approveAndPublish(${draft.id})">
                        <i class="fas fa-check me-1"></i>Aprovar e Publicar
                    </button>
                    <button class="btn btn-reject btn-sm" onclick="showRejectReason(${draft.id})">
                        <i class="fas fa-times me-1"></i>Rejeitar
                    </button>
                    <button class="btn btn-schedule btn-sm" onclick="openScheduleModal(${draft.id})">
                        <i class="fas fa-calendar-alt me-1"></i>Agendar
                    </button>
                </div>
                
                <div class="reject-reason" id="rejectReason-${draft.id}">
                    <div class="mt-2">
                        <textarea class="form-control" placeholder="Motivo da rejeição..." rows="2"></textarea>
                        <div class="mt-2">
                            <button class="btn btn-danger btn-sm" onclick="confirmReject(${draft.id})">
                                <i class="fas fa-times me-1"></i>Confirmar Rejeição
                            </button>
                            <button class="btn btn-secondary btn-sm" onclick="hideRejectReason(${draft.id})">
                                <i class="fas fa-undo me-1"></i>Cancelar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    return card;
}

// Criar card de programado
function createScheduledCard(item) {
    const card = document.createElement('div');
    card.className = 'draft-card';
    card.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <img src="${item.image}" alt="${item.title}" class="img-fluid rounded">
            </div>
            <div class="col-md-8">
                <h4>${item.title}</h4>
                <p>${item.caption}</p>
                <div class="d-flex flex-wrap gap-2 mb-2">
                    ${item.hashtags.map(tag => `<span class="badge bg-secondary">${tag}</span>`).join('')}
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="status-badge status-scheduled">
                        <i class="fas fa-clock me-1"></i>Agendado
                    </span>
                    <small class="text-muted">
                        <i class="fas fa-calendar-alt me-1"></i>
                        ${new Date(item.scheduledAt).toLocaleString('pt-BR')}
                    </small>
                </div>
                <div class="action-buttons">
                    <button class="btn btn-primary btn-sm" onclick="publishNow(${item.id})">
                        <i class="fas fa-rocket me-1"></i>Publicar Agora
                    </button>
                    <button class="btn btn-warning btn-sm" onclick="cancelSchedule(${item.id})">
                        <i class="fas fa-times me-1"></i>Cancelar Agendamento
                    </button>
                </div>
            </div>
        </div>
    `;
    return card;
}

// Criar card de aprovado
function createApprovedCard(item) {
    const card = document.createElement('div');
    card.className = 'draft-card';
    card.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <img src="${item.image}" alt="${item.title}" class="img-fluid rounded">
            </div>
            <div class="col-md-8">
                <h4>${item.title}</h4>
                <p>${item.caption}</p>
                <div class="d-flex flex-wrap gap-2 mb-2">
                    ${item.hashtags.map(tag => `<span class="badge bg-secondary">${tag}</span>`).join('')}
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="status-badge status-approved">
                        <i class="fas fa-check-circle me-1"></i>Aprovado
                    </span>
                    <small class="text-muted">
                        <i class="fas fa-check me-1"></i>
                        Aprovado em: ${new Date(item.approvedAt).toLocaleString('pt-BR')}
                    </small>
                </div>
            </div>
        </div>
    `;
    return card;
}

// Criar card de rejeitado
function createRejectedCard(item) {
    const card = document.createElement('div');
    card.className = 'draft-card';
    card.innerHTML = `
        <div class="row">
            <div class="col-md-4">
                <img src="${item.image}" alt="${item.title}" class="img-fluid rounded">
            </div>
            <div class="col-md-8">
                <h4>${item.title}</h4>
                <p>${item.caption}</p>
                <div class="d-flex flex-wrap gap-2 mb-2">
                    ${item.hashtags.map(tag => `<span class="badge bg-secondary">${tag}</span>`).join('')}
                </div>
                <div class="d-flex align-items-center gap-3">
                    <span class="status-badge status-rejected">
                        <i class="fas fa-times-circle me-1"></i>Rejeitado
                    </span>
                    <small class="text-muted">
                        <i class="fas fa-times me-1"></i>
                        Rejeitado em: ${new Date(item.rejectedAt).toLocaleString('pt-BR')}
                    </small>
                </div>
                <div class="alert alert-danger mt-2">
                    <strong>Motivo:</strong> ${item.rejectReason}
                </div>
            </div>
        </div>
    `;
    return card;
}

// Criar card de mídia
function createMediaCard(media) {
    const card = document.createElement('div');
    card.className = 'media-card';
    const icon = media.type === 'audio' ? 'fa-music' : 'fa-video';
    card.innerHTML = `
        <button class="ai-suggestor-btn" onclick="openCaptionSuggestor(${media.id})" title="Gerar legendas com IA">
            <i class="fas fa-magic"></i>
        </button>
        <div class="row">
            <div class="col-md-2">
                <div class="text-center">
                    <i class="fas ${icon} fa-3x mb-2"></i>
                </div>
            </div>
            <div class="col-md-10">
                <h5>${media.title}</h5>
                <div class="d-flex gap-3 text-muted small">
                    <span><i class="fas fa-clock me-1"></i>${media.duration}</span>
                    <span><i class="fas fa-file me-1"></i>${media.size}</span>
                    <span><i class="fas fa-tag me-1"></i>${media.type.toUpperCase()}</span>
                </div>
                <div class="mt-2">
                    <button class="btn btn-sm btn-outline-light" onclick="playMedia('${media.url}')">
                        <i class="fas fa-play me-1"></i>Reproduzir
                    </button>
                    <button class="btn btn-sm btn-outline-light" onclick="downloadMedia('${media.url}')">
                        <i class="fas fa-download me-1"></i>Baixar
                    </button>
                </div>
            </div>
        </div>
        <div class="caption-suggestor" id="captionSuggestor-${media.id}" style="display: none;">
            <h6><i class="fas fa-magic me-2"></i>Legendas Sugeridas por IA</h6>
            <div id="captionOptions-${media.id}">
                <!-- Opções de legenda serão inseridas aqui -->
            </div>
        </div>
    `;
    return card;
}

// Funções de edição inline
function makeEditable(element, type) {
    if (element.classList.contains('editing')) return;
    
    const originalText = element.textContent;
    element.classList.add('editing');
    
    if (type === 'image') {
        // Para imagens, mostrar input de URL
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'form-control';
        input.value = element.src;
        input.style.width = '100%';
        
        element.parentNode.replaceChild(input, element);
        input.focus();
        input.select();
        
        const saveEdit = () => {
            const newSrc = input.value;
            const newImg = document.createElement('img');
            newImg.src = newSrc;
            newImg.alt = 'Imagem do post';
            newImg.className = 'img-fluid rounded';
            newImg.style.cursor = 'pointer';
            newImg.onclick = () => makeEditable(newImg, 'image');
            
            input.parentNode.replaceChild(newImg, input);
        };
        
        input.addEventListener('blur', saveEdit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') saveEdit();
        });
    } else {
        // Para texto
        const input = document.createElement('textarea');
        input.className = 'form-control';
        input.value = originalText;
        input.rows = type === 'title' ? 1 : 3;
        input.style.width = '100%';
        
        element.parentNode.replaceChild(input, element);
        input.focus();
        input.select();
        
        const saveEdit = () => {
            const newText = input.value;
            const newElement = document.createElement(type === 'title' ? 'h4' : 'p');
            newElement.className = 'editable-text';
            newElement.textContent = newText;
            newElement.onclick = () => makeEditable(newElement, type);
            newElement.setAttribute('data-original', originalText);
            
            input.parentNode.replaceChild(newElement, input);
        };
        
        input.addEventListener('blur', saveEdit);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey && type === 'title') {
                e.preventDefault();
                saveEdit();
            }
        });
    }
}

// Funções de aprovação e rejeição
function approveAndPublish(draftId) {
    const draft = draftsData.find(d => d.id === draftId);
    if (!draft) return;
    
    // Mover para aprovados
    draft.status = 'approved';
    draft.approvedAt = new Date().toISOString();
    approvedData.push(draft);
    
    // Remover dos rascunhos
    draftsData = draftsData.filter(d => d.id !== draftId);
    
    // Atualizar interface
    renderDrafts();
    renderApproved();
    updateTabCounts();
    
    // Mostrar notificação
    showNotification('Post aprovado e publicado com sucesso!', 'success');
}

function showRejectReason(draftId) {
    const reasonDiv = document.getElementById(`rejectReason-${draftId}`);
    reasonDiv.style.display = 'block';
}

function hideRejectReason(draftId) {
    const reasonDiv = document.getElementById(`rejectReason-${draftId}`);
    reasonDiv.style.display = 'none';
}

function confirmReject(draftId) {
    const reasonDiv = document.getElementById(`rejectReason-${draftId}`);
    const textarea = reasonDiv.querySelector('textarea');
    const reason = textarea.value.trim();
    
    if (!reason) {
        showNotification('Por favor, informe o motivo da rejeição', 'warning');
        return;
    }
    
    const draft = draftsData.find(d => d.id === draftId);
    if (!draft) return;
    
    // Mover para rejeitados
    draft.status = 'rejected';
    draft.rejectedAt = new Date().toISOString();
    draft.rejectReason = reason;
    rejectedData.push(draft);
    
    // Remover dos rascunhos
    draftsData = draftsData.filter(d => d.id !== draftId);
    
    // Atualizar interface
    renderDrafts();
    renderRejected();
    updateTabCounts();
    
    showNotification('Post rejeitado com sucesso', 'danger');
}

// Funções de agendamento
function openScheduleModal(draftId) {
    currentSchedulingId = draftId;
    const draft = draftsData.find(d => d.id === draftId);
    if (!draft) return;
    
    const modal = document.getElementById('scheduleModal');
    const preview = document.getElementById('schedulePreview');
    const datetimeInput = document.getElementById('scheduleDateTime');
    
    // Configurar data/hora mínima como agora
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    datetimeInput.min = now.toISOString().slice(0, 16);
    
    // Mostrar preview do post
    preview.innerHTML = `
        <h6>${draft.title}</h6>
        <p class="mb-0">${draft.caption}</p>
    `;
    
    modal.style.display = 'flex';
}

function closeScheduleModal() {
    const modal = document.getElementById('scheduleModal');
    modal.style.display = 'none';
    currentSchedulingId = null;
}

function confirmSchedule() {
    const datetimeInput = document.getElementById('scheduleDateTime');
    const scheduledAt = datetimeInput.value;
    
    if (!scheduledAt) {
        showNotification('Por favor, selecione uma data e hora', 'warning');
        return;
    }
    
    const draft = draftsData.find(d => d.id === currentSchedulingId);
    if (!draft) return;
    
    // Mover para programados
    draft.status = 'scheduled';
    draft.scheduledAt = scheduledAt;
    scheduledData.push(draft);
    
    // Remover dos rascunhos
    draftsData = draftsData.filter(d => d.id !== currentSchedulingId);
    
    // Atualizar interface
    renderDrafts();
    renderScheduled();
    updateTabCounts();
    
    closeScheduleModal();
    showNotification('Post agendado com sucesso!', 'info');
}

function publishNow(itemId) {
    const item = scheduledData.find(i => i.id === itemId);
    if (!item) return;
    
    // Mover para aprovados
    item.status = 'approved';
    item.approvedAt = new Date().toISOString();
    delete item.scheduledAt;
    approvedData.push(item);
    
    // Remover dos programados
    scheduledData = scheduledData.filter(i => i.id !== itemId);
    
    // Atualizar interface
    renderScheduled();
    renderApproved();
    updateTabCounts();
    
    showNotification('Post publicado com sucesso!', 'success');
}

function cancelSchedule(itemId) {
    const item = scheduledData.find(i => i.id === itemId);
    if (!item) return;
    
    // Mover de volta para rascunhos
    item.status = 'draft';
    delete item.scheduledAt;
    draftsData.push(item);
    
    // Remover dos programados
    scheduledData = scheduledData.filter(i => i.id !== itemId);
    
    // Atualizar interface
    renderDrafts();
    renderScheduled();
    updateTabCounts();
    
    showNotification('Agendamento cancelado', 'warning');
}

// Funções do CaptionSuggestor
function openCaptionSuggestor(mediaId) {
    const suggestorDiv = document.getElementById(`captionSuggestor-${mediaId}`);
    const optionsDiv = document.getElementById(`captionOptions-${mediaId}`);
    
    if (suggestorDiv.style.display === 'none') {
        // Gerar opções de legenda
        const captions = generateAICaptions();
        optionsDiv.innerHTML = captions.map((caption, index) => `
            <div class="caption-option">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <strong>${caption.type}</strong>
                    <span class="badge bg-info">${caption.style}</span>
                </div>
                <p class="mb-2">${caption.text}</p>
                <div class="d-flex flex-wrap gap-1 mb-2">
                    ${caption.hashtags.map(tag => `<small class="badge bg-secondary">${tag}</small>`).join('')}
                </div>
                <div class="copy-buttons">
                    <button class="copy-btn" onclick="copyText('${caption.text}')">
                        <i class="fas fa-copy me-1"></i>Copiar Legenda
                    </button>
                    <button class="copy-btn" onclick="copyText('${caption.hashtags.join(' ')}')">
                        <i class="fas fa-hashtag me-1"></i>Copiar Hashtags
                    </button>
                    <button class="copy-btn" onclick="copyText('${caption.text}\\n\\n${caption.hashtags.join(' ')}')">
                        <i class="fas fa-copy me-1"></i>Copiar Tudo
                    </button>
                </div>
            </div>
        `).join('');
        
        suggestorDiv.style.display = 'block';
    } else {
        suggestorDiv.style.display = 'none';
    }
}

function generateAICaptions() {
    return [
        {
            type: "Engajadora",
            style: "Dinâmica",
            text: "Transforme sua comunicação com vozes IA realistas! Nosso sistema revoluciona a forma como você cria conteúdo em áudio. Experimente agora e surpreenda seu público! ",
            hashtags: ["#Inovação", "#VozesIA", "#Tecnologia", "#Comunicação", "#Futuro"]
        },
        {
            type: "Curta",
            style: "Direta",
            text: "Vozes IA realistas para seus projetos. Rápido, fácil e profissional. Comece hoje mesmo!",
            hashtags: ["#VozesIA", "#Rápido", "#Profissional", "#Tecnologia"]
        },
        {
            type: "Técnica",
            style: "Informativa",
            text: "Sistema avançado de síntese de voz utilizando redes neurais profundas. Compatível com múltiplos idiomas e estilos vocais. Ideal para aplicações corporativas e educacionais.",
            hashtags: ["#SínteseVoz", "#RedesNeurais", "#IA", "#Tecnologia", "#Educação"]
        }
    ];
}

function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Texto copiado para a área de transferência!', 'success');
    }).catch(() => {
        showNotification('Erro ao copiar texto', 'danger');
    });
}

// Funções de mídia
function playMedia(url) {
    window.open(url, '_blank');
}

function downloadMedia(url) {
    const link = document.createElement('a');
    link.href = url;
    link.download = url.split('/').pop();
    link.click();
}

// Funções utilitárias
function updateTabCounts() {
    const tabs = [
        { id: 'drafts-tab', count: draftsData.length },
        { id: 'scheduled-tab', count: scheduledData.length },
        { id: 'approved-tab', count: approvedData.length },
        { id: 'rejected-tab', count: rejectedData.length }
    ];
    
    tabs.forEach(tab => {
        const tabElement = document.getElementById(tab.id);
        const badge = tabElement.querySelector('.badge');
        if (badge) {
            badge.textContent = tab.count;
        }
    });
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Fechar modal ao clicar fora
document.getElementById('scheduleModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeScheduleModal();
    }
});
