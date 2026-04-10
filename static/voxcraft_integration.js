// VoxCraft Integration - Locutores IA
(function(){
    const state = {isActive:false, sessionId:null, postId:null, title:'', returnUrl:'', text:'', audioFilename:null};
    
    document.addEventListener('DOMContentLoaded', function(){
        const params = new URLSearchParams(window.location.search);
        if(params.get('voxcraft') === 'true'){
            initVoxCraft(params);
        }
    });
    
    function initVoxCraft(params){
        state.isActive = true;
        state.sessionId = params.get('session_id');
        state.postId = params.get('post_id');
        state.title = decodeURIComponent(params.get('title') || 'Notícia VoxCraft');
        state.returnUrl = decodeURIComponent(params.get('return_url') || '');
        state.text = decodeURIComponent(params.get('text') || '');
        
        addBanner();
        prefillText();
        watchAudioGeneration();
        
        console.log('✅ VoxCraft mode active:', state);
    }
    
    function addBanner(){
        const banner = document.createElement('div');
        banner.id = 'voxcraft-banner';
        banner.innerHTML = `
            <div style="background:linear-gradient(135deg,#8b5cf6,#7c3aed);color:white;padding:15px 20px;border-radius:10px;margin:0 0 20px 0;display:flex;align-items:center;gap:12px;">
                <span style="font-size:24px;">🚀</span>
                <div>
                    <div style="font-weight:bold;font-size:16px;">Modo VoxCraft Ativo</div>
                    <div style="font-size:13px;opacity:0.9;">${state.title}</div>
                </div>
            </div>`;
        const container = document.querySelector('.container');
        if(container) container.insertBefore(banner, container.firstChild);
    }
    
    function prefillText(){
        const textarea = document.getElementById('textInput');
        if(textarea && state.text){
            textarea.value = state.text;
            textarea.style.border = '2px solid #8b5cf6';
            console.log('✅ Text pre-filled');
        }
    }
    
    function watchAudioGeneration(){
        const audioPlayer = document.getElementById('generatedAudio');
        if(!audioPlayer) return;
        
        const observer = new MutationObserver(function(mutations){
            mutations.forEach(function(mutation){
                if(mutation.type === 'attributes' && mutation.attributeName === 'src'){
                    const src = audioPlayer.src;
                    if(src && src.includes('locution_')){
                        state.audioFilename = src.split('/').pop().split('?')[0];
                        state.audioGenerated = true;
                        showReturnButton();
                        console.log('✅ Audio generated:', state.audioFilename);
                    }
                }
            });
        });
        
        observer.observe(audioPlayer, {attributes:true});
    }
    
    function showReturnButton(){
        if(document.getElementById('voxcraft-return-btn')) return;
        
        const btn = document.createElement('button');
        btn.id = 'voxcraft-return-btn';
        btn.innerHTML = '🚀 Voltar para VoxCraft';
        btn.style.cssText = 'background:linear-gradient(135deg,#8b5cf6,#7c3aed);color:white;border:none;padding:12px 24px;border-radius:8px;font-weight:bold;cursor:pointer;margin-top:15px;';
        btn.onclick = returnToVoxCraft;
        
        const controls = document.querySelector('.audio-controls');
        if(controls) controls.appendChild(btn);
    }
    
    async function returnToVoxCraft(){
        if(!state.sessionId || !state.audioFilename){
            alert('Áudio não gerado ainda!');
            return;
        }
        
        try{
            const response = await fetch('/api/voxcraft/complete',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({session_id:state.sessionId, audio_filename:state.audioFilename})
            });
            const data = await response.json();
            
            if(data.success && data.return_url){
                window.location.href = data.return_url;
            } else if(state.returnUrl){
                window.location.href = state.returnUrl + '?audio=' + state.audioFilename;
            } else{
                alert('Áudio gerado com sucesso! Nome: ' + state.audioFilename);
            }
        } catch(e){
            console.error('Error:', e);
            if(state.returnUrl) window.location.href = state.returnUrl;
        }
    }
    
    // Expõe função global
    window.returnToVoxCraft = returnToVoxCraft;
})();
