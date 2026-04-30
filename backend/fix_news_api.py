"""
Correções para a API de notícias - Integrar com Supabase news_log
"""

import os
from flask import jsonify
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def add_news_routes(app):
    """Adiciona as rotas corrigidas para notícias com Supabase"""
    
    @app.route('/api/news/collected', methods=['GET'])
    def get_collected_news():
        """Endpoint para buscar notícias coletadas do Supabase news_log"""
        try:
            from supabase import create_client
            
            # Forçar recarregar variáveis de ambiente
            from dotenv import load_dotenv
            load_dotenv('.env.local', override=True)
            
            supabase_url = os.getenv("SUPABASE_URL")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not supabase_url or not service_key:
                return jsonify({"success": False, "error": "Credenciais Supabase não configuradas"}), 500
            
            # Criar cliente Supabase
            supabase = create_client(supabase_url, service_key)
            
            # Buscar notícias na tabela news_log (não posts!)
            response = supabase.table('news_log').select('*').order('created_at', desc=True).limit(50).execute()
            
            if response.data:
                news_list = []
                for item in response.data:
                    news_list.append({
                        'id': item.get('id'),
                        'title': item.get('titulo'),
                        'content': f"Fonte: {item.get('fonte', 'Desconhecida')} | Categoria: {item.get('categoria', 'Geral')}",
                        'category': item.get('categoria'),
                        'created_at': item.get('created_at'),
                        'status': item.get('status', 'publicada'),
                        'metadata': {
                            'source': item.get('fonte'),
                            'url': item.get('url'),
                            'agent': item.get('agente_origem')
                        }
                    })
                
                return jsonify({
                    "success": True,
                    "posts": news_list,
                    "count": len(news_list)
                })
            else:
                return jsonify({
                    "success": True,
                    "posts": [],
                    "count": 0
                })
                
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/news/statistics', methods=['GET'])
    def get_news_statistics():
        """Endpoint para obter estatísticas reais do Supabase"""
        try:
            from supabase import create_client
            
            # Forçar recarregar variáveis de ambiente
            from dotenv import load_dotenv
            load_dotenv('.env.local', override=True)
            
            supabase_url = os.getenv("SUPABASE_URL")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not supabase_url or not service_key:
                return jsonify({"success": False, "error": "Credenciais Supabase não configuradas"}), 500
            
            supabase = create_client(supabase_url, service_key)
            
            # Estatísticas das notícias
            total_response = supabase.table('news_log').select('id', count='exact').execute()
            total_news = total_response.count or 0
            
            # Notícias por fonte
            fontes_response = supabase.table('news_log').select('fonte', count='exact').execute()
            news_by_source = {}
            if fontes_response.data:
                for item in fontes_response.data:
                    fonte = item.get('fonte', 'Desconhecida')
                    news_by_source[fonte] = news_by_source.get(fonte, 0) + 1
            
            # Notícias recentes (últimas 24h)
            from datetime import datetime, timedelta
            yesterday = datetime.utcnow() - timedelta(days=1)
            recent_response = supabase.table('news_log').select('id', count='exact').gte('created_at', yesterday.isoformat()).execute()
            recent_news = recent_response.count or 0
            
            # Estatísticas dos ciclos
            cycles_response = supabase.table('news_cycles').select('id', count='exact').execute()
            total_cycles = cycles_response.count or 0
            
            return jsonify({
                "success": True,
                "statistics": {
                    "total_news": total_news,
                    "recent_news_24h": recent_news,
                    "news_by_source": news_by_source,
                    "total_cycles": total_cycles
                }
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/system/status', methods=['GET'])
    def get_system_status():
        """Endpoint para obter status completo do sistema"""
        try:
            from supabase import create_client
            
            # Forçar recarregar variáveis de ambiente
            from dotenv import load_dotenv
            load_dotenv('.env.local', override=True)
            
            supabase_url = os.getenv("SUPABASE_URL")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not supabase_url or not service_key:
                return jsonify({"success": False, "error": "Credenciais Supabase não configuradas"}), 500
            
            supabase = create_client(supabase_url, service_key)
            
            # Verificar última execução do agente
            cycles_response = supabase.table('news_cycles').select('*').order('created_at', desc=True).limit(1).execute()
            last_cycle = cycles_response.data[0] if cycles_response.data else None
            
            # Verificar notícias recentes
            from datetime import datetime, timedelta
            last_24h = datetime.utcnow() - timedelta(hours=24)
            recent_news_response = supabase.table('news_log').select('id', count='exact').gte('created_at', last_24h.isoformat()).execute()
            recent_news_count = recent_news_response.count or 0
            
            # Status do agente
            agent_status = "OK"
            if last_cycle:
                if last_cycle.get('status') == 'failed':
                    agent_status = "Com Erros"
                elif recent_news_count == 0:
                    agent_status = "Inativo"
                else:
                    agent_status = "Ativo"
            else:
                agent_status = "Nunca Executado"
            
            return jsonify({
                "success": True,
                "status": {
                    "agent": agent_status,
                    "last_cycle": last_cycle,
                    "recent_news_24h": recent_news_count,
                    "supabase_connected": True
                }
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    
    @app.route('/api/system/logs', methods=['GET'])
    def get_system_logs():
        """Endpoint para obter logs do sistema"""
        try:
            from supabase import create_client
            
            # Forçar recarregar variáveis de ambiente
            from dotenv import load_dotenv
            load_dotenv('.env.local', override=True)
            
            supabase_url = os.getenv("SUPABASE_URL")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not supabase_url or not service_key:
                return jsonify({"success": False, "error": "Credenciais Supabase não configuradas"}), 500
            
            supabase = create_client(supabase_url, service_key)
            
            # Buscar últimos ciclos com logs
            cycles_response = supabase.table('news_cycles').select('*').order('created_at', desc=True).limit(10).execute()
            
            logs = []
            for cycle in cycles_response.data:
                logs.append({
                    'cycle_id': cycle.get('cycle_id'),
                    'timestamp': cycle.get('created_at'),
                    'status': cycle.get('status'),
                    'task_name': cycle.get('task_name'),
                    'statistics': cycle.get('estatisticas'),
                    'message': cycle.get('mensagem'),
                    'errors': cycle.get('erros', {}).get('error_details', [])
                })
            
            return jsonify({
                "success": True,
                "logs": logs,
                "count": len(logs)
            })
            
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

def update_noticias_html():
    """Atualiza o template noticias.html para usar as novas APIs"""
    
    html_content = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notícias - Locutores IA</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-microphone-alt me-2"></i>Locutores IA
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/"><i class="fas fa-home me-1"></i>Início</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/busca"><i class="fas fa-search me-1"></i>Busca</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" href="/noticias"><i class="fas fa-newspaper me-1"></i>Notícias</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/minidaw" target="_blank"><i class="fas fa-music me-1"></i>MiniDAW</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/painel"><i class="fas fa-tachometer-alt me-1"></i>Painel</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contato"><i class="fas fa-envelope me-1"></i>Contato</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Conteúdo -->
    <div class="container mt-5">
        <div class="row">
            <div class="col-12">
                <h1><i class="fas fa-newspaper me-2"></i>Notícias Coletadas</h1>
                <p class="lead">Notícias coletadas automaticamente pelo agente de IA</p>
                <div class="d-flex gap-2 mb-3">
                    <button class="btn btn-primary" onclick="loadCollectedNews()">
                        <i class="fas fa-sync me-1"></i>Atualizar
                    </button>
                    <button class="btn btn-success" onclick="showStatistics()">
                        <i class="fas fa-chart-bar me-1"></i>Estatísticas
                    </button>
                    <button class="btn btn-info" onclick="showSystemLogs()">
                        <i class="fas fa-list me-1"></i>Ver Logs
                    </button>
                </div>
            </div>
        </div>

        <div class="row mt-4">
            <div class="col-md-8" id="news-container">
                <div class="text-center py-5" id="news-loading">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                    <p class="mt-2 text-muted">Carregando notícias coletadas...</p>
                </div>
                
                <div id="no-news-message" class="alert alert-info d-none">
                    <i class="fas fa-info-circle me-2"></i>Nenhuma notícia coletada encontrada!
                </div>
                
                <div id="news-list"></div>
            </div>

            <div class="col-md-4">
                <!-- Estatísticas -->
                <div class="card">
                    <div class="card-header">
                        <h6><i class="fas fa-chart-bar me-2"></i>Estatísticas</h6>
                    </div>
                    <div class="card-body">
                        <div class="row text-center">
                            <div class="col-6">
                                <div class="border rounded p-2 mb-2">
                                    <div class="fw-bold text-primary" id="stat-total">0</div>
                                    <small>Total</small>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="border rounded p-2 mb-2">
                                    <div class="fw-bold text-success" id="stat-recent">0</div>
                                    <small>24h</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Status do Sistema -->
                <div class="card mt-4">
                    <div class="card-header">
                        <h6><i class="fas fa-cogs me-2"></i>Status do Sistema</h6>
                    </div>
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-center">
                            <span>Agente:</span>
                            <span class="badge" id="agent-status">Verificando...</span>
                        </div>
                        <div class="d-flex justify-content-between align-items-center mt-2">
                            <span>Supabase:</span>
                            <span class="badge" id="supabase-status">Verificando...</span>
                        </div>
                        <button class="btn btn-sm btn-outline-primary w-100 mt-3" onclick="updateSystemStatus()">
                            <i class="fas fa-sync me-1"></i>Atualizar Status
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Estatísticas -->
    <div class="modal fade" id="statisticsModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Estatísticas do Sistema</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="statistics-content">
                    <div class="text-center">
                        <div class="spinner-border" role="status"></div>
                        <p class="mt-2">Carregando estatísticas...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal de Logs -->
    <div class="modal fade" id="logsModal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Logs do Sistema</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="logs-content">
                    <div class="text-center">
                        <div class="spinner-border" role="status"></div>
                        <p class="mt-2">Carregando logs...</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentNews = [];

        function loadCollectedNews() {
            document.getElementById('news-loading').classList.remove('d-none');
            document.getElementById('no-news-message').classList.add('d-none');
            
            fetch('/api/news/collected')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('news-loading').classList.add('d-none');
                    
                    if (data.success && data.posts.length > 0) {
                        currentNews = data.posts;
                        renderCollectedNews(data.posts);
                        document.getElementById('stat-total').textContent = data.count;
                    } else {
                        document.getElementById('no-news-message').classList.remove('d-none');
                        document.getElementById('stat-total').textContent = '0';
                    }
                })
                .catch(err => {
                    document.getElementById('news-loading').classList.add('d-none');
                    alert('Erro ao carregar notícias!');
                    console.error(err);
                });
        }

        function renderCollectedNews(posts) {
            const list = document.getElementById('news-list');
            list.innerHTML = '';
            
            posts.forEach(post => {
                const dateHtml = new Date(post.created_at).toLocaleDateString('pt-BR');
                const card = document.createElement('div');
                card.className = 'card mb-4 border-success shadow-sm';
                card.innerHTML = `
                    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                        <span class="badge bg-dark">COLETADA</span>
                        <small>Fonte: ${post.metadata?.source || 'Desconhecida'}</small>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">${post.title}</h5>
                        <p class="text-muted mb-2"><small>Coletada em ${dateHtml} | Categoria: ${post.category || 'Geral'}</small></p>
                        <p class="card-text">${post.content}</p>
                        <div class="d-flex gap-2 mt-3">
                            <button class="btn btn-primary btn-sm" onclick="viewNewsDetails('${post.id}')">
                                <i class="fas fa-eye me-1"></i>Ver Detalhes
                            </button>
                            <a href="${post.metadata?.url || '#'}" target="_blank" class="btn btn-outline-primary btn-sm">
                                <i class="fas fa-external-link-alt me-1"></i>Ver Original
                            </a>
                        </div>
                    </div>
                `;
                list.appendChild(card);
            });
        }

        function showStatistics() {
            document.getElementById('statistics-content').innerHTML = `
                <div class="text-center">
                    <div class="spinner-border" role="status"></div>
                    <p class="mt-2">Carregando estatísticas...</p>
                </div>
            `;
            
            fetch('/api/news/statistics')
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        const stats = data.statistics;
                        document.getElementById('statistics-content').innerHTML = `
                            <div class="row">
                                <div class="col-md-6">
                                    <h6><i class="fas fa-newspaper me-2"></i>Notícias</h6>
                                    <ul class="list-unstyled">
                                        <li><strong>Total:</strong> ${stats.total_news}</li>
                                        <li><strong>Últimas 24h:</strong> ${stats.recent_news_24h}</li>
                                        <li><strong>Total de Ciclos:</strong> ${stats.total_cycles}</li>
                                    </ul>
                                </div>
                                <div class="col-md-6">
                                    <h6><i class="fas fa-chart-pie me-2"></i>Por Fonte</h6>
                                    <ul class="list-unstyled">
                                        ${Object.entries(stats.news_by_source).map(([source, count]) => 
                                            `<li><strong>${source}:</strong> ${count}</li>`
                                        ).join('')}
                                    </ul>
                                </div>
                            </div>
                        `;
                    }
                })
                .catch(err => {
                    document.getElementById('statistics-content').innerHTML = '<div class="alert alert-danger">Erro ao carregar estatísticas</div>';
                });
            
            new bootstrap.Modal(document.getElementById('statisticsModal')).show();
        }

        function showSystemLogs() {
            document.getElementById('logs-content').innerHTML = `
                <div class="text-center">
                    <div class="spinner-border" role="status"></div>
                    <p class="mt-2">Carregando logs...</p>
                </div>
            `;
            
            fetch('/api/system/logs')
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('logs-content').innerHTML = `
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Ciclo</th>
                                            <th>Status</th>
                                            <th>Data</th>
                                            <th>Tarefa</th>
                                            <th>Mensagem</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${data.logs.map(log => `
                                            <tr>
                                                <td><code>${log.cycle_id}</code></td>
                                                <td><span class="badge bg-${log.status === 'success' ? 'success' : 'danger'}">${log.status}</span></td>
                                                <td>${new Date(log.timestamp).toLocaleString('pt-BR')}</td>
                                                <td>${log.task_name}</td>
                                                <td>${log.message}</td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        `;
                    }
                })
                .catch(err => {
                    document.getElementById('logs-content').innerHTML = '<div class="alert alert-danger">Erro ao carregar logs</div>';
                });
            
            new bootstrap.Modal(document.getElementById('logsModal')).show();
        }

        function updateSystemStatus() {
            const agentStatusEl = document.getElementById('agent-status');
            const supabaseStatusEl = document.getElementById('supabase-status');
            
            agentStatusEl.textContent = 'Atualizando...';
            agentStatusEl.className = 'badge bg-warning';
            supabaseStatusEl.textContent = 'Verificando...';
            supabaseStatusEl.className = 'badge bg-warning';
            
            fetch('/api/system/status')
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        const status = data.status;
                        
                        // Status do agente
                        agentStatusEl.textContent = status.agent;
                        if (status.agent === 'OK') {
                            agentStatusEl.className = 'badge bg-success';
                        } else if (status.agent === 'Com Erros') {
                            agentStatusEl.className = 'badge bg-danger';
                        } else {
                            agentStatusEl.className = 'badge bg-warning';
                        }
                        
                        // Status do Supabase
                        supabaseStatusEl.textContent = status.supabase_connected ? 'Conectado' : 'Erro';
                        supabaseStatusEl.className = status.supabase_connected ? 'badge bg-success' : 'badge bg-danger';
                        
                        // Atualizar estatísticas
                        document.getElementById('stat-recent').textContent = status.recent_news_24h;
                    }
                })
                .catch(err => {
                    agentStatusEl.textContent = 'Erro';
                    agentStatusEl.className = 'badge bg-danger';
                    supabaseStatusEl.textContent = 'Erro';
                    supabaseStatusEl.className = 'badge bg-danger';
                });
        }

        function viewNewsDetails(newsId) {
            const news = currentNews.find(n => n.id === newsId);
            if (!news) return;
            
            alert(`Detalhes da Notícia:\\n\\nTítulo: ${news.title}\\nFonte: ${news.metadata?.source}\\nCategoria: ${news.category}\\nColetada em: ${new Date(news.created_at).toLocaleString('pt-BR')}\\n\\nURL: ${news.metadata?.url}`);
        }

        // Carregar notícias ao abrir a página
        document.addEventListener('DOMContentLoaded', function() {
            loadCollectedNews();
            updateSystemStatus();
        });
    </script>
</body>
</html>'''
    
    with open('templates/noticias_fixed.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ Template noticias_fixed.html criado com as correções!")
    print("  Substitua o templates/noticias.html por este arquivo")

if __name__ == "__main__":
    update_noticias_html()
