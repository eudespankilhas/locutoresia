"""
Cliente Supabase para publicação automática de notícias - NewPost-IA
"""

import json
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Cliente para integração com Supabase API"""
    
    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "apikey": api_key,
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
    
    def publish_post(self, post_data: Dict) -> Tuple[bool, Optional[str]]:
        """
        Publica post no Supabase
        
        Args:
            post_data: Dicionário com dados do post
            
        Returns:
            Tuple (success: bool, post_id: Optional[str])
        """
        try:
            # Validar campos obrigatórios
            required_fields = [
                "title", "content", "url_source", "source", 
                "category", "author", "published_at", 
                "slug", "tags", "sentiment", 
                "relevance_score", "status", "created_at"
            ]
            
            for field in required_fields:
                if field not in post_data or not post_data[field]:
                    logger.error(f"Campo obrigatório ausente: {field}")
                    return False, None
            
            # Validar formatos
            if not isinstance(post_data["tags"], str):
                # Converter array para string JSON
                post_data["tags"] = json.dumps(post_data["tags"])
            
            # Validar score
            if not isinstance(post_data["relevance_score"], int) or not (1 <= post_data["relevance_score"] <= 10):
                logger.error(f"relevance_score inválido: {post_data['relevance_score']}")
                return False, None
            
            # Validar sentimento
            if post_data["sentiment"] not in ["positivo", "negativo", "neutro"]:
                logger.error(f"sentiment inválido: {post_data['sentiment']}")
                return False, None
            
            # Fazer requisição POST
            response = requests.post(
                self.url,
                json=post_data,
                headers=self.headers,
                timeout=30
            )
            
            # Processar resposta
            if response.status_code == 201:
                result = response.json()
                post_id = result.get("id")
                logger.info(f"Post publicado com sucesso: {post_data['title']} (ID: {post_id})")
                return True, post_id
                
            elif response.status_code == 409:
                logger.warning(f"Post duplicado no Supabase: {post_data['title']}")
                return False, None
                
            elif response.status_code == 401:
                logger.error("Erro de autenticação no Supabase")
                return False, None
                
            elif response.status_code >= 500:
                logger.error(f"Erro no servidor Supabase: {response.status_code}")
                return False, None
                
            else:
                logger.error(f"Erro ao publicar post: {response.status_code} - {response.text}")
                return False, None
                
        except requests.exceptions.Timeout:
            logger.error("Timeout na requisição ao Supabase")
            return False, None
            
        except requests.exceptions.ConnectionError:
            logger.error("Erro de conexão com Supabase")
            return False, None
            
        except Exception as e:
            logger.error(f"Exceção ao publicar no Supabase: {str(e)}")
            return False, None
    
    def check_duplicate_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Verifica se já existe post com mesmo slug
        
        Args:
            slug: Slug para verificar
            
        Returns:
            Dict com dados do post ou None se não encontrado
        """
        try:
            response = requests.get(
                f"{self.url}?slug=eq.{slug}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                posts = response.json()
                if posts and len(posts) > 0:
                    return posts[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao verificar duplicata por slug: {str(e)}")
            return None
    
    def get_posts_by_source(self, source: str, limit: int = 10) -> List[Dict]:
        """
        Obtém posts de uma fonte específica
        
        Args:
            source: Nome da fonte
            limit: Número máximo de posts
            
        Returns:
            Lista de posts
        """
        try:
            response = requests.get(
                f"{self.url}?source=eq.{source}&order=created_at.desc&limit={limit}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            
            return []
            
        except Exception as e:
            logger.error(f"Erro ao obter posts da fonte {source}: {str(e)}")
            return []
    
    def update_post_status(self, post_id: str, status: str) -> bool:
        """
        Atualiza status de um post
        
        Args:
            post_id: ID do post
            status: Novo status
            
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            if status not in ["pending", "published", "failed", "archived"]:
                logger.error(f"Status inválido: {status}")
                return False
            
            response = requests.patch(
                f"{self.url}?id=eq.{post_id}",
                json={"status": status, "updated_at": datetime.utcnow().isoformat()},
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 204:
                logger.info(f"Status do post {post_id} atualizado para {status}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao atualizar status do post {post_id}: {str(e)}")
            return False
    
    def get_stats(self) -> Dict:
        """
        Obtém estatísticas dos posts
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            # Total de posts
            response = requests.get(
                f"{self.url}?select=count",
                headers=self.headers,
                timeout=10
            )
            
            total_posts = 0
            if response.status_code == 200:
                result = response.json()
                total_posts = result.get("count", 0)
            
            # Posts por fonte
            response = requests.get(
                f"{self.url}?select=source,count",
                headers=self.headers,
                timeout=10
            )
            
            posts_by_source = {}
            if response.status_code == 200:
                result = response.json()
                for item in result:
                    posts_by_source[item["source"]] = item["count"]
            
            # Posts recentes (últimas 24h)
            yesterday = datetime.utcnow() - timedelta(days=1)
            response = requests.get(
                f"{self.url}?created_at=gte.{yesterday.isoformat()}&select=count",
                headers=self.headers,
                timeout=10
            )
            
            recent_posts = 0
            if response.status_code == 200:
                result = response.json()
                recent_posts = result.get("count", 0)
            
            return {
                "total_posts": total_posts,
                "posts_by_source": posts_by_source,
                "recent_posts_24h": recent_posts,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {str(e)}")
            return {
                "total_posts": 0,
                "posts_by_source": {},
                "recent_posts_24h": 0,
                "last_updated": datetime.utcnow().isoformat()
            }

# Importar timedelta
from datetime import timedelta
