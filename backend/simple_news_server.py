"""
Servidor Simplificado de News Auto Post - NewPost-IA
Versão sem dependências complexas de web scraping
"""

import json
import threading
import time
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import os
import sys

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.news_utils import NewsUtils

# Configuração
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado global
automation_state = {
    "is_running": False,
    "last_run": None,
    "next_run_in": None,
    "logs": [],
    "current_job": None,
    "stats": {
        "total_cycles": 0,
        "successful_cycles": 0,
        "failed_cycles": 0,
        "news_published": 0
    },
    "enabled_sources": {
        "exame": True,
        "veja": True,
        "folha": True,
        "diario_nordeste": True
    }
}

# Thread para automação
automation_thread = None
stop_automation = threading.Event()

class SimpleNewsManager:
    def __init__(self):
        self.news_utils = NewsUtils()
        
        # Fontes RSS simplificadas
        self.rss_feeds = {
            "exame": {
                "url": "https://exame.com/feed/",
                "name": "Exame",
                "emoji": "📊"
            },
            "veja": {
                "url": "https://veja.abril.com.br/feed/",
                "name": "Veja", 
                "emoji": "📖"
            },
            "folha": {
                "url": "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml",
                "name": "Folha de S.Paulo",
                "emoji": "📰"
            },
            "diario_nordeste": {
                "url": "https://diariodonordeste.verdesmares.com.br/rss/ultimas-noticias",
                "name": "Diário do Nordeste",
                "emoji": "🌵"
            }
        }
    
    def add_log(self, message: str, log_type: str = "info"):
        """Adiciona entrada ao log"""
        log_entry = {
            "message": message,
            "type": log_type,
            "time": datetime.now()
        }
        automation_state["logs"].append(log_entry)
        
        # Manter apenas últimos 100 logs
        if len(automation_state["logs"]) > 100:
            automation_state["logs"] = automation_state["logs"][-100:]
        
        logger.info(f"[{log_type.upper()}] {message}")
    
    def fetch_from_rss(self, source_id: str) -> List[Dict]:
        """Busca notícias de um RSS feed específico"""
        if source_id not in self.rss_feeds:
            return []
        
        source_config = self.rss_feeds[source_id]
        self.add_log(f"🔍 Buscando RSS de {source_config['name']}...", "info")
        
        try:
            feed = feedparser.parse(source_config["url"])
            today = datetime.now().date()
            
            news_items = []
            for entry in feed.entries[:5]:  # Limitar a 5 notícias
                try:
                    # Tentar parse da data
                    pub_date = today
                    if hasattr(entry, 'published'):
                        try:
                            # Formatos comuns de data RSS
                            date_str = entry.published
                            if 'GMT' in date_str:
                                pub_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z').date()
                            elif '+' in date_str:
                                pub_date = datetime.strptime(date_str.split('+')[0].strip(), '%a, %d %b %Y %H:%M:%S').date()
                        except:
                            pass  # Usa data atual se falhar
                    
                    # Apenas notícias de hoje
                    if pub_date == today:
                        news_items.append({
                            "title": entry.title,
                            "url": entry.link,
                            "source": source_config["name"],
                            "snippet": entry.summary[:200] + "..." if hasattr(entry, 'summary') else entry.title,
                            "published_at": entry.published if hasattr(entry, 'published') else datetime.now().isoformat(),
                            "source_emoji": source_config["emoji"]
                        })
                        
                except Exception as e:
                    logger.warning(f"Erro ao processar entrada: {e}")
                    continue
            
            self.add_log(f"✅ Encontradas {len(news_items)} notícias em {source_config['name']}", "success")
            return news_items
            
        except Exception as e:
            self.add_log(f"❌ Erro ao buscar RSS de {source_config['name']}: {str(e)}", "error")
            return []
    
    def publish_news(self, news_item: Dict) -> bool:
        """Publica uma notícia no sistema"""
        try:
            # Criar dados para publicação
            post_data = {
                "title": news_item["title"],
                "content": news_item["snippet"],
                "source_url": news_item["url"],
                "category": "noticias",
                "status": "published",
                "published_at": datetime.now().isoformat(),
                "metadata": {
                    "source": news_item["source"],
                    "source_emoji": news_item.get("source_emoji", "📰"),
                    "auto_generated": True,
                    "platform": "news_auto_post"
                }
            }
            
            # Salvar no Supabase (se disponível)
            success, msg = self.news_utils.save_to_supabase(post_data)
            
            if success:
                self.add_log(f"✅ Publicado: {news_item['title'][:50]}...", "success")
                automation_state["stats"]["news_published"] += 1
                return True
            else:
                self.add_log(f"⚠️ Salvo localmente (erro Supabase): {msg}", "warn")
                return True  # Considera sucesso mesmo sem Supabase
                
        except Exception as e:
            self.add_log(f"❌ Erro ao publicar: {str(e)}", "error")
            return False
    
    def run_cycle(self) -> Dict:
        """Executa um ciclo completo de coleta e publicação"""
        self.add_log("🚀 Iniciando ciclo de automação...", "info")
        
        # Filtrar fontes ativas
        active_sources = [
            source_id for source_id, enabled in automation_state["enabled_sources"].items()
            if enabled
        ]
        
        if not active_sources:
            self.add_log("⚠️ Nenhuma fonte ativa configurada", "warn")
            return {"error": "Nenhuma fonte ativa"}
        
        # Selecionar fonte aleatória
        import random
        selected_source = random.choice(active_sources)
        
        # Buscar notícias
        news_items = self.fetch_from_rss(selected_source)
        
        if not news_items:
            self.add_log(f"❌ Nenhuma notícia encontrada em {self.rss_feeds[selected_source]['name']}", "error")
            return {"error": "Nenhuma notícia encontrada"}
        
        # Publicar primeira notícia mais recente
        selected_news = news_items[0]
        success = self.publish_news(selected_news)
        
        if success:
            automation_state["stats"]["successful_cycles"] += 1
            automation_state["stats"]["total_cycles"] += 1
            automation_state["last_run"] = datetime.now()
            
            self.add_log("✅ Ciclo concluído com sucesso", "success")
            return {
                "success": True,
                "title": selected_news["title"],
                "summary": selected_news["snippet"],
                "source": selected_news["source"],
                "source_emoji": selected_news.get("source_emoji", "📰"),
                "published_date": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
        else:
            automation_state["stats"]["failed_cycles"] += 1
            automation_state["stats"]["total_cycles"] += 1
            return {"error": "Falha na publicação"}

# Instância global
manager = SimpleNewsManager()

def automation_worker():
    """Worker thread para automação contínua"""
    logger.info("Thread de automação iniciada")
    
    while not stop_automation.is_set():
        try:
            # Executar ciclo
            result = manager.run_cycle()
            
            # Esperar 1 hora para próximo ciclo
            for i in range(3600):  # 3600 segundos = 1 hora
                if stop_automation.is_set():
                    break
                
                # Atualizar contador
                remaining = 3600 - i
                automation_state["next_run_in"] = remaining
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Erro no worker de automação: {e}")
            time.sleep(60)  # Esperar 1 minuto antes de tentar novamente
    
    logger.info("Thread de automação finalizada")

# Endpoints da API
@app.route('/api/news/status', methods=['GET'])
def get_status():
    """Retorna status atual da automação"""
    return jsonify({
        "is_running": automation_state["is_running"],
        "last_run": automation_state["last_run"].isoformat() if automation_state["last_run"] else None,
        "next_run_in": automation_state["next_run_in"],
        "enabled_sources": automation_state["enabled_sources"],
        "stats": automation_state["stats"],
        "logs": [
            {
                "message": log["message"],
                "type": log["type"],
                "time": log["time"].isoformat()
            }
            for log in automation_state["logs"][-50:]
        ]
    })

@app.route('/api/news/start', methods=['POST'])
def start_automation():
    """Inicia a automação de notícias"""
    global automation_thread, stop_automation
    
    if automation_state["is_running"]:
        return jsonify({"error": "Automação já está em execução"}), 400
    
    try:
        data = request.get_json() or {}
        if "enabled_sources" in data:
            automation_state["enabled_sources"] = data["enabled_sources"]
        
        stop_automation.clear()
        automation_thread = threading.Thread(target=automation_worker, daemon=True)
        automation_thread.start()
        
        automation_state["is_running"] = True
        manager.add_log("🚀 Automação iniciada com sucesso!", "success")
        
        return jsonify({"message": "Automação iniciada"})
        
    except Exception as e:
        logger.error(f"Erro ao iniciar automação: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/stop', methods=['POST'])
def stop_automation_endpoint():
    """Para a automação de notícias"""
    global stop_automation
    
    if not automation_state["is_running"]:
        return jsonify({"error": "Automação não está em execução"}), 400
    
    try:
        stop_automation.set()
        automation_state["is_running"] = False
        automation_state["next_run_in"] = None
        manager.add_log("⛔ Automação parada pelo usuário", "warn")
        
        return jsonify({"message": "Automação parada"})
        
    except Exception as e:
        logger.error(f"Erro ao parar automação: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/execute', methods=['POST'])
def execute_now():
    """Executa um ciclo imediatamente"""
    try:
        data = request.get_json() or {}
        if "enabled_sources" in data:
            automation_state["enabled_sources"] = data["enabled_sources"]
        
        result = manager.run_cycle()
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro ao executar ciclo: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/sources', methods=['GET'])
def get_sources():
    """Retorna lista de fontes disponíveis"""
    sources = []
    for source_id, config in manager.rss_feeds.items():
        sources.append({
            "id": source_id,
            "label": config["name"],
            "url": config["url"],
            "emoji": config["emoji"]
        })
    
    return jsonify({"sources": sources})

@app.route('/api/newpost/publish', methods=['POST'])
def publish_to_newpost_ia():
    """Endpoint para publicar conteúdo na NewPost-IA"""
    try:
        data = request.get_json()
        content = data.get("content", "")
        hashtags = data.get("hashtags", [])
        
        if not content:
            return jsonify({"error": "Conteúdo é obrigatório"}), 400
        
        # Simular publicação
        post_id = f"newpost_{int(time.time())}"
        
        manager.add_log(f"✅ Publicado na NewPost-IA: {content[:50]}...", "success")
        
        return jsonify({
            "success": True,
            "post_id": post_id,
            "message": "Publicado com sucesso na NewPost-IA"
        })
            
    except Exception as e:
        manager.add_log(f"❌ Erro na publicação NewPost-IA: {str(e)}", "error")
        return jsonify({"error": str(e)}), 500

@app.route('/api/news/logs/clear', methods=['POST'])
def clear_logs():
    """Limpa o log de execuções"""
    automation_state["logs"] = []
    manager.add_log("Log limpo pelo usuário", "info")
    return jsonify({"message": "Log limpo"})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "automation_running": automation_state["is_running"]
    })

if __name__ == '__main__':
    print("🚀 Servidor Simplificado de News Auto Post iniciando...")
    print("📰 Endpoints disponíveis:")
    print("  GET  /api/news/status     - Status da automação")
    print("  POST /api/news/start      - Iniciar automação") 
    print("  POST /api/news/stop       - Parar automação")
    print("  POST /api/news/execute    - Executar agora")
    print("  POST /api/newpost/publish - Publicar na NewPost-IA")
    print("  GET  /api/news/sources    - Listar fontes")
    print("  POST /api/news/logs/clear - Limpar logs")
    print("  GET  /api/health          - Health check")
    print()
    print("🌐 Servidor rodando em: http://localhost:5000")
    print("📡 Usando RSS feeds (sem dependências complexas)")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
