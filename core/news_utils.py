"""
Utilitário Central de Notícias - NewPost-IA
Unifica a lógica de coleta, processamento e publicação.
"""

import os
import re
import time
import json
import uuid
import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsUtils:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL", "").strip()
        if self.supabase_url and not self.supabase_url.endswith("/rest/v1/posts"):
            self.supabase_url = f"{self.supabase_url.rstrip('/')}/rest/v1/posts"
        
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY", "").strip()
        
    def fetch_web_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Simula busca web. Em produção, integrar com NewsAPI ou similar.
        """
        logger.info(f"Buscando notícias para: {query}")
        # Simulando resultados para manter o fluxo funcional
        results = []
        for i in range(max_results):
            results.append({
                "title": f"Notícia {i+1} sobre {query}: Avanços em IA no Brasil",
                "url": f"https://noticias-ia.com.br/artigo-{uuid.uuid4().hex[:6]}",
                "source": "IA News",
                "snippet": f"A inteligência artificial está transformando o cenário tecnológico brasileiro com novas parcerias no setor de {query}...",
                "published_at": datetime.now().isoformat()
            })
        return results

    def normalize_news(self, raw_data: Dict) -> Dict:
        """
        Padroniza os dados da notícia para o formato do banco.
        """
        title = raw_data.get("title", "Sem Título").strip()
        content = raw_data.get("snippet", raw_data.get("content", ""))
        
        # Gerar Slug Simples
        slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
        slug = slug[:50] + f"-{int(time.time()) % 10000}"

        # Tags baseadas no título
        tags = ["ia", "tecnologia"]
        if "brasil" in title.lower(): tags.append("brasil")
        if "google" in title.lower(): tags.append("google")

        return {
            "title": title[:150],
            "content": content,
            "source_url": raw_data.get("url"),
            "image_url": raw_data.get("image_url"),
            "category": raw_data.get("category", "tecnologia").lower(),
            "published_at": raw_data.get("published_at", datetime.now().isoformat()),
            "status": "draft",
            "metadata": {
                "source": raw_data.get("source", "Web"),
                "sentiment": "neutro",
                "relevance_score": 7,
                "tags": tags,
                "slug": slug
            }
        }

    def is_duplicate(self, source_url: str) -> bool:
        """
        Verifica se a URL já existe no Supabase.
        """
        if not self.supabase_url or not self.supabase_key:
            return False
            
        try:
            params = {"source_url": f"eq.{source_url}"}
            headers = {"apikey": self.supabase_key, "Authorization": f"Bearer {self.supabase_key}"}
            response = requests.get(self.supabase_url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                return len(response.json()) > 0
            return False
        except Exception as e:
            logger.error(f"Erro ao checar duplicata: {e}")
            return False

    def save_to_supabase(self, data: Dict) -> Tuple[bool, str]:
        """
        Salva a notícia no Supabase no formato correto.
        """
        if not self.supabase_url or not self.supabase_key:
            return False, "Credenciais Supabase ausentes"

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

        try:
            # Flattening metadata if required by the DB schema
            # O Banco parece ter colunas específicas baseadas no news_agent anterior
            payload = {
                "title": data["title"],
                "content": data["content"],
                "source_url": data["source_url"],
                "image_url": data.get("image_url"),
                "category": data["category"],
                "published_at": data["published_at"],
                "status": data["status"], # Aqui usamos o 'draft' aprovado
                "metadata": data["metadata"]
            }

            response = requests.post(self.supabase_url, json=payload, headers=headers, timeout=20)
            
            if response.status_code in [201, 201]:
                logger.info(f"Notícia salva com sucesso: {data['title']}")
                return True, "Sucesso"
            else:
                logger.error(f"Erro Supabase ({response.status_code}): {response.text}")
                return False, response.text
        except Exception as e:
            logger.error(f"Exceção ao salvar: {e}")
            return False, str(e)
