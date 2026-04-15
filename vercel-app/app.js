// LMNT Voice Cloner Web App JavaScript

class LMNTWebApp {
    constructor() {
        this.baseURL = '';
        this.currentAudio = null;
        this.voices = [];
        this.init();
    }

    async init() {
        await this.checkConnection();
        await this.loadVoices();
        await this.loadAccountInfo();
    }

    async apiCall(endpoint, method = 'GET', data = null) {
        try {
            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                }
            };

            if (data && method !== 'GET') {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(this.baseURL + endpoint, options);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async checkConnection() {
        try {
            const response = await this.apiCall('/api/lmnt/health');
            this.updateConnectionStatus(true);
            return true;
        } catch (error) {
            this.updateConnectionStatus(false);
            return false;
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (connected) {
            statusElement.innerHTML = '<i class="fas fa-circle text-green-500"></i> Conectado';
        } else {
            statusElement.innerHTML = '<i class="fas fa-circle text-red-500"></i> Desconectado';
        }
    }

    async loadAccountInfo() {
        try {
            this.showLoading('Carregando informações da conta...');
            const account = await this.apiCall('/api/lmnt/account');
            
            document.getElementById('plan-type').textContent = account.plan?.type || 'N/A';
            document.getElementById('character-limit').textContent = account.plan?.character_limit?.toLocaleString() || 'N/A';
            document.getElementById('commercial-use').textContent = account.plan?.commercial_use_allowed ? 'Sim' : 'Não';
            
            this.hideLoading();
        } catch (error) {
            this.showToast('Erro ao carregar informações da conta', 'error');
            this.hideLoading();
        }
    }

    async loadVoices() {
        try {
            this.showLoading('Carregando vozes disponíveis...');
            const response = await this.apiCall('/api/lmnt/voices');
            this.voices = response.voices || [];
            
            // Populate voice select
            const selectElement = document.getElementById('voice-select');
            selectElement.innerHTML = '<option value="">Selecione uma voz...</option>';
            
            this.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.id;
                option.textContent = `${voice.name} (${voice.gender}) - ${voice.description?.substring(0, 50)}...`;
                selectElement.appendChild(option);
            });
            
            // Populate voices grid
            this.renderVoicesGrid();
            
            this.hideLoading();
        } catch (error) {
            this.showToast('Erro ao carregar vozes', 'error');
            this.hideLoading();
        }
    }

    renderVoicesGrid() {
        const gridElement = document.getElementById('voices-grid');
        gridElement.innerHTML = '';
        
        this.voices.forEach(voice => {
            const voiceCard = document.createElement('div');
            voiceCard.className = 'bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-purple-300 transition';
            
            voiceCard.innerHTML = `
                <div class="flex items-start justify-between mb-2">
                    <div>
                        <h4 class="font-semibold text-gray-800">${voice.name}</h4>
                        <p class="text-sm text-gray-600">ID: ${voice.id}</p>
                    </div>
                    <span class="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
                        ${voice.gender || 'N/A'}
                    </span>
                </div>
                <p class="text-sm text-gray-600 mb-3">${voice.description || 'Sem descrição'}</p>
                <div class="flex space-x-2">
                    <button onclick="app.selectVoice('${voice.id}')" 
                        class="flex-1 px-3 py-1 bg-purple-600 text-white text-sm rounded hover:bg-purple-700 transition">
                        <i class="fas fa-play mr-1"></i>Usar
                    </button>
                    <button onclick="app.viewVoiceDetails('${voice.id}')" 
                        class="flex-1 px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300 transition">
                        <i class="fas fa-info-circle mr-1"></i>Info
                    </button>
                </div>
            `;
            
            gridElement.appendChild(voiceCard);
        });
    }

    selectVoice(voiceId) {
        document.getElementById('voice-select').value = voiceId;
        document.getElementById('voice-select').focus();
        this.showToast(`Voz ${voiceId} selecionada`, 'success');
    }

    async viewVoiceDetails(voiceId) {
        try {
            this.showLoading('Carregando detalhes da voz...');
            const voice = await this.apiCall(`/api/lmnt/voice/${voiceId}`);
            
            const details = `
                <strong>Nome:</strong> ${voice.name}<br>
                <strong>ID:</strong> ${voice.id}<br>
                <strong>Gênero:</strong> ${voice.gender || 'N/A'}<br>
                <strong>Descrição:</strong> ${voice.description || 'N/A'}<br>
                <strong>Tipo:</strong> ${voice.type || 'N/A'}<br>
                <strong>Estado:</strong> ${voice.state || 'N/A'}<br>
                <strong>Dono:</strong> ${voice.owner || 'N/A'}
            `;
            
            this.showToast(details, 'info', 5000);
            this.hideLoading();
        } catch (error) {
            this.showToast('Erro ao carregar detalhes da voz', 'error');
            this.hideLoading();
        }
    }

    async generateSpeech() {
        const voiceId = document.getElementById('voice-select').value;
        const text = document.getElementById('text-input').value.trim();
        const format = document.querySelector('input[name="format"]:checked').value;
        
        if (!voiceId) {
            this.showToast('Selecione uma voz', 'error');
            return;
        }
        
        if (!text) {
            this.showToast('Digite um texto para sintetizar', 'error');
            return;
        }
        
        try {
            this.showLoading('Gerando áudio...');
            
            const response = await this.apiCall('/api/lmnt/generate', 'POST', {
                voice_id: voiceId,
                text: text,
                format: format
            });
            
            if (response.success) {
                this.playAudio(response.audio_base64, response.format, voiceId, text);
                this.showToast('Áudio gerado com sucesso!', 'success');
            } else {
                throw new Error('Falha na geração do áudio');
            }
            
            this.hideLoading();
        } catch (error) {
            this.showToast('Erro ao gerar áudio: ' + error.message, 'error');
            this.hideLoading();
        }
    }

    playAudio(audioBase64, format, voiceId, text) {
        const audioData = atob(audioBase64);
        const byteArray = new Uint8Array(audioData.length);
        
        for (let i = 0; i < audioData.length; i++) {
            byteArray[i] = audioData.charCodeAt(i);
        }
        
        const blob = new Blob([byteArray], { type: `audio/${format}` });
        const audioUrl = URL.createObjectURL(blob);
        
        const audioPlayer = document.getElementById('audio-player');
        audioPlayer.src = audioUrl;
        
        // Store current audio for download
        this.currentAudio = {
            blob: blob,
            url: audioUrl,
            format: format,
            filename: `lmnt_${voiceId}_${Date.now()}.${format}`
        };
        
        // Update audio info
        document.getElementById('audio-info').textContent = 
            `Voz: ${voiceId} | Formato: ${format.toUpperCase()} | Tamanho: ${(blob.size / 1024).toFixed(1)} KB`;
        
        // Show audio container
        document.getElementById('audio-container').classList.remove('hidden');
        
        // Auto-play
        audioPlayer.play();
    }

    downloadAudio() {
        if (!this.currentAudio) {
            this.showToast('Nenhum áudio para baixar', 'error');
            return;
        }
        
        const a = document.createElement('a');
        a.href = this.currentAudio.url;
        a.download = this.currentAudio.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        this.showToast('Áudio baixado com sucesso!', 'success');
    }

    async cloneVoice() {
        const name = document.getElementById('clone-name').value.trim();
        const description = document.getElementById('clone-description').value.trim();
        const audioFile = document.getElementById('clone-audio').files[0];
        
        if (!name) {
            this.showToast('Digite um nome para a voz', 'error');
            return;
        }
        
        if (!audioFile) {
            this.showToast('Selecione um arquivo de áudio', 'error');
            return;
        }
        
        try {
            this.showLoading('Clonando voz...');
            
            // Convert audio file to base64
            const audioBase64 = await this.fileToBase64(audioFile);
            
            const response = await this.apiCall('/api/lmnt/clone', 'POST', {
                name: name,
                audio_base64: audioBase64,
                description: description,
                enhance: true
            });
            
            this.showToast(`Voz "${name}" clonada com sucesso!`, 'success');
            
            // Clear form
            document.getElementById('clone-name').value = '';
            document.getElementById('clone-description').value = '';
            document.getElementById('clone-audio').value = '';
            
            // Reload voices
            await this.loadVoices();
            
            this.hideLoading();
        } catch (error) {
            this.showToast('Erro ao clonar voz: ' + error.message, 'error');
            this.hideLoading();
        }
    }

    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = () => {
                // Remove data URL prefix
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = error => reject(error);
        });
    }

    showLoading(message = 'Carregando...') {
        document.getElementById('loading-message').textContent = message;
        document.getElementById('loading-overlay').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading-overlay').classList.add('hidden');
    }

    showToast(message, type = 'success', duration = 3000) {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');
        const toastIcon = document.getElementById('toast-icon');
        
        toastMessage.textContent = message;
        
        // Set icon and color based on type
        if (type === 'error') {
            toastIcon.className = 'fas fa-exclamation-circle text-red-500 mr-3';
        } else if (type === 'info') {
            toastIcon.className = 'fas fa-info-circle text-blue-500 mr-3';
        } else {
            toastIcon.className = 'fas fa-check-circle text-green-500 mr-3';
        }
        
        toast.classList.remove('hidden');
        
        setTimeout(() => {
            toast.classList.add('hidden');
        }, duration);
    }
}

// Global functions for onclick handlers
let app;

window.addEventListener('DOMContentLoaded', () => {
    app = new LMNTWebApp();
});

// Global functions for HTML onclick handlers
window.checkConnection = async () => {
    await app.checkConnection();
    if (app.checkConnection()) {
        await app.loadAccountInfo();
        await app.loadVoices();
    }
};

window.generateSpeech = () => app.generateSpeech();
window.downloadAudio = () => app.downloadAudio();
window.cloneVoice = () => app.cloneVoice();
