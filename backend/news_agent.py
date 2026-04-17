"""
Agente Jornalístico Automatizado - NewPost-IA
Coleta, processa e publica notícias de fontes brasileiras confiáveis
"""

import json
import uuid
import time
import requests
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import logging

# Configuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configurações Supabase
SUPABASE_URL = "https://vsaqnqurdfgzvrhbvvxw.supabase.co/rest/v1/posts"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzYXFucXVyZGZnenZyaGJ2dnh3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMTQ2MDMsImV4cCI6MjA2MDU5MDYwM30.ZtJqQ7WD7Y1nG5a99nBZbdHHBrqlOHE1q7jL9lCPnno"

# Fontes de notícias brasileiras
NEWS_SOURCES = {
    "exame": {
        "domain": "exame.com.br",
        "url": "https://www.exame.com.br",
        "categories": ["tecnologia", "negocios", "economia"],
        "name": "Exame"
    },
    "veja": {
        "domain": "veja.com.br",
        "url": "https://www.veja.com.br",
        "categories": ["economia", "politica", "brasil"],
        "name": "Veja"
    },
    "folha": {
        "domain": "folha.uol.com.br",
        "url": "https://www.folha.uol.com.br",
        "categories": ["mercado", "cotidiano", "brasil"],
        "name": "Folha de S.Paulo"
    },
    "g1": {
        "domain": "g1.globo.com",
        "url": "https://g1.globo.com",
        "categories": ["economia", "tecnologia", "brasil"],
        "name": "G1"
    }
}

class NewsAgent:
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
            "news_collected_by_source": {source: 0 for source in NEWS_SOURCES.keys()}
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
        
    def web_search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Simula busca web por notícias
        Em produção, substituir por API real de busca
        """
        try:
            # Simulação de resultados de busca
            # Em produção, usar: requests.get(f"https://api.search.com/search?q={query}")
            
            # Dados mock para demonstração
            mock_results = []
            for i in range(min(max_results, 3)):  # Limitar para demo
                mock_results.append({
                    "title": f"Notícia exemplo {i+1} - {query}",
                    "url": f"https://example.com/news{i+1}",
                    "snippet": f"Conteúdo da notícia sobre {query}...",
                    "published_at": (datetime.utcnow() - timedelta(hours=i)).isoformat()
                })
            
            return mock_results
            
        except Exception as e:
            self.log_error(f"Erro na busca web: {str(e)}", "fetch")
            return []
    
    def extract_news_data(self, result: Dict, source: str, category: str) -> Optional[Dict]:
        """Extrai e estrutura dados da notícia"""
        try:
            return {
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "source": NEWS_SOURCES[source]["name"],
                "source_domain": NEWS_SOURCES[source]["domain"],
                "published_at": result.get("published_at", ""),
                "summary": result.get("snippet", "")[:200],
                "category": category,
                "author": "Redação",  # Padrão se não informado
                "content_snippet": result.get("snippet", "")[:500],
                "image_url": None  # Seria extraído do HTML real
            }
        except Exception as e:
            self.log_error(f"Erro ao extrair dados: {str(e)}", "parse")
            return None
    
    def validate_news(self, news_data: Dict) -> Tuple[bool, List[str]]:
        """Valida dados da notícia"""
        errors = []
        
        # Validações obrigatórias
        if not news_data.get("title") or len(news_data.get("title", "")) < 10:
            errors.append("Título ausente ou muito curto")
        
        if not news_data.get("url") or not news_data["url"].startswith("https://"):
            errors.append("URL inválida")
        
        if not news_data.get("source"):
            errors.append("Fonte não identificada")
        
        # Validar data
        try:
            published_date = datetime.fromisoformat(news_data.get("published_at", "").replace("Z", "+00:00"))
            if published_date < datetime.utcnow() - timedelta(days=7):
                errors.append("Notícia muito antiga (mais de 7 dias)")
        except:
            errors.append("Data de publicação inválida")
        
        # Validar summary
        summary = news_data.get("summary", "")
        if len(summary) < 50 or len(summary) > 200:
            errors.append("Summary deve ter entre 50 e 200 caracteres")
        
        return len(errors) == 0, errors
    
    def normalize_data(self, news_data: Dict) -> Dict:
        """Normaliza dados da notícia"""
        # Normalizar título
        title = news_data["title"]
        title = re.sub(r'[^\w\s-]', '', title)  # Remove caracteres especiais
        title = title.title()  # Title Case
        title = title[:150]  # Limitar tamanho
        
        # Normalizar categoria
        category_map = {
            "tecnologia": "Tech",
            "negocios": "Negócios",
            "economia": "Economia",
            "politica": "Política",
            "brasil": "Brasil",
            "mercado": "Economia",
            "cotidiano": "Brasil"
        }
        
        normalized_category = category_map.get(news_data["category"].lower(), news_data["category"])
        
        # Gerar slug
        slug = self.generate_slug(title)
        
        # Gerar tags
        tags = self.generate_tags(title, normalized_category)
        
        # Análise de sentimento
        sentiment, confidence = self.analyze_sentiment(title + " " + news_data.get("summary", ""))
        
        # Score de relevância
        relevance_score = self.calculate_relevance_score(news_data, sentiment)
        
        return {
            **news_data,
            "title": title,
            "category": normalized_category,
            "slug": slug,
            "tags": tags,
            "sentiment": sentiment,
            "sentiment_confidence": confidence,
            "relevance_score": relevance_score
        }
    
    def generate_slug(self, title: str) -> str:
        """Gera slug único e SEO-friendly"""
        # Converter para lowercase e remover acentos
        slug = title.lower()
        slug = re.sub(r'[àáâãäå]', 'a', slug)
        slug = re.sub(r'[èéêë]', 'e', slug)
        slug = re.sub(r'[ìíîï]', 'i', slug)
        slug = re.sub(r'[òóôõö]', 'o', slug)
        slug = re.sub(r'[ùúûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = re.sub(r'^-+|-+$', '', slug)
        slug = slug[:100]
        
        # Adicionar timestamp para garantir unicidade
        timestamp = int(time.time())
        return f"{slug}-{timestamp}"
    
    def generate_tags(self, title: str, category: str) -> List[str]:
        """Gera tags automáticas baseadas no título e categoria"""
        tags = [category.lower()]  # Tag obrigatória
        
        # Extrair palavras-chave do título
        words = re.findall(r'\b\w+\b', title.lower())
        
        # Palavras-chave comuns em notícias brasileiras
        keywords = ["bolsa", "selic", "banco central", "inflação", "pib", "dólar", "euro", 
                  "petróleo", "tesouro", "lula", "governo", "congresso", "stf", "eleições"]
        
        for word in words[:3]:  # Limitar a 3 palavras principais
            if len(word) > 3 and word not in tags:
                tags.append(word)
        
        # Adicionar tag trending se for relevante
        if any(keyword in title.lower() for keyword in keywords):
            tags.append("trending")
        
        return tags[:5]  # Máximo 5 tags
    
    def analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Analisa sentimento do texto"""
        positive_words = ["alta", "crescimento", "ganho", "lucro", "aprovacao", "sucesso", "recorde", "aumento"]
        negative_words = ["queda", "risco", "crise", "perda", "demissao", "falha", "investigacao", "reducao"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positivo", min(0.9, 0.5 + (positive_count * 0.1))
        elif negative_count > positive_count:
            return "negativo", min(0.9, 0.5 + (negative_count * 0.1))
        else:
            return "neutro", 0.6
    
    def calculate_relevance_score(self, news_data: Dict, sentiment: str) -> int:
        """Calcula score de relevância (1-10)"""
        base_score = 5
        
        # Fatores positivos
        try:
            published_date = datetime.fromisoformat(news_data.get("published_at", "").replace("Z", "+00:00"))
            hours_ago = (datetime.utcnow() - published_date).total_seconds() / 3600
            
            if hours_ago <= 24:
                base_score += 2
            elif hours_ago <= 48:
                base_score += 1
                
            if news_data.get("category") in ["Tech", "Economia"]:
                base_score += 1
                
            if sentiment in ["positivo", "negativo"]:
                base_score += 1
                
            if news_data.get("source") in ["Folha de S.Paulo", "G1"]:
                base_score += 1
                
            if any(char.isdigit() for char in news_data.get("title", "")):
                base_score += 0.5
                
            if news_data.get("image_url"):
                base_score += 0.5
                
        except:
            pass
        
        return min(10, max(1, int(base_score)))
    
    def check_duplicates(self, news_data: Dict, existing_news: List[Dict]) -> bool:
        """Verifica se notícia é duplicata"""
        title = news_data.get("title", "").lower()
        url = news_data.get("url", "")
        
        for existing in existing_news:
            existing_title = existing.get("title", "").lower()
            existing_url = existing.get("url", "")
            
            # Duplicata exata
            if title == existing_title and news_data.get("source") == existing.get("source"):
                return True
            
            # Duplicata por URL
            if url == existing_url:
                return True
        
        return False
    
    def publish_to_supabase(self, news_data: Dict) -> Tuple[bool, Optional[str]]:
        """Publica notícia no Supabase"""
        try:
            payload = {
                "title": news_data["title"],
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
                self.stats["news_published"] += 1
                self.log_info(f"Notícia publicada: {news_data['title']}")
                return True, response.json().get("id")
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
    
    def collect_from_source(self, source_key: str, category: str) -> List[Dict]:
        """Coleta notícias de uma fonte específica"""
        try:
            self.log_info(f"Coletando notícias de {NEWS_SOURCES[source_key]['name']} - {category}")
            
            # Construir query de busca
            domain = NEWS_SOURCES[source_key]["domain"]
            query = f"site:{domain} {category} after:2025-04-16"
            
            # Buscar notícias
            results = self.web_search(query, max_results=5)
            
            collected_news = []
            for result in results:
                news_data = self.extract_news_data(result, source_key, category)
                if news_data:
                    collected_news.append(news_data)
                    self.stats["news_collected"] += 1
                    self.stats["news_collected_by_source"][source_key] += 1
            
            self.stats["sources_success"].append(f"{NEWS_SOURCES[source_key]['name']} - {category}")
            return collected_news
            
        except Exception as e:
            self.stats["sources_failed"].append(f"{NEWS_SOURCES[source_key]['name']} - {category}")
            self.log_error(f"Erro ao coletar de {source_key}: {str(e)}", "fetch")
            return []
    
    def run_cycle(self) -> Dict:
        """Executa ciclo completo de coleta e publicação"""
        self.log_info("Iniciando ciclo de coleta de notícias")
        
        all_news = []
        
        # Coletar de todas as fontes e categorias
        for source_key, source_config in NEWS_SOURCES.items():
            for category in source_config["categories"]:
                news_batch = self.collect_from_source(source_key, category)
                all_news.extend(news_batch)
                
                # Pequeno delay entre requisições
                time.sleep(1)
        
        # Validar e processar notícias
        processed_news = []
        for news_data in all_news:
            # Validar
            is_valid, validation_errors = self.validate_news(news_data)
            
            if is_valid:
                # Normalizar dados
                normalized_news = self.normalize_data(news_data)
                
                # Verificar duplicatas
                if not self.check_duplicates(normalized_news, processed_news):
                    processed_news.append(normalized_news)
                    self.stats["news_validated"] += 1
                else:
                    self.stats["duplicates_found"] += 1
                    self.log_info(f"Duplicata removida: {news_data['title']}")
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
            "task_name": "Coleta Multicanal - Exame, Veja, Folha, G1",
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
            
            "MENSAGEM": f"Coletou {self.stats['news_collected']} notícias, publicou {self.stats['news_published']}, removeu {self.stats['duplicates_found']} duplicatas"
        }
        
        # Salvar log em arquivo
        with open(f"news_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w", encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)
        
        self.log_info(f"Ciclo finalizado. Status: {log_entry['status']}")
        return log_entry

# Função principal para execução
def main():
    """Função principal para executar o agente de notícias"""
    agent = NewsAgent()
    result = agent.run_cycle()
    
    print("\n=== RESUMO DA EXECUÇÃO ===")
    print(f"Status: {result['status']}")
    print(f"Notícias coletadas: {result['ESTATISTICAS']['news_collected']}")
    print(f"Notícias publicadas: {result['ESTATISTICAS']['news_published']}")
    print(f"Duplicatas removidas: {result['ESTATISTICAS']['duplicates_found']}")
    print(f"Tempo de execução: {result['ESTATISTICAS']['execution_time_seconds']:.2f} segundos")
    print("=== FIM ===")

if __name__ == "__main__":
    main()
