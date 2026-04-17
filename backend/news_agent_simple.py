import json
import os
import uuid
import time
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Adicionar diretório raiz ao path para encontrar o módulo 'core'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from core.news_utils import NewsUtils

class NewsAgentSimple:
    """Agente simplificado para coleta de notícias"""
    
    def __init__(self):
        self.cycle_id = str(uuid.uuid4())
        self.start_time = datetime.utcnow()
        self.news_utils = NewsUtils()
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
                    "url": "https://example.com/news11",
                    "source": "G1",
                    "source_domain": "g1.globo.com",
                    "published_at": datetime.utcnow().isoformat(),
                    "snippet": "Comitê de Política Monetária decidiu manter a taxa básica de juros em 13.75% ao ano.",
                    "category": "Economia",
                    "image_url": None
                },
                {
                    "title": "Tesla anuncia nova fábrica no Brasil em 2026",
                    "url": "https://example.com/news22",
                    "source": "Exame",
                    "source_domain": "exame.com.br",
                    "published_at": datetime.utcnow().isoformat(),
                    "snippet": "Empresa de Elon Musk confirmou investimento de R$ 5 bilhões em nova unidade industrial.",
                    "category": "Tech",
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
    
    def run_cycle(self) -> Dict:
        """Executa ciclo completo de coleta e publicação"""
        self.log_info("Iniciando ciclo simplificado de coleta de notícias (NewsUtils)")
        
        # Coletar notícias mock
        all_news = self.collect_mock_news()
        
        # Validar, Normalizar e Publicar usando news_utils
        for news_data in all_news:
            try:
                # 1. Normalizar
                processed = self.news_utils.normalize_news(news_data)
                
                # 2. Verificar Duplicata
                if self.news_utils.is_duplicate(processed["source_url"]):
                    self.stats["duplicates_found"] += 1
                    self.log_info(f"Duplicata pulada: {processed['title']}")
                    continue
                
                # 3. Publicar (como Draft)
                success, msg = self.news_utils.save_to_supabase(processed)
                if success:
                    self.stats["news_published"] += 1
                else:
                    self.stats["supabase_errors"] += 1
                    self.log_error(f"Falha ao salvar no Supabase: {msg}")
                    
            except Exception as e:
                self.log_error(f"Erro ao processar notícia simple: {e}")

        
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
        
        # Salvar log em arquivo (usar /tmp na Vercel)
        log_dir = "/tmp" if os.environ.get('VERCEL') else "."
        log_filename = f"news_log_simple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_path = os.path.join(log_dir, log_filename)
        
        with open(log_path, "w", encoding='utf-8') as f:
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
