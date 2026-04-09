import os
from google import genai
from google.genai import types

def test_simple_tts():
    print("Testando TTS Gemini de forma simplificada...")
    
    try:
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        model = "gemini-2.5-pro-preview-tts"
        
        # Teste básico com configuração mínima
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Olá, este é um teste simples."),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            response_modalities=["audio"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Charon"
                    )
                )
            ),
        )
        
        print("Enviando requisição...")
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        
        print("Resposta recebida!")
        if response.parts and response.parts[0].inline_data:
            audio_data = response.parts[0].inline_data.data
            print(f"Áudio gerado: {len(audio_data)} bytes")
            return audio_data
        else:
            print("Nenhum áudio na resposta")
            return None
            
    except Exception as e:
        print(f"ERRO: {e}")
        return None

if __name__ == "__main__":
    test_simple_tts()
