from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class SpeechConvertParams:
    """Parâmetros para conversão de speech"""
    
    input_format: str
    output_format: str
    data: bytes  # Dados binários do áudio
    voice: Optional[str] = None
    speed: Optional[float] = None
    pitch: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário, tratando dados binários"""
        result = {
            'input_format': self.input_format,
            'output_format': self.output_format,
            'data': self.data
        }
        
        if self.voice:
            result['voice'] = self.voice
        if self.speed is not None:
            result['speed'] = self.speed
        if self.pitch is not None:
            result['pitch'] = self.pitch
            
        return result
