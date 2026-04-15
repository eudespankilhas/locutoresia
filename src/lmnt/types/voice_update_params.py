from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class VoiceUpdateParams:
    """Parâmetros para atualização de voz"""
    
    name: Optional[str] = None
    description: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    accent: Optional[str] = None
    language: Optional[str] = None
    is_public: Optional[bool] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário, incluindo apenas campos não nulos"""
        result = {}
        
        if self.name is not None:
            result['name'] = self.name
        if self.description is not None:
            result['description'] = self.description
        if self.gender is not None:
            result['gender'] = self.gender
        if self.age is not None:
            result['age'] = self.age
        if self.accent is not None:
            result['accent'] = self.accent
        if self.language is not None:
            result['language'] = self.language
        if self.is_public is not None:
            result['is_public'] = self.is_public
            
        return result
