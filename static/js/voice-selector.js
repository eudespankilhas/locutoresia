/**
 * Voice Selector - Solução definitiva para múltiplas vozes
 * Funciona independentemente das variáveis de ambiente da Vercel
 */

class VoiceSelector {
    constructor() {
        this.voices = [
            { id: 'amy', name: 'Amy', gender: 'F', description: 'Narrative. Excited. US' },
            { id: 'ansel', name: 'Ansel', gender: 'M', description: 'Young, engaging voice with enthusiasm' },
            { id: 'autumn', name: 'Autumn', gender: 'F', description: 'Warm, friendly female voice' },
            { id: 'ava', name: 'Ava', gender: 'F', description: 'Conversational. Sultry. US' },
            { id: 'bella', name: 'Bella', gender: 'F', description: 'Professional female voice' },
            { id: 'charlie', name: 'Charlie', gender: 'M', description: 'Friendly male voice' },
            { id: 'drew', name: 'Drew', gender: 'M', description: 'Professional male voice' },
            { id: 'elli', name: 'Elli', gender: 'F', description: 'Italian female voice' },
            { id: 'javier', name: 'Javier', gender: 'M', description: 'Spanish male voice' },
            { id: 'pierre', name: 'Pierre', gender: 'M', description: 'French male voice' },
            { id: 'roger', name: 'Roger', gender: 'M', description: 'American male voice' },
            { id: 'sarah', name: 'Sarah', gender: 'F', description: 'British female voice' },
            { id: 'sofia', name: 'Sofia', gender: 'F', description: 'Mexican female voice' },
            { id: 'adam', name: 'Adam', gender: 'M', description: 'Generic male voice' },
            { id: 'brian', name: 'Brian', gender: 'M', description: 'Professional male voice' },
            { id: 'emma', name: 'Emma', gender: 'F', description: 'Natural female voice' },
            { id: 'olivia', name: 'Olivia', gender: 'F', description: 'Young female voice' },
            { id: 'ryan', name: 'Ryan', gender: 'M', description: 'Casual male voice' },
            { id: 'sophia', name: 'Sophia', gender: 'F', description: 'Elegant female voice' },
            { id: 'liam', name: 'Liam', gender: 'M', description: 'Deep male voice' },
            { id: 'mia', name: 'Mia', gender: 'F', description: 'Sweet female voice' }
        ];
        
        this.init();
    }
    
    init() {
        this.setupVoiceSelector();
        this.setupEventListeners();
        this.loadSavedPreferences();
    }
    
    setupVoiceSelector() {
        // Adicionar seletor de vozes na página principal
        const voiceSelect = document.getElementById('voiceSelect');
        if (voiceSelect) {
            voiceSelect.innerHTML = '<option value="">Selecione uma voz...</option>';
            
            this.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.id;
                option.textContent = `${voice.name} (${voice.gender}) - ${voice.description.substring(0, 40)}...`;
                voiceSelect.appendChild(option);
            });
        }
        
        // Adicionar seletor no painel de clonagem
        const cloneVoiceSelect = document.getElementById('cloneVoiceSelect');
        if (cloneVoiceSelect) {
            cloneVoiceSelect.innerHTML = '<option value="">Selecione uma voz para clonar...</option>';
            
            this.voices.forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.id;
                option.textContent = `${voice.name} - ${voice.description}`;
                cloneVoiceSelect.appendChild(option);
            });
        }
    }
    
    setupEventListeners() {
        // Event listener para seleção de voz
        const voiceSelect = document.getElementById('voiceSelect');
        if (voiceSelect) {
            voiceSelect.addEventListener('change', (e) => {
                this.saveVoicePreference(e.target.value);
                this.updateVoiceInfo(e.target.value);
            });
        }
        
        // Event listener para geração de áudio
        const generateBtn = document.getElementById('generateAudioBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateAudio();
            });
        }
    }
    
    generateAudio() {
        const text = document.getElementById('textInput')?.value?.trim();
        const voiceId = document.getElementById('voiceSelect')?.value;
        
        if (!text) {
            this.showMessage('Por favor, digite um texto para gerar áudio', 'error');
            return;
        }
        
        if (!voiceId) {
            this.showMessage('Por favor, selecione uma voz', 'error');
            return;
        }
        
        // Tentar usar API LMNT primeiro
        this.tryLMNTGeneration(text, voiceId)
            .catch(() => {
                // Fallback para síntese do navegador
                this.fallbackBrowserSynthesis(text, voiceId);
            });
    }
    
    async tryLMNTGeneration(text, voiceId) {
        try {
            const response = await fetch('/api/lmnt/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    voice_id: voiceId,
                    format: 'mp3'
                })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    this.playAudio(data.filename, data.voice_id);
                    return;
                }
            }
            
            throw new Error('LMNT API não disponível');
            
        } catch (error) {
            console.log('LMNT não disponível, usando síntese do navegador:', error);
            throw error;
        }
    }
    
    fallbackBrowserSynthesis(text, voiceId) {
        if ('speechSynthesis' in window) {
            // Mapear IDs de voz para vozes do navegador
            const voiceMap = {
                'amy': 'Microsoft Zira Desktop - English (United States)',
                'bella': 'Microsoft Hazel Desktop - English (United Kingdom)',
                'sarah': 'Microsoft Susan Desktop - English (United Kingdom)',
                'emma': 'Microsoft Zira Desktop - English (United States)',
                'olivia': 'Microsoft Hazel Desktop - English (United Kingdom)',
                'adam': 'Microsoft David Desktop - English (United States)',
                'brian': 'Microsoft David Desktop - English (United States)',
                'ryan': 'Microsoft Mark Desktop - English (United States)',
                'liam': 'Microsoft David Desktop - English (United States)',
                'drew': 'Microsoft David Desktop - English (United States)',
                'charlie': 'Microsoft David Desktop - English (United States)',
                'roger': 'Microsoft David Desktop - English (United States)',
                'javier': 'Microsoft Sabina Desktop - Spanish (Spain)',
                'pierre': 'Microsoft Hortense Desktop - French (France)',
                'elli': 'Microsoft Elsa Desktop - Italian (Italy)',
                'sofia': 'Microsoft Helena Desktop - Spanish (Mexico)',
                'autumn': 'Microsoft Zira Desktop - English (United States)',
                'ava': 'Microsoft Hazel Desktop - English (United Kingdom)',
                'mia': 'Microsoft Zira Desktop - English (United States)',
                'sophia': 'Microsoft Hazel Desktop - English (United Kingdom)'
            };
            
            const utterance = new SpeechSynthesisUtterance(text);
            const selectedVoice = voiceMap[voiceId] || 'Microsoft Zira Desktop - English (United States)';
            
            // Encontrar a voz correspondente
            const voices = speechSynthesis.getVoices();
            const voice = voices.find(v => v.name === selectedVoice);
            
            if (voice) {
                utterance.voice = voice;
            }
            
            utterance.rate = 1.0;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            
            speechSynthesis.speak(utterance);
            this.showMessage(`Gerando áudio com voz: ${this.getVoiceName(voiceId)}`, 'success');
            
        } else {
            this.showMessage('Seu navegador não suporta síntese de voz', 'error');
        }
    }
    
    getVoiceName(voiceId) {
        const voice = this.voices.find(v => v.id === voiceId);
        return voice ? voice.name : voiceId;
    }
    
    updateVoiceInfo(voiceId) {
        const voice = this.voices.find(v => v.id === voiceId);
        if (voice) {
            const infoDiv = document.getElementById('voiceInfo');
            if (infoDiv) {
                infoDiv.innerHTML = `
                    <div class="voice-info-card">
                        <h4>${voice.name}</h4>
                        <p><strong>Gênero:</strong> ${voice.gender}</p>
                        <p><strong>Descrição:</strong> ${voice.description}</p>
                        <p><strong>ID:</strong> ${voice.id}</p>
                    </div>
                `;
            }
        }
    }
    
    saveVoicePreference(voiceId) {
        localStorage.setItem('preferredVoice', voiceId);
    }
    
    loadSavedPreferences() {
        const savedVoice = localStorage.getItem('preferredVoice');
        if (savedVoice) {
            const voiceSelect = document.getElementById('voiceSelect');
            if (voiceSelect) {
                voiceSelect.value = savedVoice;
                this.updateVoiceInfo(savedVoice);
            }
        }
    }
    
    playAudio(filename, voiceId) {
        const audio = new Audio(`/generated_audio/${filename}`);
        audio.play();
        this.showMessage(`Áudio gerado com voz: ${this.getVoiceName(voiceId)}`, 'success');
    }
    
    showMessage(message, type = 'info') {
        // Criar toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new VoiceSelector();
});

// Adicionar estilos CSS
const style = document.createElement('style');
style.textContent = `
    .voice-info-card {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .voice-info-card h4 {
        margin-bottom: 0.5rem;
        color: #495057;
    }
    
    .voice-info-card p {
        margin-bottom: 0.25rem;
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    .toast {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 9999;
        animation: slideIn 0.3s ease;
    }
    
    .toast-success {
        background: #28a745;
    }
    
    .toast-error {
        background: #dc3545;
    }
    
    .toast-info {
        background: #17a2b8;
    }
    
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;

document.head.appendChild(style);
