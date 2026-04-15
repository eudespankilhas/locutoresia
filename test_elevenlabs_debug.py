#!/usr/bin/env python3
import os
import requests
import json

# Carregar variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv não está instalado

def test_elevenlabs_direct():
    print("Testando ElevenLabs diretamente...")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("ERRO: ELEVENLABS_API_KEY não encontrada!")
        return False
    
    print(f"API Key encontrada: {api_key[:10]}... (comprimento: {len(api_key)})")
    
    # Teste de listagem de vozes
    url = "https://api.elevenlabs.io/v1/voices"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print("Testando listagem de vozes...")
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.ok:
            voices = response.json()
            print(f"Vozes encontradas: {len(voices.get('voices', []))}")
            
            # Mostrar algumas vozes
            for i, voice in enumerate(voices.get('voices', [])[:5]):
                print(f"  {i+1}. {voice.get('name')} ({voice.get('voice_id')})")
            
            # Teste de geração de áudio
            print("\nTestando geração de áudio...")
            voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam
            
            tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            payload = {
                "text": "Hello test.",
                "model_id": "eleven_turbo_v2",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            headers_tts = {
                "xi-api-key": api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg"
            }
            
            response = requests.post(tts_url, headers=headers_tts, json=payload)
            print(f"TTS Status Code: {response.status_code}")
            
            if response.ok:
                audio_data = response.content
                print(f"Áudio gerado! Tamanho: {len(audio_data)} bytes")
                
                # Salvar arquivo
                with open("test_elevenlabs_direct.mp3", "wb") as f:
                    f.write(audio_data)
                print("Áudio salvo como: test_elevenlabs_direct.mp3")
                return True
            else:
                print(f"Erro no TTS: {response.status_code} - {response.text}")
                return False
                
        else:
            print(f"Erro na listagem: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Exceção: {e}")
        return False

if __name__ == "__main__":
    test_elevenlabs_direct()
