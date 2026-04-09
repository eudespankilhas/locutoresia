import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Carregar variáveis de ambiente
load_dotenv('../.env')

def test_fixed_tts():
    print("Testando TTS Gemini com configuração corrigida...")
    
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("ERRO: GEMINI_API_KEY não encontrada")
            return None
            
        print(f"API Key encontrada: {api_key[:10]}...")
        
        client = genai.Client(api_key=api_key)
        model = "gemini-2.5-pro-preview-tts"
        
        # Configuração simplificada e corrigida
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text="Olá, este é um teste de áudio."),
                ],
            ),
        ]
        
        # Configuração corrigida - sem multi_speaker
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
        
        print("Enviando requisição corrigida...")
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        
        print("Resposta recebida!")
        if response.parts and response.parts[0].inline_data:
            audio_data = response.parts[0].inline_data.data
            print(f"Áudio gerado com sucesso: {len(audio_data)} bytes")
            
            # Salvar arquivo de teste
            with open("test_audio.wav", "wb") as f:
                f.write(audio_data)
            print("Áudio salvo como test_audio.wav")
            
            return audio_data
        else:
            print("Nenhum áudio na resposta")
            print(f"Resposta: {response}")
            return None
            
    except Exception as e:
        print(f"ERRO: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_fixed_tts()
