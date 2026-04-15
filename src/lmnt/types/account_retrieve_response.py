from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountRetrieveResponse:
    """Resposta com informações da conta"""
    
    account_id: str
    email: str
    name: Optional[str] = None
    plan: Optional[str] = None
    credits_remaining: Optional[int] = None
    credits_used: Optional[int] = None
    api_calls_made: Optional[int] = None
    voices_created: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AccountRetrieveResponse':
        """Cria instância a partir de dicionário"""
        # Tratar datas
        created_at = None
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            elif isinstance(data['created_at'], (int, float)):
                created_at = datetime.fromtimestamp(data['created_at'])
        
        updated_at = None
        if 'updated_at' in data:
            if isinstance(data['updated_at'], str):
                updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            elif isinstance(data['updated_at'], (int, float)):
                updated_at = datetime.fromtimestamp(data['updated_at'])
        
        return cls(
            account_id=data.get('account_id', ''),
            email=data.get('email', ''),
            name=data.get('name'),
            plan=data.get('plan'),
            credits_remaining=data.get('credits_remaining'),
            credits_used=data.get('credits_used'),
            api_calls_made=data.get('api_calls_made'),
            voices_created=data.get('voices_created'),
            created_at=created_at,
            updated_at=updated_at,
            metadata=data.get('metadata')
        )
