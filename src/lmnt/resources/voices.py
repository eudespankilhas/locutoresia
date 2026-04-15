import requests
import json
from typing import Dict, Any, Optional, List
from ..types.voice import Voice
from ..types.voice_create_params import VoiceCreateParams
from ..types.voice_update_params import VoiceUpdateParams
from ..types.voice_update_response import VoiceUpdateResponse
from ..types.voice_list_response import VoiceListResponse
from ..types.voice_delete_response import VoiceDeleteResponse
from ..types.voice_list_params import VoiceListParams


class Voices:
    """Recursos de Voices da API LMNT"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.lmnt.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def create(self, **params) -> Voice:
        """
        Cria uma nova voz
        
        Args:
            **params: Parâmetros para criação de voz (VoiceCreateParams)
            
        Returns:
            Voice: Informações da voz criada
        """
        url = f"{self.base_url}/v1/ai/voice"
        
        # Converter parâmetros para o formato esperado pela API
        create_params = VoiceCreateParams(**params)
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=create_params.to_dict()
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return Voice.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao criar voz: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
    
    def retrieve(self, id: str) -> Voice:
        """
        Recupera informações de uma voz específica
        
        Args:
            id: ID da voz a ser recuperada
            
        Returns:
            Voice: Informações da voz
        """
        url = f"{self.base_url}/v1/ai/voice/{id}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return Voice.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao recuperar voz {id}: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
    
    def update(self, id: str, **params) -> VoiceUpdateResponse:
        """
        Atualiza informações de uma voz
        
        Args:
            id: ID da voz a ser atualizada
            **params: Parâmetros para atualização (VoiceUpdateParams)
            
        Returns:
            VoiceUpdateResponse: Resposta da atualização
        """
        url = f"{self.base_url}/v1/ai/voice/{id}"
        
        # Converter parâmetros para o formato esperado pela API
        update_params = VoiceUpdateParams(**params)
        
        try:
            response = requests.put(
                url,
                headers=self.headers,
                json=update_params.to_dict()
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return VoiceUpdateResponse.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao atualizar voz {id}: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
    
    def list(self, **params) -> VoiceListResponse:
        """
        Lista vozes disponíveis
        
        Args:
            **params: Parâmetros de listagem (VoiceListParams)
            
        Returns:
            VoiceListResponse: Lista de vozes
        """
        url = f"{self.base_url}/v1/ai/voice/list"
        
        # Converter parâmetros para o formato esperado pela API
        list_params = VoiceListParams(**params)
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=list_params.to_dict()
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return VoiceListResponse.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao listar vozes: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
    
    def delete(self, id: str) -> VoiceDeleteResponse:
        """
        Exclui uma voz
        
        Args:
            id: ID da voz a ser excluída
            
        Returns:
            VoiceDeleteResponse: Resposta da exclusão
        """
        url = f"{self.base_url}/v1/ai/voice/{id}"
        
        try:
            response = requests.delete(
                url,
                headers=self.headers
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return VoiceDeleteResponse.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao excluir voz {id}: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
