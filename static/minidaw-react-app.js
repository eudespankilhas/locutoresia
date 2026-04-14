// MiniDAW React App - Versão Integrada
// Simulação da aplicação React para integração com Locutores IA

class MiniDAWReactApp {
    constructor() {
        this.tracks = [];
        this.isPlaying = false;
        this.currentTime = 0;
        this.voices = this.loadVoices();
        this.history = this.loadHistory();
        this.init();
    }

    init() {
        console.log('MiniDAW React App initialized');
        this.renderApp();
    }

    loadVoices() {
        // Carrega vozes do localStorage ou usa defaults
        const stored = localStorage.getItem('cloned_voices_library');
        if (stored) {
            try {
                return JSON.parse(stored);
            } catch (e) {
                console.error('Error loading voices:', e);
            }
        }
        
        // Vozes padrão para demonstração
        return [
            {
                id: '1',
                name: 'Alex Professional',
                description: 'Voz masculina corporativa',
                gender: 'masculino',
                createdAt: new Date().toISOString(),
                lmntVoiceId: 'alex-professional'
            },
            {
                id: '2',
                name: 'Maria Amigável',
                description: 'Voz feminina calorosa',
                gender: 'feminino',
                createdAt: new Date().toISOString(),
                lmntVoiceId: 'maria-amigavel'
            }
        ];
    }

    loadHistory() {
        const stored = localStorage.getItem('voice_generation_history');
        if (stored) {
            try {
                return JSON.parse(stored);
            } catch (e) {
                console.error('Error loading history:', e);
            }
        }
        return [];
    }

    renderApp() {
        const container = document.getElementById('react-daw-container');
        if (!container) return;

        container.innerHTML = `
            <div style="padding: 2rem; height: 100%; overflow-y: auto;">
                <h3 style="color: #6366f1; margin-bottom: 1.5rem;">
                    <i class="fas fa-robot me-2"></i>MiniDAW com Geração de Voz IA
                </h3>
                
                <!-- Botão Gerar Voz -->
                <div style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; padding: 1rem; border-radius: 8px; margin-bottom: 2rem;">
                    <h4 style="margin: 0 0 1rem 0;">
                        <i class="fas fa-magic me-2"></i>Gerar Voz com IA
                    </h4>
                    <button onclick="minidawReact.showVoiceGenerator()" style="background: white; color: #6366f1; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; cursor: pointer;">
                        <i class="fas fa-plus me-2"></i>Nova Geração de Voz
                    </button>
                </div>

                <!-- Tracks -->
                <div style="margin-bottom: 2rem;">
                    <h4 style="margin-bottom: 1rem;">
                        <i class="fas fa-sliders-h me-2"></i>Tracks de Áudio
                    </h4>
                    <div id="tracks-container">
                        ${this.renderTracks()}
                    </div>
                    <button onclick="minidawReact.addTrack('voice')" style="background: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; margin-right: 0.5rem;">
                        <i class="fas fa-microphone me-1"></i>Adicionar Locução
                    </button>
                    <button onclick="minidawReact.addTrack('music')" style="background: #a855f7; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px;">
                        <i class="fas fa-music me-1"></i>Adicionar Trilha
                    </button>
                </div>

                <!-- Controles -->
                <div style="background: rgba(30, 41, 59, 0.8); padding: 1rem; border-radius: 8px; display: flex; align-items: center; gap: 1rem;">
                    <button onclick="minidawReact.togglePlay()" style="width: 48px; height: 48px; border-radius: 50%; background: #6366f1; border: none; color: white; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                        <i class="fas fa-play" id="play-btn"></i>
                    </button>
                    <span style="color: #94a3b8;">Tempo: <span id="current-time">0:00</span></span>
                    <span style="color: #94a3b8;">Duração: <span id="total-duration">0:00</span></span>
                    <button onclick="minidawReact.exportMix()" style="background: #10b981; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; margin-left: auto;">
                        <i class="fas fa-download me-1"></i>Exportar
                    </button>
                </div>
            </div>
        `;
    }

    renderTracks() {
        if (this.tracks.length === 0) {
            return `
                <div style="text-align: center; padding: 2rem; background: rgba(30, 41, 59, 0.3); border-radius: 8px; margin-bottom: 1rem;">
                    <i class="fas fa-music" style="font-size: 3rem; color: #64748b; margin-bottom: 1rem;"></i>
                    <p style="color: #94a3b8;">Nenhuma track adicionada</p>
                    <p style="color: #64748b; font-size: 0.875rem;">Adicione locuções ou trilhas para começar</p>
                </div>
            `;
        }

        return this.tracks.map((track, index) => `
            <div style="background: ${track.type === 'voice' ? 'rgba(59, 130, 246, 0.1)' : 'rgba(168, 85, 247, 0.1)'}; border: 1px solid ${track.type === 'voice' ? '#3b82f6' : '#a855f7'}; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <div style="display: flex; justify-content: between; align-items: center; margin-bottom: 0.5rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <div style="width: 3px; height: 20px; background: ${track.type === 'voice' ? '#3b82f6' : '#a855f7'}; border-radius: 2px;"></div>
                        <strong style="color: #f1f5f9;">${track.name}</strong>
                        <span style="background: ${track.type === 'voice' ? 'rgba(59, 130, 246, 0.2)' : 'rgba(168, 85, 247, 0.2)'}; color: ${track.type === 'voice' ? '#3b82f6' : '#a855f7'}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem;">
                            ${track.type === 'voice' ? 'Locução' : 'Trilha'}
                        </span>
                    </div>
                    <button onclick="minidawReact.removeTrack(${index})" style="background: transparent; border: none; color: #ef4444; cursor: pointer;">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                ${track.audioUrl ? `
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 6px; padding: 0.75rem; margin-top: 0.5rem;">
                        <p style="color: #10b981; margin: 0; font-size: 0.875rem;">
                            <i class="fas fa-check-circle me-1"></i>Áudio carregado
                        </p>
                    </div>
                ` : `
                    <div style="background: rgba(15, 23, 42, 0.6); border: 2px dashed #475569; border-radius: 6px; padding: 1rem; text-align: center; margin-top: 0.5rem;">
                        <p style="color: #94a3b8; margin: 0;">Arraste áudio aqui ou gere com voz IA</p>
                    </div>
                `}
            </div>
        `).join('');
    }

    showVoiceGenerator() {
        const container = document.getElementById('react-daw-container');
        if (!container) return;

        container.innerHTML = `
            <div style="padding: 2rem;">
                <h3 style="color: #6366f1; margin-bottom: 1.5rem;">
                    <i class="fas fa-magic me-2"></i>Gerar Voz com IA
                </h3>
                
                <div style="background: rgba(30, 41, 59, 0.8); border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;">
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; color: #f1f5f9; margin-bottom: 0.5rem;">Voz Clonada</label>
                        <select id="voice-select" style="width: 100%; padding: 0.5rem; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #f1f5f9;">
                            <option value="">Selecione uma voz</option>
                            ${this.voices.map(voice => `
                                <option value="${voice.id}">${voice.name} - ${voice.description}</option>
                            `).join('')}
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 1rem;">
                        <label style="display: block; color: #f1f5f9; margin-bottom: 0.5rem;">Texto para Gerar</label>
                        <textarea id="text-input" style="width: 100%; min-height: 100px; padding: 0.5rem; background: #1e293b; border: 1px solid #475569; border-radius: 6px; color: #f1f5f9; resize: vertical;" placeholder="Digite o texto que será falado pela voz IA..."></textarea>
                    </div>
                    
                    <button onclick="minidawReact.generateVoice()" style="background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 6px; font-weight: 600; cursor: pointer; width: 100%;">
                        <i class="fas fa-magic me-2"></i>Gerar Voz
                    </button>
                </div>
                
                <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid #6366f1; border-radius: 8px; padding: 1rem; margin-bottom: 1.5rem;">
                    <h5 style="color: #6366f1; margin-bottom: 0.5rem;">
                        <i class="fas fa-history me-2"></i>Gerações Recentes
                    </h5>
                    ${this.history.length > 0 ? `
                        <div style="max-height: 200px; overflow-y: auto;">
                            ${this.history.slice(0, 5).map(item => `
                                <div style="background: rgba(30, 41, 59, 0.6); border-radius: 6px; padding: 0.75rem; margin-bottom: 0.5rem; cursor: pointer;" onclick="minidawReact.useHistoryItem('${item.id}')">
                                    <p style="color: #f1f5f9; margin: 0; font-weight: 600;">${item.voiceName}</p>
                                    <p style="color: #94a3b8; margin: 0; font-size: 0.875rem;">${item.text.substring(0, 50)}${item.text.length > 50 ? '...' : ''}</p>
                                </div>
                            `).join('')}
                        </div>
                    ` : `
                        <p style="color: #94a3b8; margin: 0;">Nenhuma geração recente</p>
                    `}
                </div>
                
                <button onclick="minidawReact.renderApp()" style="background: #475569; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer;">
                    <i class="fas fa-arrow-left me-2"></i>Voltar para MiniDAW
                </button>
            </div>
        `;
    }

    generateVoice() {
        const voiceSelect = document.getElementById('voice-select');
        const textInput = document.getElementById('text-input');
        
        if (!voiceSelect.value || !textInput.value.trim()) {
            alert('Selecione uma voz e digite o texto');
            return;
        }

        // Simulação de geração
        const voice = this.voices.find(v => v.id === voiceSelect.value);
        const newHistory = {
            id: Date.now().toString(),
            text: textInput.value,
            voiceName: voice.name,
            voiceId: voiceSelect.value,
            audioUrl: 'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBjiS2Oy9diMFl2+z5N17GwU7k9n1unEiBC13yO/eizEIHWq+8+OZURE',
            createdAt: new Date().toISOString()
        };

        this.history.unshift(newHistory);
        this.history = this.history.slice(0, 20); // Mantém 20 mais recentes
        localStorage.setItem('voice_generation_history', JSON.stringify(this.history));

        // Adiciona à track
        this.addTrackWithAudio('voice', newHistory.audioUrl, `${voice.name} - ${textInput.value.substring(0, 30)}...`);

        alert('Voz gerada com sucesso! Adicionada à track de locução.');
        this.renderApp();
    }

    useHistoryItem(itemId) {
        const item = this.history.find(h => h.id === itemId);
        if (item) {
            const voiceSelect = document.getElementById('voice-select');
            const textInput = document.getElementById('text-input');
            voiceSelect.value = item.voiceId;
            textInput.value = item.text;
        }
    }

    addTrack(type) {
        const newTrack = {
            id: Date.now().toString(),
            name: type === 'voice' ? `Locução ${this.tracks.filter(t => t.type === 'voice').length + 1}` : `Trilha ${this.tracks.filter(t => t.type === 'music').length + 1}`,
            type,
            audioUrl: null
        };
        this.tracks.push(newTrack);
        this.renderApp();
    }

    addTrackWithAudio(type, audioUrl, name) {
        const newTrack = {
            id: Date.now().toString(),
            name: name || (type === 'voice' ? `Locução ${this.tracks.filter(t => t.type === 'voice').length + 1}` : `Trilha ${this.tracks.filter(t => t.type === 'music').length + 1}`),
            type,
            audioUrl
        };
        this.tracks.push(newTrack);
    }

    removeTrack(index) {
        this.tracks.splice(index, 1);
        this.renderApp();
    }

    togglePlay() {
        this.isPlaying = !this.isPlaying;
        const playBtn = document.getElementById('play-btn');
        if (playBtn) {
            playBtn.className = this.isPlaying ? 'fas fa-pause' : 'fas fa-play';
        }
    }

    exportMix() {
        alert('Função de exportação em desenvolvimento. Na versão completa, você poderá exportar em WAV ou MP3.');
    }
}

// Inicializa a aplicação
let minidawReact;
document.addEventListener('DOMContentLoaded', function() {
    minidawReact = new MiniDAWReactApp();
});
