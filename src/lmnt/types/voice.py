from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Voice:
    """Modelo de voz LMNT"""
    
    id: str
    name: str
    gender: Optional[str] = None
    age: Optional[str] = None
    accent: Optional[str] = None
    language: Optional[str] = None
    description: Optional[str] = None
    is_custom: Optional[bool] = None
    is_public: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    sample_audio_url: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Voice':
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
            id=data.get('id', ''),
            name=data.get('name', ''),
            gender=data.get('gender'),
            age=data.get('age'),
            accent=data.get('accent'),
            language=data.get('language'),
            description=data.get('description'),
            is_custom=data.get('is_custom'),
            is_public=data.get('is_public'),
            created_at=created_at,
            updated_at=updated_at,
            metadata=data.get('metadata'),
            sample_audio_url=data.get('sample_audio_url')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        result = {
            'id': self.id,
            'name': self.name
        }
        
        if self.gender:
            result['gender'] = self.gender
        if self.age:
            result['age'] = self.age
        if self.accent:
            result['accent'] = self.accent
        if self.language:
            result['language'] = self.language
        if self.description:
            result['description'] = self.description
        if self.is_custom is not None:
            result['is_custom'] = self.is_custom
        if self.is_public is not None:
            result['is_public'] = self.is_public
        if self.created_at:
            result['created_at'] = self.created_at.isoformat()
        if self.updated_at:
            result['updated_at'] = self.updated_at.isoformat()
        if self.metadata:
            result['metadata'] = self.metadata
        if self.sample_audio_url:
            result['sample_audio_url'] = self.sample_audio_url
            
        return result
