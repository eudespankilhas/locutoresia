import os
import requests
import base64
import io
from typing import Dict, Any

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
BASE_URL = "https://api.elevenlabs.io/v1"


class ElevenLabsVoiceCloner:

    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        return {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": content_type
        }

    def clone_voice(self, name: str, audio_bytes: bytes, description: str = "") -> Dict[str, Any]:
        url = f"{BASE_URL}/voices/add"
        files = {"files": ("voice_sample.wav", io.BytesIO(audio_bytes), "audio/wav")}
        data = {"name": name, "description": description or f"Voz clonada: {name}"}
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        response = requests.post(url, headers=headers, data=data, files=files)
        if not response.ok:
            raise Exception(f"Erro ao clonar voz: {response.status_code} - {response.text}")
        return response.json()

    def list_voices(self) -> Dict[str, Any]:
        url = f"{BASE_URL}/voices"
        response = requests.get(url, headers=self._get_headers())
        if not response.ok:
            raise Exception(f"Erro ao listar vozes: {response.status_code} - {response.text}")
        return response.json()

    def get_preset_voices(self) -> Dict[str, Any]:
        return self.list_voices()

    def synthesize_with_cloned_voice(self, voice_id: str, text: str,
                                      model_id: str = "eleven_multilingual_v2") -> bytes:
        url = f"{BASE_URL}/text-to-speech/{voice_id}"
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }
        response = requests.post(url, headers=headers, json=payload)
        if not response.ok:
            raise Exception(f"Erro ao sintetizar áudio: {response.status_code} - {response.text}")
        return response.content

    def delete_voice(self, voice_id: str) -> Dict[str, Any]:
        url = f"{BASE_URL}/voices/{voice_id}"
        response = requests.delete(url, headers={"xi-api-key": ELEVENLABS_API_KEY})
        if not response.ok:
            raise Exception(f"Erro ao deletar voz: {response.status_code} - {response.text}")
        return response.json()

    def get_subscription_info(self) -> Dict[str, Any]:
        url = f"{BASE_URL}/user/subscription"
        response = requests.get(url, headers=self._get_headers())
        if not response.ok:
            raise Exception(f"Erro ao obter assinatura: {response.status_code} - {response.text}")
        return response.json()

    @staticmethod
    def base64_to_bytes(base64_string: str) -> bytes:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
        return base64.b64decode(base64_string)