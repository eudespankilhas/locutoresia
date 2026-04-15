from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class SpeechGenerateDetailedParams:
    """Parâmetros para geração detalhada de speech"""
    
    text: str
    voice: str
    speed: Optional[float] = None
    pitch: Optional[float] = None
    format: Optional[str] = None
    return_detailed: Optional[bool] = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        result = {
            'text': self.text,
            'voice': self.voice
        }
        
        if self.speed is not None:
            result['speed'] = self.speed
        if self.pitch is not None:
            result['pitch'] = self.pitch
        if self.format:
            result['format'] = self.format
        if self.return_detailed is not None:
            result['return_detailed'] = self.return_detailed
            
        return result
