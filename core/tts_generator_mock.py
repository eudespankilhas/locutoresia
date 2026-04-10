import os
from google import genai
from google.genai import types

# Mapeamento de vozes para Google Gemini TTS
VOICE_MAP = {
    "pt-BR-AntonioNeural": "Charon",
    "pt-BR-FranciscaNeural": "Puck",
    "pt-PT-DuarteNeural": "Charon",
    "pt-PT-RaquelNeural": "Puck",
    "en-US-GuyNeural": "Charon",
    "en-US-JennyNeural": "Puck",
    "en-GB-RyanNeural": "Charon",
    "es-ES-AlvaroNeural": "Charon",
    "fr-FR-HenriNeural": "Charon",
    "de-DE-ConradNeural": "Charon",
    "default": "Charon",
}

# Mapeamento de estilos para instruções
STYLE_INSTRUCTIONS = {
    "normal": "Fale em tom normal e claro",
    "fast": "FALE EM TOM RÁPIDO",
    "slow": "Fale em tom lento e pausado",
    "cheerful": "FALE EM TOM ALEGRE E FESTIVO",
    "serious": "Fale em tom sério e profissional"
}


class GoogleTTSGenerator:
    """Gerador TTS usando Google Gemini API (funciona no Vercel)"""
    
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY não configurada")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.5-pro-preview-tts"
    
    def generate_speech(self, text, voice_model="Charon", style="normal", language="pt-BR"):
        """Gera áudio usando Google Gemini TTS"""
        
        # Selecionar voz
        voice_name = VOICE_MAP.get(voice_model, VOICE_MAP["default"])
        
        # Instrução de estilo
        instruction = STYLE_INSTRUCTIONS.get(style, "Fale em tom normal e claro")
        full_text = f"{instruction}\n\n{text}"
        
        # Configurar voz simples (não multi-speaker)
        voice_config = types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name=voice_name
            )
        )
        
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=full_text)],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=voice_config
            ),
        )
        
        # Coletar dados de áudio
        audio_data = b""
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.parts is None:
                continue
            if chunk.parts[0].inline_data and chunk.parts[0].inline_data.data:
                audio_data += chunk.parts[0].inline_data.data
        
        return audio_data


def get_tts_generator():
    """Retorna o gerador TTS usando Google Gemini (funciona no Vercel)"""
    try:
        return GoogleTTSGenerator()
    except Exception as e:
        print(f"Erro ao inicializar Google TTS: {e}")
        raise
