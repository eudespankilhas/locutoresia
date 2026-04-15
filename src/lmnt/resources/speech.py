import requests
import json
from typing import Dict, Any, Optional
from ..types.speech_convert_params import SpeechConvertParams
from ..types.speech_generate_params import SpeechGenerateParams
from ..types.speech_generate_detailed_params import SpeechGenerateDetailedParams
from ..types.speech_generate_detailed_response import SpeechGenerateDetailedResponse


class BinaryAPIResponse:
    """Wrapper para respostas binárias da API"""
    
    def __init__(self, content: bytes, status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
    
    def save_to_file(self, filepath: str):
        """Salva o conteúdo binário em um arquivo"""
        with open(filepath, 'wb') as f:
            f.write(self.content)


class Speech:
    """Recursos de Speech da API LMNT"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.lmnt.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def convert(self, **params) -> BinaryAPIResponse:
        """
        Converte áudio usando os parâmetros fornecidos
        
        Args:
            **params: Parâmetros de conversão (SpeechConvertParams)
            
        Returns:
            BinaryAPIResponse: Resposta binária com o áudio convertido
        """
        url = f"{self.base_url}/v1/ai/speech/convert"
        
        # Converter parâmetros para o formato esperado pela API
        convert_params = SpeechConvertParams(**params)
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=convert_params.to_dict()
            )
            
            response.raise_for_status()
            return BinaryAPIResponse(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na conversão de speech: {e}")
    
    def generate(self, **params) -> BinaryAPIResponse:
        """
        Gera áudio a partir de texto usando os parâmetros fornecidos
        
        Args:
            **params: Parâmetros de geração (SpeechGenerateParams)
            
        Returns:
            BinaryAPIResponse: Resposta binária com o áudio gerado
        """
        url = f"{self.base_url}/v1/ai/speech/bytes"
        
        # Converter parâmetros para o formato esperado pela API
        generate_params = SpeechGenerateParams(**params)
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=generate_params.to_dict()
            )
            
            response.raise_for_status()
            return BinaryAPIResponse(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na geração de speech: {e}")
    
    def generate_detailed(self, **params) -> SpeechGenerateDetailedResponse:
        """
        Gera áudio com detalhes adicionais
        
        Args:
            **params: Parâmetros de geração detalhada (SpeechGenerateDetailedParams)
            
        Returns:
            SpeechGenerateDetailedResponse: Resposta detalhada com metadados
        """
        url = f"{self.base_url}/v1/ai/speech"
        
        # Converter parâmetros para o formato esperado pela API
        detailed_params = SpeechGenerateDetailedParams(**params)
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=detailed_params.to_dict()
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return SpeechGenerateDetailedResponse.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na geração detalhada de speech: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
