"""
Agente de Notícias Simplificado - NewPost-IA
Versão simplificada para testes e debug
"""

import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações Supabase
SUPABASE_URL = "https://vsaqnqurdfgzvrhbvvxw.supabase.co/rest/v1/posts"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzYXFucXVyZGZnenZyaGJ2dnh3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMTQ2MDMsImV4cCI6MjA2MDU5MDYwM30.ZtJqQ7WD7Y1nG5a99nBZbdHHBrqlOHE1q7jL9lCPnno"

class NewsAgentSimple:
    """Agente simplificado para coleta de notícias"""
    
    def __init__(self):
        self.cycle_id = str(uuid.uuid4())
        self.start_time = datetime.utcnow()
        self.stats = {
            "news_collected": 0,
            "news_validated": 0,
            "news_published": 0,
            "duplicates_found": 0,
            "validation_failed": 0,
            "supabase_errors": 0,
            "sources_success": [],
            "sources_failed": [],
            "news_collected_by_source": {}
        }
        self.errors = []
        
    def log_info(self, message: str):
        """Registra informação no log"""
        logger.info(f"[{self.cycle_id[:8]}] {message}")
        
    def log_error(self, message: str, error_type: str = "general"):
        """Registra erro no log"""
        error_msg = {
            "type": error_type,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "cycle_id": self.cycle_id
        }
        self.errors.append(error_msg)
        logger.error(f"[{self.cycle_id[:8]}] ERROR: {message}")
    
    def collect_mock_news(self) -> List[Dict]:
        """Coleta notícias mock para teste"""
        try:
            self.log_info("Coletando notícias mock para teste")
            
            mock_news = [
                {
                    "title": "Banco Central mantém taxa Selic em 13.75%",
                    "url": "https://example.com/news1",
                    "source": "G1",
                    "source_domain": "g1.globo.com",
                    "published_at": datetime.utcnow().isoformat(),
                    "summary": "Comitê de Política Monetária decidiu manter a taxa básica de juros em 13.75% ao ano.",
                    "category": "Economia",
                    "author": "Redação",
                    "content_snippet": "O Comitê de Política Monetária (Copom) decidiu nesta quarta-feira manter a taxa básica de juros (Selic) em 13.75% ao ano...",
                    "image_url": None
                },
                {
                    "title": "Tesla anuncia nova fábrica no Brasil",
                    "url": "https://example.com/news2",
                    "source": "Exame",
                    "source_domain": "exame.com.br",
                    "published_at": datetime.utcnow().isoformat(),
                    "summary": "Empresa de Elon Musk confirmou investimento de R$ 5 bilhões em nova unidade industrial.",
                    "category": "Tech",
                    "author": "Redação",
                    "content_snippet": "A Tesla confirmou oficialmente nesta quinta-feira a construção de sua nova fábrica no Brasil...",
                    "image_url": None
                },
                {
                    "title": "Governo lança novo programa de auxílio",
                    "url": "https://example.com/news3",
                    "source": "Folha de S.Paulo",
                    "source_domain": "folha.uol.com.br",
                    "published_at": datetime.utcnow().isoformat(),
                    "summary": "Programa vai beneficiar mais de 10 milhões de famílias com renda de até R$ 600.",
                    "category": "Brasil",
                    "author": "Redação",
                    "content_snippet": "O governo federal lançou nesta sexta-feira um novo programa de auxílio social...",
                    "image_url": None
                }
            ]
            
            self.stats["news_collected"] = len(mock_news)
            self.stats["news_collected_by_source"]["mock"] = len(mock_news)
            self.stats["sources_success"].append("Mock News")
            
            return mock_news
            
        except Exception as e:
            self.log_error(f"Erro na coleta mock: {str(e)}", "fetch")
            return []
    
    def validate_news(self, news_data: Dict) -> Tuple[bool, List[str]]:
        """Valida dados da notícia"""
        errors = []
        
        if not news_data.get("title") or len(news_data.get("title", "")) < 10:
            errors.append("Título ausente ou muito curto")
        
        if not news_data.get("url") or not news_data["url"].startswith("https://"):
            errors.append("URL inválida")
        
        if not news_data.get("source"):
            errors.append("Fonte não identificada")
        
        summary = news_data.get("summary", "")
        if len(summary) < 50 or len(summary) > 200:
            errors.append("Summary deve ter entre 50 e 200 caracteres")
        
        return len(errors) == 0, errors
    
    def process_news(self, news_data: Dict) -> Dict:
        """Processa notícia (normalização, slug, tags, etc)"""
        try:
            # Gerar slug
            import re
            title = news_data["title"]
            slug = title.lower()
            slug = re.sub(r'[^a-z0-9]+', '-', slug)
            slug = slug[:50] + f"-{int(time.time())}"
            
            # Gerar tags
            tags = [news_data["category"].lower()]
            if "selic" in title.lower():
                tags.append("selic")
            if "tesla" in title.lower():
                tags.append("tesla")
            if "auxílio" in title.lower():
                tags.append("auxílio")
            
            # Análise de sentimento simples
            title_lower = title.lower()
            if any(word in title_lower for word in ["alta", "crescimento", "ganho", "lucro"]):
                sentiment = "positivo"
            elif any(word in title_lower for word in ["queda", "risco", "crise", "perda"]):
                sentiment = "negativo"
            else:
                sentiment = "neutro"
            
            # Score de relevância
            score = 7  # Base
            
            processed = {
                **news_data,
                "slug": slug,
                "tags": tags[:5],
                "sentiment": sentiment,
                "sentiment_confidence": 0.7,
                "relevance_score": score
            }
            
            return processed
            
        except Exception as e:
            self.log_error(f"Erro ao processar notícia: {str(e)}", "process")
            return news_data
    
    def publish_to_supabase(self, news_data: Dict) -> Tuple[bool, Optional[str]]:
        """Publica notícia no Supabase"""
        try:
            import requests
            
            payload = {
                "title": news_data["title"][:150],
                "content": news_data["summary"],
                "url_source": news_data["url"],
                "source": news_data["source"],
                "category": news_data["category"],
                "author": news_data["author"],
                "published_at": news_data["published_at"],
                "slug": news_data["slug"],
                "tags": json.dumps(news_data["tags"]),
                "sentiment": news_data["sentiment"],
                "relevance_score": news_data["relevance_score"],
                "status": "published",
                "created_at": datetime.utcnow().isoformat()
            }
            
            headers = {
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "apikey": SUPABASE_KEY,
                "Content-Type": "application/json",
                "Prefer": "return=representation"
            }
            
            response = requests.post(SUPABASE_URL, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 201:
                result = response.json()
                post_id = result.get("id")
                self.stats["news_published"] += 1
                self.log_info(f"Notícia publicada: {news_data['title']} (ID: {post_id})")
                return True, post_id
            elif response.status_code == 409:
                self.log_info(f"Notícia duplicada no Supabase: {news_data['title']}")
                return False, None
            else:
                self.stats["supabase_errors"] += 1
                self.log_error(f"Erro Supabase {response.status_code}: {response.text}", "supabase")
                return False, None
                
        except Exception as e:
            self.stats["supabase_errors"] += 1
            self.log_error(f"Exceção ao publicar no Supabase: {str(e)}", "supabase")
            return False, None
    
    def run_cycle(self) -> Dict:
        """Executa ciclo completo de coleta e publicação"""
        self.log_info("Iniciando ciclo simplificado de coleta de notícias")
        
        # Coletar notícias mock
        all_news = self.collect_mock_news()
        
        # Validar e processar
        processed_news = []
        for news_data in all_news:
            is_valid, validation_errors = self.validate_news(news_data)
            
            if is_valid:
                processed_news_data = self.process_news(news_data)
                processed_news.append(processed_news_data)
                self.stats["news_validated"] += 1
            else:
                self.stats["validation_failed"] += 1
                self.log_error(f"Validação falhou: {news_data['title']} - Erros: {validation_errors}", "validation")
        
        # Publicar notícias processadas
        for news_data in processed_news:
            success, supabase_id = self.publish_to_supabase(news_data)
            if success:
                news_data["supabase_published"] = True
                news_data["supabase_id"] = supabase_id
        
        # Gerar log final
        end_time = datetime.utcnow()
        execution_time = (end_time - self.start_time).total_seconds()
        
        log_entry = {
            "id": self.cycle_id,
            "cycle_id": self.cycle_id,
            "execution_timestamp": self.start_time.isoformat(),
            "task_name": "Coleta Simplificada - Mock News",
            "status": "success" if self.stats["news_published"] > 0 else "failed",
            
            "ESTATISTICAS": {
                **self.stats,
                "execution_time_seconds": execution_time,
                "avg_processing_time_per_news": execution_time / max(1, self.stats["news_collected"])
            },
            
            "ERROS": {
                "errors_count": len(self.errors),
                "error_details": self.errors
            },
            
            "MENSAGEM": f"Coletou {self.stats['news_collected']} notícias, publicou {self.stats['news_published']}"
        }
        
        # Salvar log em arquivo
        with open(f"news_log_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)
        
        self.log_info(f"Ciclo simplificado finalizado. Status: {log_entry['status']}")
        return log_entry

# Função principal para execução
def main():
    """Função principal para executar o agente simplificado"""
    agent = NewsAgentSimple()
    result = agent.run_cycle()
    
    print("\n=== RESUMO DA EXECUÇÃO ===")
    print(f"Status: {result['status']}")
    print(f"Notícias coletadas: {result['ESTATISTICAS']['news_collected']}")
    print(f"Notícias publicadas: {result['ESTATISTICAS']['news_published']}")
    print(f"Tempo de execução: {result['ESTATISTICAS']['execution_time_seconds']:.2f} segundos")
    print("=== FIM ===")

if __name__ == "__main__":
    main()
