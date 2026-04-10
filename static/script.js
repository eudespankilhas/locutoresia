// Database de vozes IA - Edge TTS (gratuito)
const voicesDatabase = [
    { id: 1, name: "Antonio - Profissional", description: "Voz masculina clara e profissional", gender: "masculine", language: "pt-BR", style: "professional", avatar: "https://picsum.photos/seed/antonio/80/80", model: "pt-BR-AntonioNeural", provider: "edge", sampleText: "Bem-vindo à nossa empresa. Estamos aqui para oferecer o melhor serviço possível." },
    { id: 2, name: "Francisca - Amigável", description: "Voz feminina calorosa e acolhedora", gender: "feminine", language: "pt-BR", style: "friendly", avatar: "https://picsum.photos/seed/francisca/80/80", model: "pt-BR-FranciscaNeural", provider: "edge", sampleText: "Olá! Que bom ter você aqui. Vamos aprender juntos algo novo hoje." },
    { id: 3, name: "Duarte - Lisboa", description: "Voz masculina portuguesa, elegante e formal", gender: "masculine", language: "pt-PT", style: "professional", avatar: "https://picsum.photos/seed/duarte/80/80", model: "pt-PT-DuarteNeural", provider: "edge", sampleText: "Bem-vindo a Portugal. A nossa equipa está pronta para o receber." },
    { id: 4, name: "Raquel - Lisboa", description: "Voz feminina portuguesa, sofisticada e clara", gender: "feminine", language: "pt-PT", style: "professional", avatar: "https://picsum.photos/seed/raquel/80/80", model: "pt-PT-RaquelNeural", provider: "edge", sampleText: "Olá, seja bem-vindo. Posso ajudá-lo com o que precisar." },
    { id: 5, name: "Guy - English US", description: "American English male voice", gender: "masculine", language: "en-US", style: "professional", avatar: "https://picsum.photos/seed/guy/80/80", model: "en-US-GuyNeural", provider: "edge", sampleText: "Welcome to our platform. We are excited to have you here today." },
    { id: 6, name: "Jenny - English US", description: "American English female voice", gender: "feminine", language: "en-US", style: "friendly", avatar: "https://picsum.photos/seed/jenny/80/80", model: "en-US-JennyNeural", provider: "edge", sampleText: "Hello! I am so glad you joined us today." },
    { id: 7, name: "Ryan - English UK", description: "British English male voice", gender: "masculine", language: "en-GB", style: "professional", avatar: "https://picsum.photos/seed/ryan/80/80", model: "en-GB-RyanNeural", provider: "edge", sampleText: "Good morning. Welcome to our service." },
    { id: 8, name: "Alvaro - Español", description: "Voz masculina en español", gender: "masculine", language: "es-ES", style: "professional", avatar: "https://picsum.photos/seed/alvaro/80/80", model: "es-ES-AlvaroNeural", provider: "edge", sampleText: "Bienvenido a nuestra plataforma." },
    { id: 9, name: "Henri - Français", description: "Voix masculine française", gender: "masculine", language: "fr-FR", style: "professional", avatar: "https://picsum.photos/seed/henri/80/80", model: "fr-FR-HenriNeural", provider: "edge", sampleText: "Bienvenue sur notre plateforme." },
    { id: 10, name: "Conrad - Deutsch", description: "Deutsche männliche Stimme", gender: "masculine", language: "de-DE", style: "professional", avatar: "https://picsum.photos/seed/conrad/80/80", model: "de-DE-ConradNeural", provider: "edge", sampleText: "Willkommen auf unserer Plattform." },
];

let elevenLabsVoices = [];
let currentVoices = [...voicesDatabase];
let selectedVoice = null;
let lastGeneratedAudioBlob = null; // Armazena o último áudio gerado para enviar à MiniDAW

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Locutores IA - Inicializando...');
    console.log('Total de vozes no banco:', voicesDatabase.length);

    renderVoices(currentVoices);
    populateVoiceSelect();
    updateStats();
    loadElevenLabsVoices();

    const audioInput = document.getElementById('audioFileInput');
    if (audioInput) {
        audioInput.addEventListener('change', handleAudioFileSelect);
    }

    console.log('✅ Locutores IA - Inicialização completa!');
});

// ── Carregar vozes ElevenLabs ──────────────────────────────────────────────
async function loadElevenLabsVoices() {
    try {
        const response = await fetch('/api/list-elevenlabs-voices');
        const result = await response.json();
        if (response.ok && result.success && result.voices.length > 0) {
            elevenLabsVoices = result.voices.map((v, i) => ({
                id: `el_${v.id}`,
                name: v.name,
                description: v.description || 'Voz ElevenLabs',
                gender: v.gender || 'neutral',
                language: v.language || 'pt-BR',
                style: 'professional',
                avatar: `https://picsum.photos/seed/${v.name}/80/80`,
                model: v.id,
                provider: 'elevenlabs',
                sampleText: v.sampleText || 'Olá! Esta é uma amostra da minha voz gerada com inteligência artificial.'
            }));
            currentVoices = [...voicesDatabase, ...elevenLabsVoices];
            renderVoices(currentVoices);
            populateVoiceSelect();
            console.log(`${elevenLabsVoices.length} vozes ElevenLabs carregadas!`);
        }
    } catch (error) {
        console.error('Erro ao carregar vozes ElevenLabs:', error);
    }
}

// ── Renderizar vozes ───────────────────────────────────────────────────────
function renderVoices(voices) {
    const container = document.getElementById('voicesContainer');
    container.innerHTML = '';
    const row = document.createElement('div');
    row.className = 'row';
    voices.forEach(voice => row.appendChild(createVoiceCard(voice)));
    container.appendChild(row);
}

function createVoiceCard(voice) {
    const col = document.createElement('div');
    col.className = 'col-md-6 col-lg-4 mb-3';
    const providerBadge = voice.provider === 'elevenlabs'
        ? '<span class="badge bg-warning text-dark ms-1">ElevenLabs</span>'
        : '<span class="badge bg-success ms-1">Free</span>';
    col.innerHTML = `
        <div class="voice-card" onclick="selectVoice('${voice.id}')">
            <div class="text-center">
                <img src="${voice.avatar}" alt="${voice.name}" class="voice-avatar">
                <div class="voice-name">${voice.name} ${providerBadge}</div>
                <div class="voice-description">${voice.description}</div>
                <div class="mb-2">
                    <span class="badge-custom">${getGenderLabel(voice.gender)}</span>
                    <span class="badge-custom">${getLanguageLabel(voice.language)}</span>
                </div>
                <div class="voice-actions justify-content-center">
                    <button class="btn btn-sm btn-outline-primary" onclick="playSample(event, '${voice.id}')">
                        <i class="fas fa-play me-1"></i>Amostra
                    </button>
                    <button class="btn btn-sm btn-outline-secondary" onclick="likeVoice(event, '${voice.id}')">
                        <i class="far fa-heart"></i>
                    </button>
                </div>
            </div>
        </div>`;
    return col;
}

// ── Populate select agrupado ───────────────────────────────────────────────
function populateVoiceSelect() {
    const select = document.getElementById('voiceSelect');
    if (!select) {
        console.error('ERRO: Elemento voiceSelect não encontrado!');
        return;
    }

    console.log('Populando voiceSelect com', voicesDatabase.length, 'vozes Edge TTS');

    select.innerHTML = '<option value="">Selecione uma voz</option>';

    // Grupo Edge TTS
    const edgeGroup = document.createElement('optgroup');
    edgeGroup.label = '🟢 Edge TTS (Gratuito)';
    voicesDatabase.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.id;
        opt.textContent = v.name;
        edgeGroup.appendChild(opt);
    });
    select.appendChild(edgeGroup);
    console.log('Grupo Edge TTS adicionado com', voicesDatabase.length, 'vozes');

    // Grupo ElevenLabs
    if (elevenLabsVoices.length > 0) {
        const elGroup = document.createElement('optgroup');
        elGroup.label = '⭐ ElevenLabs (Alta Qualidade)';
        elevenLabsVoices.forEach(v => {
            const opt = document.createElement('option');
            opt.value = v.id;
            opt.textContent = v.name;
            elGroup.appendChild(opt);
        });
        select.appendChild(elGroup);
        console.log('Grupo ElevenLabs adicionado com', elevenLabsVoices.length, 'vozes');
    }

    console.log('VoiceSelect populado com sucesso!');
}

// ── Selecionar voz ─────────────────────────────────────────────────────────
function selectVoice(voiceId) {
    selectedVoice = currentVoices.find(v => String(v.id) === String(voiceId));
    document.getElementById('voiceSelect').value = voiceId;
    if (selectedVoice) document.getElementById('textInput').value = selectedVoice.sampleText;
    document.querySelector('.generation-panel').scrollIntoView({ behavior: 'smooth' });
}

// ── Filtros ────────────────────────────────────────────────────────────────
function applyFilters() {
    const gender = document.getElementById('genderFilter').value;
    const language = document.getElementById('languageFilter').value;
    const style = document.getElementById('styleFilter').value;
    currentVoices = [...voicesDatabase, ...elevenLabsVoices].filter(v =>
        (!gender || v.gender === gender) &&
        (!language || v.language === language) &&
        (!style || v.style === style)
    );
    renderVoices(currentVoices);
}

function resetFilters() {
    ['genderFilter', 'languageFilter', 'styleFilter'].forEach(id => document.getElementById(id).value = '');
    currentVoices = [...voicesDatabase, ...elevenLabsVoices];
    renderVoices(currentVoices);
}

// ── Gerar áudio (Edge TTS ou ElevenLabs) ──────────────────────────────────
async function generateAudio() {
    const text = document.getElementById('textInput').value.trim();
    const voiceId = document.getElementById('voiceSelect').value;
    const speechStyle = document.getElementById('speechStyle').value;

    if (!text) { alert('Por favor, digite o texto para gerar o áudio.'); return; }
    if (!voiceId) { alert('Por favor, selecione uma voz IA.'); return; }

    const voice = currentVoices.find(v => String(v.id) === String(voiceId));
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('audioPlayer').style.display = 'none';

    try {
        let audioUrl;

        if (voice.provider === 'elevenlabs') {
            // Sintetizar com ElevenLabs
            const response = await fetch('/api/synthesize-cloned-voice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ voice_id: voice.model, text, provider: 'elevenlabs' })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Erro ao gerar áudio');
            audioUrl = `/api/download/${result.filename}?t=` + Date.now();
        } else {
            // Sintetizar com Edge TTS
            const response = await fetch('/api/generate-audio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, voice: voice.model, style: speechStyle, language: voice.language })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Erro ao gerar áudio');
            audioUrl = result.download_url + '?t=' + Date.now();
        }

        const audioPlayer = document.getElementById('generatedAudio');
        
        // Fetch do áudio e salvar como blob para enviar à MiniDAW
        try {
            const audioResponse = await fetch(audioUrl);
            lastGeneratedAudioBlob = await audioResponse.blob();
            // Cria URL do blob para o player
            audioPlayer.src = URL.createObjectURL(lastGeneratedAudioBlob);
        } catch (blobError) {
            console.error('Erro ao criar blob do áudio:', blobError);
            audioPlayer.src = audioUrl; // Fallback para URL direta
        }
        
        audioPlayer.load();
        document.getElementById('loadingSpinner').style.display = 'none';
        document.getElementById('audioPlayer').style.display = 'block';
        updateStats();

    } catch (error) {
        alert('Erro ao gerar áudio: ' + error.message);
        document.getElementById('loadingSpinner').style.display = 'none';
    }
}

function playSample(event, voiceId) {
    event.stopPropagation();
    const voice = currentVoices.find(v => String(v.id) === String(voiceId));
    document.getElementById('textInput').value = voice.sampleText;
    document.getElementById('voiceSelect').value = voiceId;
    generateAudio();
}

function likeVoice(event, voiceId) {
    event.stopPropagation();
    const heart = event.target.closest('button').querySelector('i');
    heart.classList.toggle('far');
    heart.classList.toggle('fas');
    heart.style.color = heart.classList.contains('fas') ? '#e74c3c' : '';
}

function downloadAudio() {
    const audio = document.getElementById('generatedAudio');
    const a = document.createElement('a');
    a.href = audio.src;
    a.download = `locucao_${Date.now()}.wav`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function shareAudio() {
    if (navigator.share) {
        navigator.share({ title: 'Locução IA', text: 'Confira esta locução!', url: window.location.href });
    } else {
        navigator.clipboard.writeText(window.location.href);
        alert('Link copiado!');
    }
}

function updateStats() {
    const el = document.getElementById('audiosCount');
    const n = parseInt(el.textContent.replace(/\D/g, ''));
    el.textContent = (n + 1) + '+';
}

function getGenderLabel(g) {
    return { masculine: 'Masculino', feminine: 'Feminino', neutral: 'Neutro', cloned: 'Clonada' }[g] || g;
}

function getLanguageLabel(l) {
    return { 'pt-BR': 'Português BR', 'pt-PT': 'Português PT', 'en-US': 'Inglês US', 'en-GB': 'Inglês UK', 'es-ES': 'Espanhol', 'fr-FR': 'Francês', 'de-DE': 'Alemão', 'it-IT': 'Italiano', 'ja-JP': 'Japonês', 'zh-CN': 'Chinês' }[l] || l;
}

function getStyleLabel(s) {
    return { professional: 'Profissional', friendly: 'Amigável', energetic: 'Energético', calm: 'Calmo' }[s] || s;
}

// ── Clonagem (desabilitada no plano gratuito) ──────────────────────────────
let audioFileBase64 = null;

function handleAudioFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    if (file.size > 10 * 1024 * 1024) { alert('Arquivo muito grande. Máximo: 10MB'); return; }
    const reader = new FileReader();
    reader.onload = e => {
        audioFileBase64 = e.target.result;
        document.getElementById('previewAudio').src = audioFileBase64;
        document.getElementById('audioPreview').style.display = 'block';
    };
    reader.readAsDataURL(file);
}

async function cloneVoice() {
    alert('Clonagem de voz requer plano pago no ElevenLabs.\nAcesse elevenlabs.io para fazer upgrade.');
}

async function loadClonedVoices() {}
async function generateClonedAudio() {}
async function generateElevenLabsAudio() {}
async function deleteClonedVoice(e) { e.stopPropagation(); }
async function deleteElevenLabsVoice(e) { e.stopPropagation(); }