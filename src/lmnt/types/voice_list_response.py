from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from .voice import Voice


@dataclass
class VoiceListResponse:
    """Resposta da listagem de vozes"""
    
    voices: List[Voice]
    total_count: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    has_more: Optional[bool] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'VoiceListResponse':
        """Cria instância a partir de dicionário"""
        voices_data = data.get('voices', [])
        voices = [Voice.from_dict(voice_data) for voice_data in voices_data]
        
        return cls(
            voices=voices,
            total_count=data.get('total_count'),
            limit=data.get('limit'),
            offset=data.get('offset'),
            has_more=data.get('has_more')
        )
