import os
import sys
sys.path.append('../core')

# Testar o arquivo mais recente
def test_latest_file():
    print("Testando arquivo mais recente gerado...")
    
    # Encontrar o arquivo mais recente
    files = [f for f in os.listdir('.') if f.endswith('.wav')]
    if not files:
        print("Nenhum arquivo .wav encontrado")
        return
    
    latest_file = max(files, key=lambda f: os.path.getmtime(f))
    print(f"Arquivo mais recente: {latest_file}")
    
    # Analisar o arquivo
    analyze_audio_file(latest_file)

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
            
            # Ler alguns dados para verificar conteúdo
            if n_frames > 0:
                frames = wav_file.readframes(min(1000, n_frames))
                if len(frames) > 0 and sample_width == 2:
                    values = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
                    max_val = max(abs(v) for v in values)
                    avg_val = sum(abs(v) for v in values) / len(values)
                    print(f"Valor máximo: {max_val}")
                    print(f"Valor médio: {avg_val:.2f}")
                    
                    if max_val == 0:
                        print("ALERTA: Áudio ainda está silencioso!")
                        print("PROBLEMA: O servidor está usando versão antiga do TTS Mock")
                        return False
                    else:
                        print("SUCESSO: Áudio contém dados audíveis!")
                        return True
                else:
                    print("ERRO: Não foi possível ler frames ou formato inválido")
                    return False
            else:
                print("ERRO: Arquivo não tem frames de áudio")
                return False
                
    except Exception as e:
        print(f"ERRO ao analisar arquivo WAV: {e}")
        return False

if __name__ == "__main__":
    success = test_latest_file()
    if not success:
        print("\n=== DIAGNÓSTICO ===")
        print("O servidor não reiniciou com as correções do TTS Mock!")
        print("Precisa reiniciar o servidor novamente.")
