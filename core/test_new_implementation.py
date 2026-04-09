import sys
import os
sys.path.append('.')

# Testar nova implementação EdgeTTS
def test_new_implementation():
    print("Testando nova implementação EdgeTTS...")
    
    try:
        from tts_generator_mock import get_tts_generator
        
        tts = get_tts_generator()
        print(f"Gerador TTS: {type(tts).__name__}")
        
        # Teste com texto simples
        text = "Olá mundo, este é um teste com áudio real."
        print(f"Texto: '{text}'")
        
        # Gerar áudio
        audio_data = tts.generate_speech(
            text=text,
            voice_model="Charon",
            style="normal",
            language="pt-BR"
        )
        
        print(f"Áudio gerado: {len(audio_data)} bytes")
        
        # Salvar para análise
        filename = "new_implementation_test.wav"
        with open(filename, "wb") as f:
            f.write(audio_data)
        
        print(f"Arquivo salvo: {filename}")
        
        # Analisar o arquivo
        analyze_audio_file(filename)
        
        return True
        
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def analyze_audio_file(filepath):
    """Analisa um arquivo WAV para verificar seu conteúdo"""
    print(f"\nAnalisando arquivo: {filepath}")
    print(f"Tamanho: {os.path.getsize(filepath)} bytes")
    
    try:
        import wave
        import struct
        
        with wave.open(filepath, 'rb') as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            duration = n_frames / framerate
            
            print(f"Canais: {channels}")
            print(f"Largura da amostra: {sample_width} bytes")
            print(f"Taxa de amostragem: {framerate} Hz")
            print(f"Numero de frames: {n_frames}")
            print(f"Duração: {duration:.2f} segundos")
            
            # Ler dados para verificar conteúdo
            if n_frames > 0:
                frames = wav_file.readframes(min(1000, n_frames))
                if len(frames) > 0 and sample_width == 2:
                    values = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
                    max_val = max(abs(v) for v in values)
                    avg_val = sum(abs(v) for v in values) / len(values)
                    print(f"Valor máximo: {max_val}")
                    print(f"Valor médio: {avg_val:.2f}")
                    
                    if max_val == 0:
                        print("ERRO: Áudio está completamente silencioso!")
                        return False
                    else:
                        print("SUCESSO: Áudio real gerado!")
                        
                        # Verificar variação
                        variation = max(values[:100]) - min(values[:100])
                        print(f"Variação (primeiros 100 samples): {variation}")
                        
                        # Mostrar primeiros valores para debug
                        print(f"Primeiros 20 valores: {values[:20]}")
                        
                        return True
                else:
                    print("ERRO: Não foi possível ler frames")
                    return False
            else:
                print("ERRO: Arquivo não tem frames")
                return False
                
    except Exception as e:
        print(f"ERRO ao analisar arquivo: {e}")
        return False

if __name__ == "__main__":
    success = test_new_implementation()
    if success:
        print("\n=== RESULTADO ===")
        print("EdgeTTS real está funcionando!")
        print("Áudio real gerado com sucesso!")
    else:
        print("\n=== RESULTADO ===")
        print("Problema na nova implementação!")
