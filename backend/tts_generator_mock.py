import asyncio
import edge_tts
import io

VOICE_MAP = {
    # === PORTUGUÊS BRASIL ===
    "pt-BR-AntonioNeural": "pt-BR-AntonioNeural",
    "pt-BR-FranciscaNeural": "pt-BR-FranciscaNeural",
    # === PORTUGUÊS PORTUGAL ===
    "pt-PT-DuarteNeural": "pt-PT-DuarteNeural",
    "pt-PT-RaquelNeural": "pt-PT-RaquelNeural",
    # === INGLÊS US ===
    "en-US-GuyNeural": "en-US-GuyNeural",
    "en-US-JennyNeural": "en-US-JennyNeural",
    # === INGLÊS UK ===
    "en-GB-RyanNeural": "en-GB-RyanNeural",
    "en-GB-SoniaNeural": "en-GB-SoniaNeural",
    # === ESPANHOL ===
    "es-ES-AlvaroNeural": "es-ES-AlvaroNeural",
    "es-ES-ElviraNeural": "es-ES-ElviraNeural",
    # === FRANCÊS ===
    "fr-FR-HenriNeural": "fr-FR-HenriNeural",
    "fr-FR-DeniseNeural": "fr-FR-DeniseNeural",
    # === ALEMÃO ===
    "de-DE-ConradNeural": "de-DE-ConradNeural",
    "de-DE-KatjaNeural": "de-DE-KatjaNeural",
    # === ITALIANO ===
    "it-IT-DiegoNeural": "it-IT-DiegoNeural",
    "it-IT-ElsaNeural": "it-IT-ElsaNeural",
    # === JAPONÊS ===
    "ja-JP-KeitaNeural": "ja-JP-KeitaNeural",
    "ja-JP-NanamiNeural": "ja-JP-NanamiNeural",
    # === CHINÊS ===
    "zh-CN-YunxiNeural": "zh-CN-YunxiNeural",
    "zh-CN-XiaoxiaoNeural": "zh-CN-XiaoxiaoNeural",
    # === DEFAULT ===
    "default": "pt-BR-AntonioNeural",
}

STYLE_MAP = {
    "normal":   {"rate": "+0%",  "pitch": "+0Hz"},
    "fast":     {"rate": "+30%", "pitch": "+0Hz"},
    "slow":     {"rate": "-25%", "pitch": "-5Hz"},
    "cheerful": {"rate": "+10%", "pitch": "+10Hz"},
    "serious":  {"rate": "-10%", "pitch": "-10Hz"},
}

class EdgeTTSGenerator:
    def generate_speech(self, text, voice_model="pt-BR-AntonioNeural", style="normal", language="pt-BR"):
        # Usar diretamente o modelo EdgeTTS passado
        voice = VOICE_MAP.get(voice_model, VOICE_MAP["default"])
        style_params = STYLE_MAP.get(style, STYLE_MAP["normal"])
        return asyncio.run(self._synthesize(text, voice, style_params["rate"], style_params["pitch"]))

    @staticmethod
    async def _synthesize(text, voice, rate, pitch):
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                buffer.write(chunk["data"])
        buffer.seek(0)
        return buffer.read()

def get_tts_generator():
    return EdgeTTSGenerator()
