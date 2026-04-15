from typing import Optional, Dict, Any, List
from dataclasses import dataclass


@dataclass
class VoiceListParams:
    """Parâmetros para listagem de vozes"""
    
    limit: Optional[int] = None
    offset: Optional[int] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    accent: Optional[str] = None
    language: Optional[str] = None
    is_custom: Optional[bool] = None
    is_public: Optional[bool] = None
    search: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário, incluindo apenas campos não nulos"""
        result = {}
        
        if self.limit is not None:
            result['limit'] = self.limit
        if self.offset is not None:
            result['offset'] = self.offset
        if self.gender:
            result['gender'] = self.gender
        if self.age:
            result['age'] = self.age
        if self.accent:
            result['accent'] = self.accent
        if self.language:
            result['language'] = self.language
        if self.is_custom is not None:
            result['is_custom'] = self.is_custom
        if self.is_public is not None:
            result['is_public'] = self.is_public
        if self.search:
            result['search'] = self.search
            
        return result
