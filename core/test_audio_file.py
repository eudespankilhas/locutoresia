import os
import wave
import struct

def analyze_audio_file(filepath):
    """Analisa um arquivo WAV para verificar seu conteúdo"""
    print(f"Analisando arquivo: {filepath}")
    print(f"Tamanho: {os.path.getsize(filepath)} bytes")
    
    try:
        with wave.open(filepath, 'rb') as wav_file:
            # Informações do arquivo WAV
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
            
            # Ler alguns dados para verificar se não é apenas silêncio
            if n_frames > 0:
                frames = wav_file.readframes(min(1000, n_frames))  # Ler primeiros 1000 frames
                if len(frames) > 0:
                    # Converter para int para verificar valores
                    if sample_width == 2:
                        values = struct.unpack('<' + 'h' * (len(frames) // 2), frames)
                        max_val = max(abs(v) for v in values)
                        avg_val = sum(abs(v) for v in values) / len(values)
                        print(f"Valor máximo: {max_val}")
                        print(f"Valor médio: {avg_val:.2f}")
                        
                        if max_val == 0:
                            print("ALERTA: Áudio parece ser completamente silencioso!")
                        else:
                            print("OK: Áudio contém dados não nulos")
                else:
                    print("ERRO: Não foi possível ler frames do áudio")
            else:
                print("ERRO: Arquivo não tem frames de áudio")
                
    except Exception as e:
        print(f"ERRO ao analisar arquivo WAV: {e}")

# Testar os arquivos gerados
audio_files = [
    "locution_a417bdcd_20260408_155239.wav",
    "locution_d4d2ca8d_20260408_155346.wav"
]

for filename in audio_files:
    if os.path.exists(filename):
        analyze_audio_file(filename)
        print("-" * 50)
    else:
        print(f"Arquivo não encontrado: {filename}")
