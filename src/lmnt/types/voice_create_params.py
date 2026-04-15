from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VoiceCreateParams:
    """Parâmetros para criação de voz"""
    
    name: str
    audio_data: bytes  # Dados binários do áudio para clonagem
    description: Optional[str] = None
    enhance: Optional[bool] = True
    gender: Optional[str] = None
    age: Optional[str] = None
    accent: Optional[str] = None
    language: Optional[str] = None
    is_public: Optional[bool] = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        result = {
            'name': self.name,
            'audio_data': self.audio_data
        }
        
        if self.description:
            result['description'] = self.description
        if self.enhance is not None:
            result['enhance'] = self.enhance
        if self.gender:
            result['gender'] = self.gender
        if self.age:
            result['age'] = self.age
        if self.accent:
            result['accent'] = self.accent
        if self.language:
            result['language'] = self.language
        if self.is_public is not None:
            result['is_public'] = self.is_public
            
        return result
