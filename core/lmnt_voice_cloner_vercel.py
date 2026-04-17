"""
Integração LMNT otimizada para Vercel (sem dependências problemáticas)
"""

import os
import base64
import requests
from typing import Optional, Dict, Any, List

class LMNTVoiceClonerVercel:
    """Cliente LMNT usando API REST direta (sem SDK) para Vercel"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LMNT_API_KEY")
        self.base_url = "https://api.lmnt.com/v1"
        
        if not self.api_key:
            raise ValueError("LMNT_API_KEY não configurada")
    
    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_account_info(self) -> Dict[str, Any]:
        """Obtém informações da conta"""
        try:
            response = requests.get(
                f"{self.base_url}/account",
                headers=self._headers(),
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def list_voices(self) -> Dict[str, Any]:
        """Lista vozes disponíveis"""
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers=self._headers(),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return {
                'voices': data.get('voices', []),
                'total_count': len(data.get('voices', []))
            }
        except Exception as e:
            return {"error": str(e), "voices": []}
    
    def synthesize(self, voice_id: str, text: str, format: str = "mp3") -> bytes:
        """Gera áudio usando voz"""
        try:
            response = requests.post(
                f"{self.base_url}/speech",
                headers=self._headers(),
                json={
                    "voice": voice_id,
                    "text": text,
                    "format": format
                },
                timeout=30
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Erro na síntese: {e}")

# Wrapper seguro que não quebra se LMNT falhar
class SafeLMNTIntegration:
    """Integração segura que não crasha se LMNT não estiver disponível"""
    
    def __init__(self):
        self.client = None
        self.error = None
        try:
            self.client = LMNTVoiceClonerVercel()
        except Exception as e:
            self.error = str(e)
    
    def get_status(self):
        if self.client is None:
            return {
                "status": "unavailable",
                "message": f"LMNT não disponível: {self.error}",
                "api_key_set": bool(os.environ.get("LMNT_API_KEY"))
            }
        try:
            account = self.client.get_account_info()
            if "error" in account:
                return {
                    "status": "error",
                    "message": account["error"],
                    "api_key_set": True
                }
            return {
                "status": "available",
                "message": "LMNT API funcionando",
                "plan": account.get('plan', {}).get('type', 'Unknown')
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "api_key_set": True
            }
    
    def get_available_voices(self):
        if self.client is None:
            return {"error": "LMNT não disponível", "voices": []}
        return self.client.list_voices()
    
    def generate_speech(self, text, voice_id=None, format="mp3"):
        if self.client is None:
            return {"error": "LMNT não disponível"}
        try:
            if not voice_id:
                voices = self.client.list_voices()
                if voices.get('voices'):
                    voice_id = voices['voices'][0]['id']
                else:
                    return {"error": "Nenhuma voz disponível"}
            
            audio_bytes = self.client.synthesize(voice_id, text, format)
            
            # Salvar arquivo
            import uuid
            from datetime import datetime
            filename = f"lmnt_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            
            # No Vercel, salvar em /tmp
            upload_folder = os.environ.get('VERCEL') and '/tmp/generated_audio' or 'generated_audio'
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            
            with open(filepath, 'wb') as f:
                f.write(audio_bytes)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "voice_id": voice_id,
                "format": format,
                "text": text,
                "size_bytes": len(audio_bytes)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def clone_voice(self, name, audio_data, description="", enhance=True):
        return {"error": "Clonagem não disponível nesta versão"}
    
    def get_voice_info(self, voice_id):
        return {"error": "Info de voz não disponível nesta versão"}

# Instância global
lmnt_integration = SafeLMNTIntegration()
