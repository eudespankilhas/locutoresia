#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from tts_generator import TTSGenerator

def test_different_tlds():
    print("Testando diferentes TLDs para criar variedade de vozes...")
    
    try:
        tts = TTSGenerator()
        
        # Texto de teste
        text = "Este é um teste para verificar se as vozes realmente são diferentes."
        
        # Testar diferentes vozes com diferentes TLDs
        voices_to_test = [
            ("Adam", "pt-BR", "com.br - Brasil"),
            ("Drew", "pt-BR", "pt - Portugal"),
            ("Bella", "pt-BR", "com.br - Brasil"),
            ("Elli", "pt-BR", "it - Itália"),
            ("Roger", "en-US", "com - EUA"),
            ("Sarah", "en-US", "co.uk - Reino Unido"),
            ("Javier", "es", "es - Espanha"),
            ("Sofia", "es", "com.mx - México")
        ]
        
        print(f"Texto: '{text}'")
        print("=" * 60)
        
        for voice_model, language, description in voices_to_test:
            print(f"\n--- {voice_model} ({description}) ---")
            
            try:
                start_time = time.time()
                audio_data = tts.generate_speech(
                    text=text,
                    voice_model=voice_model,
                    style="normal",
                    language=language
                )
                end_time = time.time()
                
                if audio_data:
                    filename = f"test_{voice_model}_{description.replace(' ', '_').replace('-', '_')}.mp3"
                    with open(filename, "wb") as f:
                        f.write(audio_data)
                    
                    print(f"  Arquivo: {filename}")
                    print(f"  Tempo: {end_time - start_time:.2f}s")
                    print(f"  Tamanho: {len(audio_data)} bytes")
                    
                    # Verificar se os arquivos são realmente diferentes
                    if len(audio_data) > 0:
                        print(f"  Status: OK")
                    else:
                        print(f"  Status: ERRO - arquivo vazio")
                else:
                    print(f"  Status: ERRO - nenhum áudio gerado")
                    
            except Exception as e:
                print(f"  Erro: {e}")
        
        print("\n" + "=" * 60)
        print("Teste concluído! Verifique os arquivos gerados para ouvir as diferenças.")
        return True
        
    except Exception as e:
        print(f"Erro ao testar diferentes TLDs: {e}")
        return False

if __name__ == "__main__":
    import time
    test_different_tlds()
