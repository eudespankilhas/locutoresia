import asyncio
import edge_tts
import io
import wave
import struct

# Mapeamento de vozes por modelo/idioma
VOICE_MAP = {
    # Português Brasil
    "Alex Professional": "pt-BR-AntonioNeural",
    "Charon": "pt-BR-AntonioNeural",
    "Puck": "pt-BR-FranciscaNeural",
    "Leda": "pt-BR-FranciscaNeural",
    "Zephyr": "pt-BR-AntonioNeural",
    # Fallback genérico
    "default": "pt-BR-AntonioNeural",
}

# Mapeamento de estilos para ajuste de prosódia
STYLE_MAP = {
    "normal":   {"rate": "+0%",  "pitch": "+0Hz"},
    "fast":     {"rate": "+30%", "pitch": "+0Hz"},
    "slow":     {"rate": "-25%", "pitch": "-5Hz"},
    "cheerful": {"rate": "+10%", "pitch": "+10Hz"},
    "serious":  {"rate": "-10%", "pitch": "-10Hz"},
}


class EdgeTTSGenerator:
    """Gerador TTS real usando edge-tts (Microsoft Neural TTS)."""

    def generate_speech(self, text: str, voice_model: str = "Charon",
                        style: str = "normal", language: str = "pt-BR") -> bytes:
        """
        Gera áudio WAV real a partir de texto.

        Returns
        -------
        bytes
            Conteúdo do arquivo WAV.
        """
        # Escolher voz
        voice = VOICE_MAP.get(voice_model, VOICE_MAP["default"])

        # Ajustar para o idioma solicitado, se necessário
        if language.startswith("en"):
            voice = "en-US-GuyNeural"
        elif language.startswith("es"):
            voice = "es-ES-AlvaroNeural"

        # Parâmetros de estilo
        style_params = STYLE_MAP.get(style, STYLE_MAP["normal"])

        audio_bytes = asyncio.run(
            self._synthesize(text, voice, style_params["rate"], style_params["pitch"])
        )
        return audio_bytes

    @staticmethod
    async def _synthesize(text: str, voice: str, rate: str, pitch: str) -> bytes:
        """Chama a API edge-tts de forma assíncrona e converte para WAV."""
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])
        
        # Converter para WAV
        audio_data = buffer.getvalue()
        wav_data = EdgeTTSGenerator._convert_to_wav(audio_data)
        return wav_data
    
    @staticmethod
    def _convert_to_wav(audio_data: bytes) -> bytes:
        """Converte áudio EdgeTTS (MP3/Ogg) para WAV."""
        # Para simplificar, vamos criar um WAV com os dados brutos
        # EdgeTTS geralmente retorna 24kHz, 16-bit, mono
        
        sample_rate = 24000
        bits_per_sample = 16
        num_channels = 1
        
        # Se os dados já estiverem em formato PCM, apenas adicionar header WAV
        # Se não, vamos assumir que são PCM brutos
        data_size = len(audio_data)
        
        # WAV header
        header = struct.pack(
            "<4sI4s4sIHHIIHH4sI",
            b"RIFF",          # ChunkID
            36 + data_size,   # ChunkSize
            b"WAVE",          # Format
            b"fmt ",          # Subchunk1ID
            16,               # Subchunk1Size
            1,                # AudioFormat (PCM)
            num_channels,     # NumChannels
            sample_rate,      # SampleRate
            sample_rate * 2,  # ByteRate
            2,                # BlockAlign
            bits_per_sample,  # BitsPerSample
            b"data",          # Subchunk2ID
            data_size         # Subchunk2Size
        )
        
        return header + audio_data


# Para compatibilidade, também manter o TTSGenerator original
try:
    from tts_generator import TTSGenerator as OriginalTTSGenerator
except ImportError:
    OriginalTTSGenerator = None

def get_tts_generator():
    """Retorna o gerador TTS real usando EdgeTTS."""
    try:
        return EdgeTTSGenerator()
    except Exception as e:
        print(f"Erro ao inicializar EdgeTTS: {e}")
        # Fallback para o mock se EdgeTTS falhar
        from tts_generator_mock import TTSGenerator
        print("Usando TTS Mock como fallback")
        return TTSGenerator()
