from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SpeechGenerateDetailedResponse:
    """Resposta detalhada da geração de speech"""
    
    audio_data: bytes
    voice_id: str
    text: str
    duration: Optional[float] = None
    format: Optional[str] = None
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SpeechGenerateDetailedResponse':
        """Cria instância a partir de dicionário"""
        # Tratar campo de áudio que pode vir como base64 ou bytes
        audio_data = b''
        if 'audio_data' in data:
            if isinstance(data['audio_data'], str):
                # Se for base64, decodificar
                import base64
                audio_data = base64.b64decode(data['audio_data'])
            elif isinstance(data['audio_data'], bytes):
                audio_data = data['audio_data']
        
        # Tratar data de criação
        created_at = None
        if 'created_at' in data:
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            elif isinstance(data['created_at'], (int, float)):
                created_at = datetime.fromtimestamp(data['created_at'])
        
        return cls(
            audio_data=audio_data,
            voice_id=data.get('voice_id', ''),
            text=data.get('text', ''),
            duration=data.get('duration'),
            format=data.get('format'),
            created_at=created_at,
            metadata=data.get('metadata')
        )
    
    def save_audio(self, filepath: str):
        """Salva o áudio em um arquivo"""
        with open(filepath, 'wb') as f:
            f.write(self.audio_data)
