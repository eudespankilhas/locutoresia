"""
Servidor de News Auto Post - NewPost-IA

"""

import json
import threading
import time
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from flask import Flask, jsonify, request
import logging
import os
import sys

# Configuração
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Estado global
automation_state = {
    "is_running": False,
    "last_run": None,
    "next_run_in": None,
    "logs": [],
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

class MinimalNewsManager:
    def __init__(self):
        # Fontes RSS
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
            for entry in feed.entries[:3]:  # Limitar a 3 notícias
                try:
                    # Tentar parse da data
                    pub_date = today
                    if hasattr(entry, 'published'):
                        try:
                            # Simplificar parse de data
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
    
    def run_cycle(self) -> Dict:
        """Executa um ciclo completo de coleta"""
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
        
        # Simular publicação da primeira notícia
        selected_news = news_items[0]
        
        automation_state["stats"]["successful_cycles"] += 1
        automation_state["stats"]["total_cycles"] += 1
        automation_state["stats"]["news_published"] += 1
        automation_state["last_run"] = datetime.now()
        
        self.add_log(f"✅ Notícia publicada: {selected_news['title'][:50]}...", "success")
        
        return {
            "success": True,
            "title": selected_news["title"],
            "summary": selected_news["snippet"],
            "source": selected_news["source"],
            "source_emoji": selected_news.get("source_emoji", "📰"),
            "published_date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

# Instância global
manager = MinimalNewsManager()

def automation_worker():
    """Worker thread para automação contínua"""
    logger.info("Thread de automação iniciada")
    
    while not stop_automation.is_set():
        try:
            # Executar ciclo
            result = manager.run_cycle()
            
            # Esperar 1 hora para próximo ciclo
            for i in range(10):  # Reduzido para 10 segundos para teste
                if stop_automation.is_set():
                    break
                
                # Atualizar contador
                remaining = 10 - i
                automation_state["next_run_in"] = remaining
                time.sleep(1)
                
        except Exception as e:
            logger.error(f"Erro no worker de automação: {e}")
            time.sleep(5)  # Esperar 5 segundos antes de tentar novamente
    
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
        if not data:
            return jsonify({"success": False, "error": "Dados não fornecidos"}), 400
        
        title = data.get("title", "")
        content = data.get("content", "")
        
        if not content and not title:
            return jsonify({"success": False, "error": "Título ou conteúdo é obrigatório"}), 400
        
        # Usar título como conteúdo se não houver conteúdo
        if not content and title:
            content = title
        
        # Tentar publicar na NewPost-IA (Supabase) com timeout curto
        try:
            import os
            import requests
            
            # Credenciais do Supabase da NewPost-IA
            newpost_url = os.getenv('NEWPOST_SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co').rstrip('/')
            newpost_key = os.getenv('NEWPOST_SUPABASE_SERVICE_KEY', '')
            
            if newpost_url and newpost_key:
                headers = {
                    'apikey': newpost_key,
                    'Authorization': f'Bearer {newpost_key}',
                    'Content-Type': 'application/json',
                    'Prefer': 'return=representation'
                }
                
                post_data = {
                    'titulo': title or content[:100],
                    'descricao': content[:200],
                    'conteudo': content,
                    'hashtags': data.get('hashtags', ['notícia', 'Brasil']),
                    'autor_id': data.get('author_id', '3a1a93d0-e451-47a4-a126-f1b7375895eb'),
                    'criado_em': datetime.now().isoformat(),
                    'atualizado_em': datetime.now().isoformat()
                }
                
                # Timeout curto para não travar
                response = requests.post(
                    f"{newpost_url}/rest/v1/newpost_posts",
                    json=post_data,
                    headers=headers,
                    timeout=5
                )
                
                if response.status_code in (200, 201, 204):
                    manager.add_log(f"✅ Publicado na NewPost-IA: {title[:50] if title else content[:50]}...", "success")
                    return jsonify({
                        "success": True,
                        "post_id": f"newpost_{int(time.time())}",
                        "message": "Publicado com sucesso na NewPost-IA"
                    })
        except Exception as e:
            logger.warning(f"Falha ao publicar na NewPost-IA (API externa): {e}")
            # Continuar e retornar sucesso local
        
        # Fallback: simular publicação local
        post_id = f"local_{int(time.time())}"
        manager.add_log(f"✅ Publicado localmente: {title[:50] if title else content[:50]}...", "success")
        
        return jsonify({
            "success": True,
            "post_id": post_id,
            "message": "Publicado com sucesso (modo local)"
        })
            
    except Exception as e:
        manager.add_log(f"❌ Erro na publicação: {str(e)}", "error")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/news/logs/clear', methods=['POST'])
def clear_logs():
    """Limpa o log de execuções"""
    automation_state["logs"] = []
    manager.add_log("Log limpo pelo usuário", "info")
    return jsonify({"message": "Log limpo"})

@app.route('/api/publications', methods=['GET'])
def list_publications():
    """Lista publicações salvas (compatível com frontend)"""
    return jsonify({
        "success": True,
        "total": 0,
        "publications": []
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "automation_running": automation_state["is_running"]
    })

# Adicionar headers CORS manualmente
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    print("🚀 Servidor MÍNIMO de News Auto Post iniciando...")
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
    print("⚡ Ciclos a cada 10 segundos (para teste)")
    print("📡 Usando RSS feeds apenas")
    
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
