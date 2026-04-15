#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from tts_generator import TTSGenerator

def test_multiple_voices():
    print("Testando múltiplas vozes e velocidade...")
    
    try:
        tts = TTSGenerator()
        
        # Testar diferentes vozes
        voices_to_test = [
            ("Adam", "pt-BR"),
            ("Bella", "pt-BR"), 
            ("Roger", "en-US"),
            ("Javier", "es"),
            ("Pierre", "fr")
        ]
        
        # Texto curto para testar velocidade
        short_text = "Teste rápido de áudio!"
        
        # Texto longo para testar qualidade
        long_text = "Este é um teste mais longo para verificar a qualidade e velocidade da geração de áudio com diferentes vozes e estilos de fala."
        
        for voice_model, language in voices_to_test:
            print(f"\n--- Testando voz: {voice_model} ({language}) ---")
            
            # Testar texto curto
            print("Texto curto:")
            start_time = time.time()
            audio_data = tts.generate_speech(
                text=short_text,
                voice_model=voice_model,
                style="normal",
                language=language
            )
            end_time = time.time()
            
            if audio_data:
                filename = f"test_{voice_model}_short.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_data)
                print(f"  Áudio gerado: {filename}")
                print(f"  Tempo: {end_time - start_time:.2f}s")
                print(f"  Tamanho: {len(audio_data)} bytes")
            else:
                print("  Erro: Nenhum áudio gerado")
            
            # Testar estilo rápido
            print("Estilo rápido:")
            start_time = time.time()
            audio_data = tts.generate_speech(
                text=short_text,
                voice_model=voice_model,
                style="fast",
                language=language
            )
            end_time = time.time()
            
            if audio_data:
                filename = f"test_{voice_model}_fast.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_data)
                print(f"  Áudio gerado: {filename}")
                print(f"  Tempo: {end_time - start_time:.2f}s")
            else:
                print("  Erro: Nenhum áudio gerado")
        
        print("\n--- Teste concluído! ---")
        return True
        
    except Exception as e:
        print(f"Erro ao testar múltiplas vozes: {e}")
        return False

if __name__ == "__main__":
    import time
    test_multiple_voices()
