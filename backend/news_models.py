"""
Modelos de dados para o Agente Jornalístico - NewPost-IA
"""

from datetime import datetime
from typing import List, Optional
import uuid

class NewsPost:
    """Modelo para posts de notícias"""
    
    def __init__(self, title: str, url: str, source: str, published_at: str):
        self.id = str(uuid.uuid4())
        self.title = title[:150]  # Max 150 caracteres
        self.summary = ""  # Será preenchido depois
        self.url = url
        self.source = source
        self.source_domain = self._extract_domain(url)
        self.category = ""  # Será normalizado
        self.author = "Redação"  # Padrão
        self.content_snippet = ""  # Primeiros 500 caracteres
        self.image_url = None
        self.slug = ""  # Gerado automaticamente
        self.tags = []  # Máximo 5 tags
        self.sentiment = "neutro"  # positivo|negativo|neutro
        self.sentiment_confidence = 0.5
        self.relevance_score = 5  # 1-10
        self.status = "pending"  # pending|published|failed|archived
        self.published_at = published_at
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        self.supabase_published = False
        self.supabase_id = None
        self.validation_errors = []
    
    def _extract_domain(self, url: str) -> str:
        """Extrai domínio da URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except:
            return ""
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "source": self.source,
            "source_domain": self.source_domain,
            "category": self.category,
            "author": self.author,
            "content_snippet": self.content_snippet,
            "image_url": self.image_url,
            "slug": self.slug,
            "tags": self.tags,
            "sentiment": self.sentiment,
            "sentiment_confidence": self.sentiment_confidence,
            "relevance_score": self.relevance_score,
            "status": self.status,
            "published_at": self.published_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "supabase_published": self.supabase_published,
            "supabase_id": self.supabase_id,
            "validation_errors": self.validation_errors
        }
    
    def is_valid(self) -> tuple[bool, List[str]]:
        """Valida dados do post"""
        errors = []
        
        if not self.title or len(self.title) < 10:
            errors.append("Título ausente ou muito curto")
        
        if not self.url or not self.url.startswith("https://"):
            errors.append("URL inválida")
        
        if not self.source:
            errors.append("Fonte não identificada")
        
        try:
            published_date = datetime.fromisoformat(self.published_at.replace("Z", "+00:00"))
            if published_date < datetime.utcnow() - timedelta(days=7):
                errors.append("Notícia muito antiga (mais de 7 dias)")
        except:
            errors.append("Data de publicação inválida")
        
        if len(self.summary) < 50 or len(self.summary) > 200:
            errors.append("Summary deve ter entre 50 e 200 caracteres")
        
        return len(errors) == 0, errors

class NewsLog:
    """Modelo para logs de execução do agente"""
    
    def __init__(self, cycle_id: str = None):
        self.id = str(uuid.uuid4())
        self.cycle_id = cycle_id or str(uuid.uuid4())
        self.execution_timestamp = datetime.utcnow().isoformat()
        self.task_name = ""
        self.status = "running"  # success|partial_success|failed
        
        # Estatísticas
        self.news_collected = 0
        self.news_collected_by_source = {}
        self.news_validated = 0
        self.news_published = 0
        self.duplicates_found = 0
        self.validation_failed = 0
        self.supabase_errors = 0
        
        # Performance
        self.execution_time_seconds = 0.0
        self.avg_processing_time_per_news = 0.0
        self.sources_success = []
        self.sources_failed = []
        
        # Erros
        self.errors_count = 0
        self.error_details = []
        
        # Mensagem
        self.message = ""
        self.summary = ""
    
    def add_error(self, error_type: str, message: str, source: str = None):
        """Adiciona erro ao log"""
        error_entry = {
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "source": source
        }
        self.error_details.append(error_entry)
        self.errors_count += 1
    
    def finalize(self, status: str, message: str, summary: str):
        """Finaliza log com estatísticas finais"""
        self.status = status
        self.message = message
        self.summary = summary
        
        # Calcular tempo médio
        if self.news_collected > 0:
            self.avg_processing_time_per_news = self.execution_time_seconds / self.news_collected
    
    def to_dict(self) -> dict:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "cycle_id": self.cycle_id,
            "execution_timestamp": self.execution_timestamp,
            "task_name": self.task_name,
            "status": self.status,
            
            "ESTATISTICAS": {
                "news_collected": self.news_collected,
                "news_collected_by_source": self.news_collected_by_source,
                "news_validated": self.news_validated,
                "news_published": self.news_published,
                "duplicates_found": self.duplicates_found,
                "validation_failed": self.validation_failed,
                "supabase_errors": self.supabase_errors,
                
                "PERFORMANCE": {
                    "execution_time_seconds": self.execution_time_seconds,
                    "avg_processing_time_per_news": self.avg_processing_time_per_news,
                    "sources_success": self.sources_success,
                    "sources_failed": self.sources_failed
                }
            },
            
            "ERROS": {
                "errors_count": self.errors_count,
                "error_details": self.error_details
            },
            
            "MENSAGEM": {
                "message": self.message,
                "summary": self.summary
            }
        }
    
    def save_to_file(self, filename: str = None):
        """Salva log em arquivo JSON"""
        if not filename:
            filename = f"news_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        import json
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        
        return filename

# Importar timedelta
from datetime import timedelta
