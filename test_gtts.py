#!/usr/bin/env python3
import os
from gtts import gTTS
import io

def test_gtts():
    print("Testando Google Text-to-Speech (GTTS)...")
    
    try:
        # Texto de teste
        text = "Olá! Este é um teste do Google Text-to-Speech em português brasileiro. Vamos gerar uma locução profissional!"
        
        # Gerar áudio com GTTS
        tts = gTTS(text=text, lang='pt', slow=False)
        
        # Salvar em bytes
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_data = audio_buffer.getvalue()
        
        # Salvar arquivo
        filename = "test_gtts_output.mp3"
        with open(filename, "wb") as f:
            f.write(audio_data)
        
        print(f"Áudio GTTS gerado com sucesso!")
        print(f"Arquivo salvo: {filename}")
        print(f"Tamanho: {len(audio_data)} bytes")
        return True
        
    except Exception as e:
        print(f"Erro ao testar GTTS: {e}")
        return False

if __name__ == "__main__":
    test_gtts()
