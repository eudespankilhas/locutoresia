"""
LMNT Python SDK

SDK completo para interagir com a API LMNT de síntese de voz e clonagem de vozes.

Recursos disponíveis:
- Speech: geração e conversão de áudio
- Accounts: informações da conta
- Voices: gerenciamento de vozes personalizadas

Exemplo de uso:
    from lmnt import LMNTClient
    
    client = LMNTClient(api_key="sua_api_key")
    
    # Gerar áudio
    response = client.generate_speech(
        text="Olá mundo!",
        voice="voice_id"
    )
    response.save_to_file("output.wav")
    
    # Listar vozes
    voices = client.list_voices()
    for voice in voices.voices:
        print(f"Voz: {voice.name} ({voice.id})")
"""

from .client import LMNTClient, create_client
from .resources.speech import Speech, BinaryAPIResponse
from .resources.accounts import Accounts
from .resources.voices import Voices

# Tipos
from .types.account_retrieve_response import AccountRetrieveResponse
from .types.voice import Voice
from .types.voice_create_params import VoiceCreateParams
from .types.voice_update_params import VoiceUpdateParams
from .types.voice_list_params import VoiceListParams
from .types.voice_list_response import VoiceListResponse
from .types.voice_update_response import VoiceUpdateResponse
from .types.voice_delete_response import VoiceDeleteResponse
from .types.speech_convert_params import SpeechConvertParams
from .types.speech_generate_params import SpeechGenerateParams
from .types.speech_generate_detailed_params import SpeechGenerateDetailedParams
from .types.speech_generate_detailed_response import SpeechGenerateDetailedResponse

__version__ = "1.0.0"
__author__ = "LMNT SDK Team"

__all__ = [
    # Cliente principal
    "LMNTClient",
    "create_client",
    
    # Recursos
    "Speech",
    "Accounts", 
    "Voices",
    "BinaryAPIResponse",
    
    # Tipos de Account
    "AccountRetrieveResponse",
    
    # Tipos de Voice
    "Voice",
    "VoiceCreateParams",
    "VoiceUpdateParams", 
    "VoiceListParams",
    "VoiceListResponse",
    "VoiceUpdateResponse",
    "VoiceDeleteResponse",
    
    # Tipos de Speech
    "SpeechConvertParams",
    "SpeechGenerateParams",
    "SpeechGenerateDetailedParams", 
    "SpeechGenerateDetailedResponse",
]
