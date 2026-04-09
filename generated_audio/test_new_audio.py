import os
import sys
sys.path.append('../core')

# Testar o novo TTS Mock diretamente
from tts_generator_mock import TTSGenerator

def test_new_tts():
    print("Testando novo TTS Mock com áudio real...")
    
    tts = TTSGenerator()
    
    # Gerar áudio de teste
    text = "Este é um teste do novo sistema de geração de áudio."
    audio_data = tts.generate_speech(text, voice_model="Charon", style="normal")
    
    # Salvar arquivo
    filename = "test_new_audio.wav"
    with open(filename, "wb") as f:
        f.write(audio_data)
    
    print(f"Áudio gerado: {len(audio_data)} bytes")
    print(f"Arquivo salvo: {filename}")
    
    # Analisar o arquivo
    analyze_audio_file(filename)

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
                    else:
                        print("SUCESSO: Áudio contém dados audíveis!")
                        
                        # Mostrar alguns valores para debug
                        print(f"Primeiros 10 valores: {values[:10]}")
                else:
                    print("ERRO: Não foi possível ler frames ou formato inválido")
            else:
                print("ERRO: Arquivo não tem frames de áudio")
                
    except Exception as e:
        print(f"ERRO ao analisar arquivo WAV: {e}")

if __name__ == "__main__":
    test_new_tts()
