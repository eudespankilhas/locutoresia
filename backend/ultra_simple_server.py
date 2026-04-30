"""
Servidor Ultra Simples de News Auto Post
Versão mínima que funciona sem dependências complexas
"""

import json
import threading
import time
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Estado global
automation_state = {
    "is_running": False,
    "logs": [],
    "stats": {"news_published": 0},
    "enabled_sources": {"exame": True, "veja": True, "folha": True, "diario_nordeste": True},
    "publications": []  # Armazenamento real das publicações
}

# Adicionar headers CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/api/news/status', methods=['GET'])
def status():
    return jsonify(automation_state)

@app.route('/api/news/start', methods=['POST'])
def start():
    automation_state["is_running"] = True
    automation_state["logs"].append({"message": "Automação iniciada!", "type": "success", "time": datetime.now().isoformat()})
    return jsonify({"message": "Automação iniciada"})

@app.route('/api/news/stop', methods=['POST'])
def stop():
    automation_state["is_running"] = False
    automation_state["logs"].append({"message": "Automação parada", "type": "warn", "time": datetime.now().isoformat()})
    return jsonify({"message": "Automação parada"})

@app.route('/api/news/execute', methods=['POST'])
def execute():
    try:
        # Buscar notícias reais dos RSS feeds
        import feedparser
        import random
        
        # Fontes RSS reais
        rss_sources = {
            'exame': 'https://exame.com/feed/',
            'veja': 'https://veja.abril.com.br/feed/',
            'folha': 'https://feeds.folha.uol.com.br/emcimadahora/rss091.xml',
            'diario_nordeste': 'https://diariodonordeste.verdesmares.com.br/rss/ultimas-noticias'
        }
        
        # Escolher uma fonte aleatória
        source_id = random.choice(list(rss_sources.keys()))
        rss_url = rss_sources[source_id]
        
        # Buscar RSS
        feed = feedparser.parse(rss_url)
        
        if feed.entries and len(feed.entries) > 0:
            # Pegar notícia aleatória do feed
            entry = random.choice(feed.entries)
            
            # Mapear nomes das fontes
            source_names = {
                'exame': 'Exame',
                'veja': 'Veja',
                'folha': 'Folha de S.Paulo',
                'diario_nordeste': 'Diário do Nordeste'
            }
            
            news = {
                "success": True,
                "title": entry.title if hasattr(entry, 'title') else 'Sem título',
                "summary": entry.summary if hasattr(entry, 'summary') else entry.description if hasattr(entry, 'description') else 'Sem descrição',
                "source": source_names.get(source_id, source_id),
                "published_date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "link": entry.link if hasattr(entry, 'link') else ''
            }
            
            # Limitar tamanho do summary
            if len(news['summary']) > 200:
                news['summary'] = news['summary'][:200] + '...'
            
            automation_state["stats"]["news_published"] += 1
            automation_state["logs"].append({"message": f"Notícia REAL encontrada: {news['title'][:50]}...", "type": "success", "time": datetime.now().isoformat()})
            
            return jsonify(news)
        else:
            # Se não encontrar notícias, retornar erro
            automation_state["logs"].append({"message": f"Nenhuma notícia encontrada em {source_names.get(source_id, source_id)}", "type": "error", "time": datetime.now().isoformat()})
            return jsonify({"success": False, "error": "Nenhuma notícia encontrada"})
            
    except Exception as e:
        automation_state["logs"].append({"message": f"Erro ao buscar notícias: {str(e)}", "type": "error", "time": datetime.now().isoformat()})
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/newpost/publish', methods=['POST'])
def publish():
    try:
        # Verificar se o content-type é JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        content = data.get('content', '')
        hashtags = data.get('hashtags', [])
        
        # PUBLICAÇÃO REAL NA NEWPOST-IA
        post_id = f"real_post_{int(time.time())}"
        published_at = datetime.now().isoformat()
        
        # CONFIGURAÇÃO DO SUPABASE (NEWPOST-IA REAL)
        try:
            from newpost_config import get_newpost_config
            import requests
            
            config = get_newpost_config()
            
            # Payload para NewPost-IA
            payload = {
                "content": content,
                "hashtags": hashtags,
                "source": "News Auto Post",
                "timestamp": published_at,
                "auto_generated": True,
                "type": "news"
            }
            
            # Headers para NewPost-IA
            headers = config["headers"]
            
            # Fazer requisição REAL para NewPost-IA
            newpost_url = f"{config['url']}{config['api_endpoint']}"
            
            # Log de depuração
            automation_state["logs"].append({
                "message": f"Tentando publicar na NewPost-IA: {newpost_url}", 
                "type": "info", 
                "time": published_at
            })
            
            response = requests.post(
                newpost_url, 
                json=payload, 
                headers=headers, 
                timeout=config['timeout']
            )
            
            # Log de depuração da resposta
            automation_state["logs"].append({
                "message": f"Resposta NewPost-IA: {response.status_code} - {response.text[:100]}...", 
                "type": "info", 
                "time": published_at
            })
            
            if response.status_code == 200:
                result = response.json()
                real_post_id = result.get("id", post_id)
                
                # Criar objeto de publicação REAL
                publication = {
                    "post_id": real_post_id,
                    "content": content,
                    "hashtags": hashtags,
                    "published_to": "NewPost-IA (REAL)",
                    "published_at": published_at,
                    "status": "published",
                    "response": result
                }
                
                # Salvar publicação real no armazenamento
                automation_state["publications"].append(publication)
                
                automation_state["logs"].append({
                    "message": f"PUBLICADO NA NEWPOST-IA REAL: {content[:50]}... (ID: {real_post_id})", 
                    "type": "success", 
                    "time": published_at
                })
                
                return jsonify({
                    "success": True, 
                    "post_id": real_post_id,
                    "content": content,
                    "hashtags": hashtags,
                    "published_to": "NewPost-IA (REAL)",
                    "published_at": published_at
                })
            else:
                # Se falhar, tentar salvar localmente como fallback
                try:
                    error_detail = response.json()
                    error_msg = f"Erro NewPost-IA ({response.status_code}): {error_detail.get('message', response.text)}"
                    
                    # Se for erro de endpoint, salvar localmente
                    if "404" in str(response.status_code) or "Not Found" in response.text:
                        # Salvar localmente como fallback
                        publication = {
                            "post_id": post_id,
                            "content": content,
                            "hashtags": hashtags,
                            "published_to": "NewPost-IA (LOCAL - Tabela não encontrada)",
                            "published_at": published_at,
                            "status": "published",
                            "fallback_reason": "Tabela Supabase não existe"
                        }
                        
                        automation_state["publications"].append(publication)
                        
                        automation_state["logs"].append({
                            "message": f"API NewPost-IA não encontrada. Salvo localmente: {content[:50]}...", 
                            "type": "warning", 
                            "time": published_at
                        })
                        
                        return jsonify({
                            "success": True, 
                            "post_id": post_id,
                            "content": content,
                            "hashtags": hashtags,
                            "published_to": "NewPost-IA (LOCAL)",
                            "published_at": published_at,
                            "warning": "Tabela não encontrada no Supabase, salvo localmente"
                        })
                    
                except:
                    error_msg = f"Erro Supabase ({response.status_code}): {response.text}"
                    
                automation_state["logs"].append({
                    "message": error_msg, 
                    "type": "error", 
                    "time": published_at
                })
                return jsonify({"error": error_msg}), response.status_code
                
        except requests.exceptions.RequestException as e:
            # Se não conseguir conectar ao Supabase, mostrar erro claro
            error_msg = f"FALHA NA CONEXÃO COM SUPABASE: {str(e)}"
            automation_state["logs"].append({
                "message": error_msg, 
                "type": "error", 
                "time": published_at
            })
            return jsonify({"error": error_msg}), 500
        except Exception as e:
            # Erro ao importar configuração
            error_msg = f"ERRO DE CONFIGURAÇÃO: {str(e)}"
            automation_state["logs"].append({
                "message": error_msg, 
                "type": "error", 
                "time": published_at
            })
            return jsonify({"error": error_msg}), 500
        
        # Adicionar estatísticas
        if "auto_published" not in automation_state["stats"]:
            automation_state["stats"]["auto_published"] = 0
        automation_state["stats"]["auto_published"] += 1
        
        return jsonify({
            "success": True, 
            "post_id": post_id,
            "content": content,
            "hashtags": hashtags,
            "published_to": "Sistema Automático",
            "published_at": published_at
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/api/publications', methods=['GET'])
def get_publications():
    """Retorna todas as publicações salvas"""
    return jsonify({
        "publications": automation_state["publications"],
        "total": len(automation_state["publications"])
    })

@app.route('/api/news/sources', methods=['GET'])
def sources():
    return jsonify({
        "sources": [
            {"id": "exame", "label": "Exame", "url": "https://exame.com", "emoji": "https://exame.com"},
            {"id": "veja", "label": "Veja", "url": "https://veja.abril.com.br", "emoji": "https://veja.abril.com.br"},
            {"id": "folha", "label": "Folha de S.Paulo", "url": "https://folha.uol.com.br", "emoji": "https://folha.uol.com.br"},
            {"id": "diario_nordeste", "label": "Diário do Nordeste", "url": "https://diariodonordeste.verdesmares.com.br", "emoji": "https://diariodonordeste.verdesmares.com.br"}
        ]
    })

if __name__ == '__main__':
    print("Servidor Ultra Simples iniciando...")
    print("URL: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
