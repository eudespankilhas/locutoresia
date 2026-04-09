import asyncio
import edge_tts
import io

VOICE_MAP = {
    "Alex Professional": "pt-BR-AntonioNeural",
    "Charon": "pt-BR-AntonioNeural",
    "Puck": "pt-BR-FranciscaNeural",
    "Leda": "pt-BR-FranciscaNeural",
    "Zephyr": "pt-BR-AntonioNeural",
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
    def generate_speech(self, text, voice_model="Charon", style="normal", language="pt-BR"):
        voice = VOICE_MAP.get(voice_model, VOICE_MAP["default"])
        if language.startswith("en"):
            voice = "en-US-GuyNeural"
        elif language.startswith("es"):
            voice = "es-ES-AlvaroNeural"
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
