"""
Gerador de Imagens com Fallback - NewPost-IA
Orquestra a geração de imagens usando Replicate e Stable Horde.
"""

import os
import requests
import logging
import time
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self):
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
        self.stable_horde_key = os.getenv("STABLE_HORDE_API_KEY", "0000000000") # '0000000000' is the default anonymous key

    def generate_image(self, prompt: str) -> Optional[str]:
        """
        Tenta gerar imagem usando múltiplos provedores.
        Retorna a URL da imagem gerada ou None.
        """
        # 1. Tentar Replicate
        if self.replicate_token:
            logger.info("Tentando gerar imagem via Replicate...")
            url = self._generate_via_replicate(prompt)
            if url: return url
        
        # 2. Tentar Stable Horde (Fallback)
        logger.info("Tentando gerar imagem via Stable Horde (Fallback)...")
        url = self._generate_via_stable_horde(prompt)
        if url: return url

        # 3. Fallback final: Imagem Placeholder/Mock
        logger.warning("Todos os provedores de imagem falharam. Usando placeholder.")
        return f"https://loremflickr.com/800/600/technology,artificialintelligence?random={int(time.time())}"

    def _generate_via_replicate(self, prompt: str) -> Optional[str]:
        """Integração com Replicate API (SDXL Turbo)"""
        try:
            # Replicate HTTP API (SDXL Turbo)
            headers = {
                "Authorization": f"Token {self.replicate_token}",
                "Content-Type": "application/json"
            }
            # SDXL Turbo Model URL/Version
            model_version = "62828551f50a-4b9e-9d2a-1c0c32688820" # Example version
            # No Replicate real, geralmente mandamos para o endpoint de 'predictions'
            payload = {
                "version": "a8274a3834a2f8c5c70f90e945c50c05b8229bd8dc1d743a1682f6f582f3c788", # SDXL Turbo
                "input": {"prompt": prompt, "width": 768, "height": 768, "num_inference_steps": 1}
            }
            
            response = requests.post("https://api.replicate.com/v1/predictions", json=payload, headers=headers, timeout=15)
            if response.status_code == 201:
                prediction = response.json()
                get_url = prediction["urls"]["get"]
                
                # Polling simples (max 30s)
                for _ in range(10):
                    res = requests.get(get_url, headers=headers)
                    pred_data = res.json()
                    if pred_data["status"] == "succeeded":
                        # Retorna a lista de outputs (primeira imagem)
                        return pred_data["output"][0] if pred_data.get("output") else None
                    if pred_data["status"] == "failed":
                        break
                    time.sleep(3)
            return None
        except Exception as e:
            logger.error(f"Erro no Replicate: {e}")
            return None

    def _generate_via_stable_horde(self, prompt: str) -> Optional[str]:
        """Integração com Stable Horde (Comunidade Gratuita)"""
        try:
            headers = {
                "Content-Type": "application/json",
                "apikey": self.stable_horde_key
            }
            payload = {
                "prompt": f"{prompt} ### fotorealism, cinematic",
                "params": {
                    "steps": 20,
                    "n": 1,
                    "sampler_name": "k_euler",
                    "width": 512,
                    "height": 512
                }
            }
            
            # 1. Enviar requisição
            response = requests.post("https://stablehorde.net/api/v2/generate/async", json=payload, headers=headers, timeout=15)
            if response.status_code == 202:
                req_id = response.json()["id"]
                
                # 2. Polling por status
                for _ in range(15):
                    status_res = requests.get(f"https://stablehorde.net/api/v2/generate/check/{req_id}", timeout=10)
                    status_data = status_res.json()
                    if status_data.get("done"):
                        final_res = requests.get(f"https://stablehorde.net/api/v2/generate/status/{req_id}", timeout=10)
                        final_data = final_res.json()
                        return final_data["generations"][0]["img"] # Retorna URL da imagem hospedada ou base64
                    time.sleep(4)
            return None
        except Exception as e:
            logger.error(f"Erro no Stable Horde: {e}")
            return None
