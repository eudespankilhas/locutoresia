#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from tts_generator import TTSGenerator

def test_real_voices():
    print("Testando se as vozes são realmente diferentes...")
    
    try:
        tts = TTSGenerator()
        
        # Texto curto para testar
        text = "Teste rápido"
        
        # Testar vozes masculinas vs femininas
        voices_to_test = [
            ("Adam", "Masculina"),
            ("Bella", "Feminina"),
            ("Drew", "Masculina"),
            ("Elli", "Feminina")
        ]
        
        print(f"Texto: '{text}'")
        print("=" * 50)
        
        results = []
        
        for voice_model, gender in voices_to_test:
            print(f"\n--- {voice_model} ({gender}) ---")
            
            try:
                start_time = time.time()
                audio_data = tts.generate_speech(
                    text=text,
                    voice_model=voice_model,
                    style="normal",
                    language="pt-BR"
                )
                end_time = time.time()
                
                if audio_data:
                    filename = f"test_{voice_model}_real.mp3"
                    with open(filename, "wb") as f:
                        f.write(audio_data)
                    
                    file_size = len(audio_data)
                    print(f"  Tamanho: {file_size} bytes")
                    print(f"  Tempo: {end_time - start_time:.2f}s")
                    
                    results.append((voice_model, gender, file_size))
                else:
                    print(f"  ERRO: Nenhum áudio gerado")
                    
            except Exception as e:
                print(f"  ERRO: {e}")
        
        print("\n" + "=" * 50)
        print("ANÁLISE DOS RESULTADOS:")
        
        # Verificar se os tamanhos são realmente diferentes
        if len(results) > 1:
            sizes = [r[2] for r in results]
            unique_sizes = set(sizes)
            
            print(f"Tamanhos encontrados: {sizes}")
            print(f"Tamanhos únicos: {unique_sizes}")
            
            if len(unique_sizes) == 1:
                print("CONCLUSÃO: Todos os arquivos têm o mesmo tamanho - mesma voz!")
                print("O GTTS realmente não tem múltiplas vozes.")
            else:
                print("CONCLUSÃO: Arquivos com tamanhos diferentes - vozes diferentes!")
        
        return True
        
    except Exception as e:
        print(f"Erro ao testar: {e}")
        return False

if __name__ == "__main__":
    import time
    test_real_voices()
