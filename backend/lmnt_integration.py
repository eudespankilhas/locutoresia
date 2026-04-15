"""
Integração LMNT Voice Cloner com o backend Locutores IA
"""

import os
import base64
import uuid
from datetime import datetime
from flask import jsonify, request
from core.lmnt_voice_cloner_final import LMNTVoiceClonerFinal

class LMNTIntegration:
    """Classe de integração LMNT com o backend existente"""
    
    def __init__(self):
        try:
            self.cloner = LMNTVoiceClonerFinal()
            self.available = True
        except Exception as e:
            print(f"LMNT não disponível: {e}")
            self.available = False
    
    def get_status(self):
        """Verifica status da integração LMNT"""
        if not self.available:
            return {
                "status": "unavailable",
                "message": "LMNT API não configurada",
                "api_key_set": bool(os.environ.get("LMNT_API_KEY"))
            }
        
        try:
            account = self.cloner.get_account_info()
            return {
                "status": "available",
                "message": "LMNT API funcionando",
                "plan": account.get('plan', {}).get('type', 'Unknown'),
                "character_limit": account.get('plan', {}).get('character_limit', 0),
                "commercial_use": account.get('plan', {}).get('commercial_use_allowed', False)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro na API LMNT: {str(e)}"
            }
    
    def get_available_voices(self):
        """Obtém lista de vozes disponíveis"""
        if not self.available:
            return {"error": "LMNT não disponível"}
        
        try:
            voices = self.cloner.list_voices()
            return {
                "voices": voices.get('voices', []),
                "total_count": len(voices.get('voices', []))
            }
        except Exception as e:
            return {"error": f"Erro ao listar vozes: {str(e)}"}
    
    def generate_speech(self, text, voice_id=None, format="mp3"):
        """Gera áudio usando LMNT"""
        if not self.available:
            return {"error": "LMNT não disponível"}
        
        try:
            # Se não especificar voz, usa a primeira disponível
            if not voice_id:
                voices = self.cloner.list_voices()
                if voices.get('voices'):
                    voice_id = voices['voices'][0]['id']
                else:
                    return {"error": "Nenhuma voz disponível"}
            
            # Gerar áudio
            audio_bytes = self.cloner.synthesize_with_cloned_voice(voice_id, text, format)
            
            # Salvar arquivo
            filename = f"lmnt_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
            filepath = os.path.join(os.path.dirname(__file__), '..', 'generated_audio', filename)
            
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
            return {"error": f"Erro na geração: {str(e)}"}
    
    def clone_voice(self, name, audio_data, description="", enhance=True):
        """Clona uma nova voz"""
        if not self.available:
            return {"error": "LMNT não disponível"}
        
        try:
            voice = self.cloner.clone_voice(name, audio_data, description, enhance)
            return {
                "success": True,
                "voice": voice
            }
        except Exception as e:
            return {"error": f"Erro na clonagem: {str(e)}"}
    
    def get_voice_info(self, voice_id):
        """Obtém informações de uma voz específica"""
        if not self.available:
            return {"error": "LMNT não disponível"}
        
        try:
            voice = self.cloner.get_voice(voice_id)
            return {"voice": voice}
        except Exception as e:
            return {"error": f"Erro ao obter voz: {str(e)}"}

# Instância global da integração
lmnt_integration = LMNTIntegration()
