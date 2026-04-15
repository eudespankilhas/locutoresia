import requests
import json
from typing import Dict, Any
from ..types.account_retrieve_response import AccountRetrieveResponse


class Accounts:
    """Recursos de Accounts da API LMNT"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.lmnt.com"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def retrieve(self) -> AccountRetrieveResponse:
        """
        Recupera informações da conta
        
        Returns:
            AccountRetrieveResponse: Informações detalhadas da conta
        """
        url = f"{self.base_url}/v1/account"
        
        try:
            response = requests.get(
                url,
                headers=self.headers
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            return AccountRetrieveResponse.from_dict(response_data)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao recuperar informações da conta: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Erro ao decodificar resposta JSON: {e}")
