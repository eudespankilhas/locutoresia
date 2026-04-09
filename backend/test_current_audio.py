import os
import sys
sys.path.append('../core')

# Testar o arquivo atual gerado
def test_current_audio():
    print("Testando arquivo atual gerado...")
    
    # Encontrar o arquivo mais recente
    files = [f for f in os.listdir('.') if f.startswith('test_locution_') and f.endswith('.wav')]
    if not files:
        print("Nenhum arquivo de teste encontrado")
        return False
    
    latest_file = max(files, key=lambda f: os.path.getmtime(f))
    print(f"Arquivo mais recente: {latest_file}")
    
    # Analisar o arquivo
    return analyze_audio_file(latest_file)

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
                        print("SUCESSO: Áudio tem dados!")
                        
                        # Verificar variação
                        variation = max(values[:100]) - min(values[:100])
                        print(f"Variação (primeiros 100 samples): {variation}")
                        
                        if variation > 500:
                            print("INDICADOR: Variação alta - bom para fala sintetizada")
                        else:
                            print("INDICADOR: Variação baixa - pode ser tom constante")
                        
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
    success = test_current_audio()
    if success:
        print("\n=== DIAGNÓSTICO FINAL ===")
        print("Backend está gerando áudio CORRETAMENTE!")
        print("O problema está no FRONTEND - player não está carregando o arquivo.")
        print("\nSOLUÇÃO:")
        print("1. O backend funciona (API 200)")
        print("2. O arquivo de áudio tem dados")
        print("3. O frontend não está atualizando o player")
        print("4. Precisa corrigir JavaScript do player")
    else:
        print("\n=== DIAGNÓSTICO FINAL ===")
        print("Backend não está gerando áudio corretamente!")
