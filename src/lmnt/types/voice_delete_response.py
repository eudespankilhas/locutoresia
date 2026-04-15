from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class VoiceDeleteResponse:
    """Resposta da exclusão de voz"""
    
    success: bool
    voice_id: str
    message: Optional[str] = None
    deleted_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceDeleteResponse':
        """Cria instância a partir de dicionário"""
        # Tratar data de exclusão
        deleted_at = None
        if 'deleted_at' in data:
            if isinstance(data['deleted_at'], str):
                deleted_at = datetime.fromisoformat(data['deleted_at'].replace('Z', '+00:00'))
            elif isinstance(data['deleted_at'], (int, float)):
                deleted_at = datetime.fromtimestamp(data['deleted_at'])
        
        return cls(
            success=data.get('success', False),
            voice_id=data.get('voice_id', ''),
            message=data.get('message'),
            deleted_at=deleted_at
        )
