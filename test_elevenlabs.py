#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from core.tts_generator import TTSGenerator

def test_elevenlabs():
    print("Testando ElevenLabs TTS...")
    
    tts = TTSGenerator()
    
    try:
        # Teste simples em inglês para evitar problemas de codificação
        text = "Hello! This is a test of ElevenLabs voice."
        print(f"Gerando áudio para: '{text}'")
        
        audio_data = tts.generate_speech(text, voice_model="Adam", style="normal", language="en")
        
        if audio_data:
            filename = "test_elevenlabs_output.mp3"
            with open(filename, "wb") as f:
                f.write(audio_data)
            print(f"Áudio gerado com sucesso! Salvo como: {filename}")
            print(f"Tamanho do arquivo: {len(audio_data)} bytes")
            return True
        else:
            print("Erro: Nenhum dado de áudio retornado")
            return False
            
    except Exception as e:
        print(f"Erro ao testar ElevenLabs: {e}")
        return False

if __name__ == "__main__":
    test_elevenlabs()
