import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Testar se a chave da API está sendo carregada
api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key encontrada: {api_key[:10]}..." if api_key else "API Key NÃO encontrada!")

# Testar importação do módulo TTS
try:
    from tts_generator import TTSGenerator
    print("Módulo TTSGenerator importado com sucesso!")
    
    # Testar criação da instância
    tts = TTSGenerator()
    print("Instância TTSGenerator criada com sucesso!")
    
    # Testar geração de áudio simples
    print("Testando geração de áudio...")
    audio_data = tts.generate_speech(
        text="Olá, este é um teste.",
        voice_model="Charon",
        style="normal",
        language="pt-BR"
    )
    
    if audio_data:
        print(f"Áudio gerado com sucesso! Tamanho: {len(audio_data)} bytes")
    else:
        print("Falha na geração de áudio - dados vazios")
        
except ImportError as e:
    print(f"Erro ao importar TTSGenerator: {e}")
except Exception as e:
    print(f"Erro durante o teste: {e}")
    import traceback
    traceback.print_exc()
