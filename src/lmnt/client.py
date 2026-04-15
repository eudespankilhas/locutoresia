import os
from typing import Optional
from .resources.speech import Speech
from .resources.accounts import Accounts
from .resources.voices import Voices
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


class LMNTClient:
    """
    Cliente principal da API LMNT
    
    Este cliente fornece acesso a todos os recursos da API LMNT:
    - Speech: geração e conversão de áudio
    - Accounts: informações da conta
    - Voices: gerenciamento de vozes
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.lmnt.com"):
        """
        Inicializa o cliente LMNT
        
        Args:
            api_key: Chave da API LMNT. Se não fornecida, tentará obter da variável de ambiente LMNT_API_KEY
            base_url: URL base da API LMNT
        """
        self.api_key = api_key or os.environ.get("LMNT_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "API key não fornecida. Configure LMNT_API_KEY como variável de ambiente "
                "ou passe como parâmetro para o construtor."
            )
        
        self.base_url = base_url
        
        # Inicializar recursos
        self.speech = Speech(self.api_key, self.base_url)
        self.accounts = Accounts(self.api_key, self.base_url)
        self.voices = Voices(self.api_key, self.base_url)
    
    # Métodos de conveniência para acesso rápido
    
    # Speech
    def convert_speech(self, **params) -> 'BinaryAPIResponse':
        """Converte áudio usando parâmetros fornecidos"""
        return self.speech.convert(**params)
    
    def generate_speech(self, **params) -> 'BinaryAPIResponse':
        """Gera áudio a partir de texto"""
        return self.speech.generate(**params)
    
    def generate_detailed_speech(self, **params) -> SpeechGenerateDetailedResponse:
        """Gera áudio com detalhes adicionais"""
        return self.speech.generate_detailed(**params)
    
    # Accounts
    def get_account_info(self) -> AccountRetrieveResponse:
        """Obtém informações da conta"""
        return self.accounts.retrieve()
    
    # Voices
    def create_voice(self, **params) -> Voice:
        """Cria uma nova voz"""
        return self.voices.create(**params)
    
    def get_voice(self, voice_id: str) -> Voice:
        """Obtém informações de uma voz específica"""
        return self.voices.retrieve(voice_id)
    
    def update_voice(self, voice_id: str, **params) -> VoiceUpdateResponse:
        """Atualiza informações de uma voz"""
        return self.voices.update(voice_id, **params)
    
    def list_voices(self, **params) -> VoiceListResponse:
        """Lista vozes disponíveis"""
        return self.voices.list(**params)
    
    def delete_voice(self, voice_id: str) -> VoiceDeleteResponse:
        """Exclui uma voz"""
        return self.voices.delete(voice_id)
    
    def __repr__(self):
        return f"LMNTClient(base_url='{self.base_url}', api_key='{self.api_key[:10]}...')"


# Função de conveniência para criar cliente rapidamente
def create_client(api_key: Optional[str] = None) -> LMNTClient:
    """
    Função de conveniência para criar um cliente LMNT
    
    Args:
        api_key: Chave da API LMNT
        
    Returns:
        LMNTClient: Instância do cliente
    """
    return LMNTClient(api_key=api_key)


# Importar BinaryAPIResponse para estar disponível no nível do cliente
from .resources.speech import BinaryAPIResponse
