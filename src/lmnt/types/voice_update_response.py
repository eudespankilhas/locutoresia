from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from .voice import Voice


@dataclass
class VoiceUpdateResponse:
    """Resposta da atualização de voz"""
    
    success: bool
    voice: Voice
    message: Optional[str] = None
    updated_at: Optional[datetime] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceUpdateResponse':
        """Cria instância a partir de dicionário"""
        voice_data = data.get('voice', {})
        voice = Voice.from_dict(voice_data)
        
        # Tratar data de atualização
        updated_at = None
        if 'updated_at' in data:
            if isinstance(data['updated_at'], str):
                updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
            elif isinstance(data['updated_at'], (int, float)):
                updated_at = datetime.fromtimestamp(data['updated_at'])
        
        return cls(
            success=data.get('success', False),
            voice=voice,
            message=data.get('message'),
            updated_at=updated_at
        )
