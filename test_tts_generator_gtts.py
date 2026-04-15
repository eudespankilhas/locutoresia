#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from tts_generator import TTSGenerator

def test_tts_generator():
    print("Testando TTSGenerator com GTTS...")
    
    try:
        tts = TTSGenerator()
        
        # Texto de teste
        text = "Olá! Este é um teste do TTSGenerator com Google Text-to-Speech. Vamos gerar uma locução profissional com voz real!"
        
        print(f"Gerando áudio para: '{text}'")
        print("Usando GTTS como principal...")
        
        # Gerar áudio
        audio_data = tts.generate_speech(
            text=text,
            voice_model="Adam",
            style="normal",
            language="pt-BR"
        )
        
        if audio_data:
            filename = "test_tts_generator_gtts.mp3"
            with open(filename, "wb") as f:
                f.write(audio_data)
            
            print(f"Áudio gerado com sucesso!")
            print(f"Arquivo salvo: {filename}")
            print(f"Tamanho: {len(audio_data)} bytes")
            return True
        else:
            print("Erro: Nenhum dado de áudio retornado")
            return False
            
    except Exception as e:
        print(f"Erro ao testar TTSGenerator: {e}")
        return False

if __name__ == "__main__":
    test_tts_generator()
