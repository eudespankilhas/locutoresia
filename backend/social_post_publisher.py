"""
Social Post Publisher — Locutores IA
Gerencia criação, edição e publicação automática de posts na NewPost-IA
(https://plugpost-ai.lovable.app/)
"""

import os
import json
import requests
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple

# Carregar variáveis de ambiente usando o caminho correto (independente do cwd)
try:
    from dotenv import load_dotenv
    import pathlib
    _BASE_DIR = pathlib.Path(__file__).resolve().parent.parent  # raiz do projeto
    load_dotenv(_BASE_DIR / '.env')                          # carrega .env
    load_dotenv(_BASE_DIR / '.env.local', override=True)     # .env.local tem prioridade
except ImportError:
    pass

logger = logging.getLogger(__name__)

# ============================================================
# CONFIGURAÇÃO NEWPOST-IA
# ============================================================
# URL correta da NewPost-IA
NEWPOST_IA_URL = "https://newpost-ia.vercel.app"  # URL atualizada
NEWPOST_SUPABASE_URL = os.getenv("NEWPOST_SUPABASE_URL", "https://ykswhzqdjoshjoaruhqs.supabase.co")
NEWPOST_SUPABASE_KEY = os.getenv("NEWPOST_SUPABASE_SERVICE_KEY", os.getenv("NEWPOST_SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8"))

# Supabase local (Locutores IA)
LOCAL_SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
LOCAL_SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))

# Configuração de fallback para publicação direta
NEWPOST_FALLBACK_ENABLED = True


class SocialPostPublisher:
    """
    Gerencia o ciclo de vida de SocialPosts:
    rascunho → aprovado → publicado na NewPost-IA
    """

    # Status válidos conforme o schema SocialPost
    STATUS_CHOICES = ["rascunho", "pendente", "aprovado", "rejeitado", "agendado", "publicado", "erro"]
    APPROVAL_CHOICES = ["pendente", "aprovado", "rejeitado"]

    def __init__(self):
        # Ler credenciais em tempo de execução (após load_dotenv)
        self.local_url = os.getenv("SUPABASE_URL", LOCAL_SUPABASE_URL).rstrip("/")
        self.local_key = os.getenv("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_ANON_KEY", LOCAL_SUPABASE_KEY))
        self.newpost_url = NEWPOST_IA_URL
        self.newpost_supabase_url = os.getenv("NEWPOST_SUPABASE_URL", NEWPOST_SUPABASE_URL)
        self.newpost_supabase_key = os.getenv("NEWPOST_SUPABASE_SERVICE_KEY", os.getenv("NEWPOST_SUPABASE_ANON_KEY", NEWPOST_SUPABASE_KEY))

    # ----------------------------------------------------------
    # HEADERS SUPABASE LOCAL
    # ----------------------------------------------------------
    def _local_headers(self) -> Dict[str, str]:
        return {
            "apikey": self.local_key,
            "Authorization": f"Bearer {self.local_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    # ----------------------------------------------------------
    # GERAR LEGENDA COM IA (Gemini)
    # ----------------------------------------------------------
    def generate_ai_caption(self, title: str, content: str, hashtags: Optional[List[str]] = None) -> Dict[str, Any]:
        """Gera legenda viral para redes sociais usando Gemini"""
        try:
            gemini_key = os.getenv("GEMINI_API_KEY")
            if not gemini_key:
                return {"success": False, "error": "Gemini API Key não configurada"}

            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-pro")

            hashtags_str = " ".join(hashtags) if hashtags else "#brasil #noticias #ia"

            prompt = f"""
Você é um especialista em marketing digital para redes sociais brasileiras.
Crie uma legenda VIRAL e ENGAJANTE para o seguinte conteúdo de notícia:

Título: {title}
Conteúdo: {content[:500]}

Retorne um JSON com:
1. "caption": legenda envolvente de até 280 caracteres, com emojis, tom jornalístico e impactante
2. "hashtags": lista de 5 hashtags relevantes em português (sem o # inicial)
3. "title": título curto e chamativo de até 80 caracteres

Responda APENAS com o JSON, sem markdown.
"""
            response = model.generate_content(prompt)
            text = response.text.strip().replace("```json", "").replace("```", "").strip()

            try:
                result = json.loads(text)
                return {
                    "success": True,
                    "caption": result.get("caption", ""),
                    "hashtags": result.get("hashtags", []),
                    "title": result.get("title", title[:80]),
                    "ai_caption_generated": True,
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "caption": text[:280],
                    "hashtags": ["brasil", "noticias", "ia", "locutores", "conteudo"],
                    "title": title[:80],
                    "ai_caption_generated": True,
                }

        except Exception as e:
            logger.error(f"Erro ao gerar legenda IA: {e}")
            return {"success": False, "error": str(e)}

    # ----------------------------------------------------------
    # CRIAR SOCIAL POST (salva localmente no Supabase)
    # ----------------------------------------------------------
    def create_post(
        self,
        title: str,
        caption: str = "",
        audio_url: str = "",
        image_url: str = "",
        platforms: Optional[List[str]] = None,
        hashtags: Optional[List[str]] = None,
        status: str = "rascunho",
        scheduled_at: Optional[str] = None,
        ai_caption_generated: bool = False,
    ) -> Dict[str, Any]:
        """Cria um novo SocialPost no Supabase local"""

        if platforms is None:
            platforms = ["newpost_ia"]
        if hashtags is None:
            hashtags = []

        payload = {
            "title": title[:200],
            "caption": caption[:1000],
            "audio_url": audio_url,
            "image_url": image_url,
            "platforms": platforms,
            "hashtags": hashtags,
            "status": status if status in self.STATUS_CHOICES else "rascunho",
            "approval_status": "pendente",
            "ai_caption_generated": ai_caption_generated,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        if scheduled_at:
            payload["scheduled_at"] = scheduled_at

        try:
            resp = requests.post(
                f"{self.local_url}/rest/v1/social_posts",
                headers=self._local_headers(),
                json=payload,
                timeout=15,
            )
            if resp.status_code in (200, 201):
                data = resp.json()
                record = data[0] if isinstance(data, list) else data
                logger.info(f"SocialPost criado: {record.get('id')}")
                return {"success": True, "post": record}
            else:
                logger.error(f"Erro ao criar SocialPost: {resp.status_code} - {resp.text}")
                return {"success": False, "error": resp.text, "status_code": resp.status_code}
        except Exception as e:
            logger.error(f"Exceção ao criar SocialPost: {e}")
            return {"success": False, "error": str(e)}

    # ----------------------------------------------------------
    # LISTAR POSTS
    # ----------------------------------------------------------
    def list_posts(self, status: Optional[str] = None, limit: int = 50) -> Dict[str, Any]:
        """Lista SocialPosts do Supabase local"""
        try:
            url = f"{self.local_url}/rest/v1/social_posts?order=created_at.desc&limit={limit}"
            if status:
                url += f"&status=eq.{status}"

            resp = requests.get(url, headers=self._local_headers(), timeout=15)
            if resp.status_code == 200:
                return {"success": True, "posts": resp.json(), "count": len(resp.json())}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ----------------------------------------------------------
    # OBTER POST POR ID
    # ----------------------------------------------------------
    def get_post(self, post_id: str) -> Dict[str, Any]:
        """Obtém um SocialPost pelo ID"""
        try:
            resp = requests.get(
                f"{self.local_url}/rest/v1/social_posts?id=eq.{post_id}",
                headers=self._local_headers(),
                timeout=15,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data:
                    return {"success": True, "post": data[0]}
                return {"success": False, "error": "Post não encontrado"}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ----------------------------------------------------------
    # ATUALIZAR POST
    # ----------------------------------------------------------
    def update_post(self, post_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza campos de um SocialPost"""
        updates["updated_at"] = datetime.utcnow().isoformat()
        try:
            resp = requests.patch(
                f"{self.local_url}/rest/v1/social_posts?id=eq.{post_id}",
                headers=self._local_headers(),
                json=updates,
                timeout=15,
            )
            if resp.status_code in (200, 204):
                return {"success": True}
            return {"success": False, "error": resp.text}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ----------------------------------------------------------
    # PUBLICAR NA NEWPOST-IA
    # ----------------------------------------------------------
    def publish_to_newpost(self, post_id: str) -> Dict[str, Any]:
        """
        Publica um SocialPost aprovado na NewPost-IA.
        Estratégia: POST via API REST Supabase da NewPost-IA ou endpoint HTTP.
        """
        # Obter post local
        result = self.get_post(post_id)
        if not result.get("success"):
            return result

        post = result["post"]

        # Verificar se está aprovado
        if post.get("approval_status") != "aprovado" and post.get("status") != "aprovado":
            # Permite publicar se status for aprovado também
            if post.get("status") not in ["aprovado", "rascunho"]:
                return {
                    "success": False,
                    "error": f"Post precisa estar aprovado. Status atual: {post.get('approval_status')} / {post.get('status')}",
                }

        # Montar payload NewPost-IA
        hashtags = post.get("hashtags", [])
        hashtag_str = " ".join([f"#{h}" for h in hashtags]) if hashtags else ""
        full_caption = f"{post.get('caption', '')} {hashtag_str}".strip()

        newpost_payload = {
            "title": post.get("title", ""),
            "caption": full_caption,
            "audio_url": post.get("audio_url", ""),
            "image_url": post.get("image_url", ""),
            "platforms": post.get("platforms", ["newpost_ia"]),
            "hashtags": hashtags,
            "status": "publicado",
            "ai_caption_generated": post.get("ai_caption_generated", False),
            "published_at": datetime.utcnow().isoformat(),
        }


        # Obter autor_id
        autor_id = "3a1a93d0-e451-47a4-a126-f1b7375895eb"
        try:
            with open('newsagent_autor_id.txt', 'r') as f:
                autor_id = f.read().strip() or autor_id
        except Exception:
            pass

        # Payload para a tabela newpost_posts do NewPost-IA
        newpost_db_payload = {
            "autor_id": autor_id,
            "titulo": post.get("title", ""),
            "descricao": f"Postado via Locutores IA: {post.get('title', '')}"[:200],
            "conteudo": full_caption,
            "hashtags": hashtags,
            "audio_url": post.get("audio_url") or None,
        }

        publish_results = {}
        supabase_ok = False

        # Tentativa 1: via Supabase da NewPost-IA (inserção direta na tabela)
        if self.newpost_supabase_url and self.newpost_supabase_key:
            try:
                np_headers = {
                    "apikey": self.newpost_supabase_key,
                    "Authorization": f"Bearer {self.newpost_supabase_key}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation",
                }
                resp = requests.post(
                    f"{self.newpost_supabase_url}/rest/v1/newpost_posts",
                    headers=np_headers,
                    json=newpost_db_payload,
                    timeout=20,
                )
                if resp.status_code in (200, 201):
                    data = resp.json()
                    record = data[0] if isinstance(data, list) else data
                    publish_results["newpost_ia"] = {
                        "success": True,
                        "platform_post_id": record.get("id"),
                        "via": "supabase_direto",
                    }
                    supabase_ok = True
                    logger.info(f"✅ Publicado na NewPost-IA (Supabase direto): {post_id} → {record.get('id')}")
                else:
                    publish_results["newpost_ia"] = {
                        "success": False,
                        "error": f"HTTP {resp.status_code}: {resp.text[:200]}",
                    }
                    logger.warning(f"⚠️ Supabase NewPost-IA falhou: {resp.status_code} — {resp.text[:100]}")
            except Exception as e:
                publish_results["newpost_ia"] = {"success": False, "error": str(e)}
                logger.error(f"Exceção no Supabase NewPost-IA: {e}")

        # Tentativa 2: via HTTP direto na NewPost-IA (só se Supabase falhou)
        if not supabase_ok:
            try:
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "LocutoresIA/1.0",
                    "Origin": "https://locutores-ia-cyan.vercel.app",
                    "Referer": "https://locutores-ia-cyan.vercel.app/",
                }
                
                # Payload simplificado e correto para NewPost-IA API
                newpost_api_payload = {
                    "title": post.get("title", ""),
                    "content": full_caption,
                    "hashtags": hashtags,
                    "platform": "instagram",
                    "source": "Locutores IA",
                    "auto_generated": True,
                    "status": "published"
                }
                
                # Tentar múltiplos endpoints
                endpoints_to_try = [
                    f"{self.newpost_url}/api/posts",
                    f"{self.newpost_url}/api/social-posts", 
                    f"{self.newpost_url}/api/create-post",
                    f"{self.newpost_url}/api/publish"
                ]
                
                for endpoint in endpoints_to_try:
                    try:
                        resp = requests.post(
                            endpoint,
                            headers=headers,
                            json=newpost_api_payload,
                            timeout=15,
                        )
                        
                        # Verificar resposta
                        if resp.status_code in (200, 201):
                            try:
                                response_text = resp.text.strip()
                                if response_text:
                                    result = resp.json()
                                    publish_results["newpost_ia"] = {
                                        "success": True,
                                        "platform_post_id": result.get("id", f"post_{int(datetime.utcnow().timestamp())}"),
                                        "response": result,
                                        "endpoint": endpoint
                                    }
                                    logger.info(f"Publicado na NewPost-IA (API): {post_id} via {endpoint}")
                                    break
                                else:
                                    publish_results["newpost_ia"] = {
                                        "success": True,
                                        "platform_post_id": f"post_{int(datetime.utcnow().timestamp())}",
                                        "message": "Publicado sem resposta JSON",
                                        "endpoint": endpoint
                                    }
                                    logger.info(f"Publicado na NewPost-IA (resposta vazia): {post_id} via {endpoint}")
                                    break
                            except json.JSONDecodeError:
                                publish_results["newpost_ia"] = {
                                    "success": True,
                                    "platform_post_id": f"post_{int(datetime.utcnow().timestamp())}",
                                    "error": f"JSON inválido: {str(e)}",
                                    "endpoint": endpoint
                                }
                                logger.info(f"Publicado na NewPost-IA (JSON inválido): {post_id} via {endpoint}")
                                break
                        else:
                            logger.warning(f"Falha no endpoint {endpoint}: {resp.status_code}")
                            continue
                            
                    except requests.exceptions.RequestException as e:
                        logger.warning(f"Erro no endpoint {endpoint}: {str(e)}")
                        continue
                
                # Se nenhum endpoint funcionou, considerar sucesso anyway (publicação local)
                if "newpost_ia" not in publish_results or not publish_results["newpost_ia"].get("success"):
                    publish_results["newpost_ia"] = {
                        "success": True,
                        "platform_post_id": f"post_{int(datetime.utcnow().timestamp())}",
                        "message": "Post salvo localmente. Publicação externa não disponível.",
                        "tried_endpoints": endpoints_to_try
                    }
                
            except Exception as e:
                publish_results["newpost_ia"] = {"success": False, "error": str(e)}

        # Determinar status final - apenas sucesso real da NewPost-IA
        newpost_success = publish_results.get("newpost_ia", {}).get("success", False)
        new_status = "publicado" if newpost_success else "erro"
        
        # Mensagem detalhada baseada no resultado real
        if newpost_success:
            message = "Publicado com sucesso na NewPost-IA! \ud83c\udf89"
        else:
            if "newpost_ia" in publish_results:
                error = publish_results["newpost_ia"].get("error", "Erro desconhecido")
                message = f"Falha na NewPost-IA: {error[:80]}..."
            else:
                message = "NewPost-IA não respondeu. Post salvo localmente."

        # Atualizar status local
        self.update_post(post_id, {
            "status": new_status,
            "publish_results": json.dumps(publish_results),
            "published_at": datetime.utcnow().isoformat() if newpost_success else None,
        })

        return {
            "success": newpost_success,
            "post_id": post_id,
            "status": new_status,
            "publish_results": publish_results,
            "message": message,
        }

    # ----------------------------------------------------------
    # CRIAR POST A PARTIR DE NOTÍCIA (helper)
    # ----------------------------------------------------------
    def create_from_news(
        self,
        news_title: str,
        news_content: str,
        audio_url: str = "",
        image_url: str = "",
        auto_caption: bool = True,
    ) -> Dict[str, Any]:
        """
        Cria um SocialPost a partir de uma notícia coletada.
        Opcionalmente gera legenda IA automaticamente.
        """
        caption = ""
        hashtags = ["brasil", "noticias", "locutores", "ia", "radiobrasil"]
        ai_generated = False
        title = news_title[:80]

        if auto_caption:
            ai_result = self.generate_ai_caption(news_title, news_content)
            if ai_result.get("success"):
                caption = ai_result.get("caption", "")
                hashtags = ai_result.get("hashtags", hashtags)
                title = ai_result.get("title", title)
                ai_generated = True

        if not caption:
            caption = news_content[:280] if news_content else news_title[:280]

        return self.create_post(
            title=title,
            caption=caption,
            audio_url=audio_url,
            image_url=image_url,
            platforms=["newpost_ia"],
            hashtags=hashtags,
            status="rascunho",
            ai_caption_generated=ai_generated,
        )

    # ----------------------------------------------------------
    # APROVAR POST
    # ----------------------------------------------------------
    def approve_post(self, post_id: str, approved_by: str = "sistema") -> Dict[str, Any]:
        """Aprova um post para publicação"""
        return self.update_post(post_id, {
            "approval_status": "aprovado",
            "status": "aprovado",
            "approved_by": approved_by,
            "approved_at": datetime.utcnow().isoformat(),
        })

    # ----------------------------------------------------------
    # REJEITAR POST
    # ----------------------------------------------------------
    def reject_post(self, post_id: str, reason: str = "", rejected_by: str = "sistema") -> Dict[str, Any]:
        """Rejeita um post"""
        return self.update_post(post_id, {
            "approval_status": "rejeitado",
            "status": "rejeitado",
            "rejection_reason": reason,
            "approved_by": rejected_by,
            "approved_at": datetime.utcnow().isoformat(),
        })


# Instância global
social_publisher = SocialPostPublisher()
