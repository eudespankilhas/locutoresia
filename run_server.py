#!/usr/bin/env python3
"""
Script para iniciar o servidor NewsAgent
Execute: python run_server.py
"""

import sys
import os

# Adicionar paths necessários
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'backend'))

def main():
    """Inicia o servidor Flask"""
    try:
        print("🚀 INICIANDO NEWSAGENT API")
        print("=" * 50)
        
        # Importar o app Flask
        from backend.app import app
        
        # Configurações
        port = int(os.environ.get('PORT', 5000))
        host = '0.0.0.0'
        debug = True  # Modo debug para desenvolvimento
        
        print(f"📡 Servidor: http://{host}:{port}")
        print(f"🌐 Acesse: http://localhost:{port}")
        print()
        print("📰 ENDPOINTS DISPONÍVEIS:")
        print("   GET  /api/news/sources     - Listar fontes de notícias")
        print("   GET  /api/news/status      - Status das fontes")
        print("   GET  /api/news/health      - Health check")
        print("   GET  /api/news/cache       - Cache local")
        print("   GET  /api/news/collect/<source>/<category> - Coletar notícias")
        print("   POST /api/news/execute     - Coleta com filtros")
        print()
        print("🧪 PARA TESTAR (em outro terminal):")
        print("   PowerShell: .\\test_powershell_simple.ps1")
        print("   Python: python test_api_endpoints.py")
        print()
        print("⚠️ Pressione Ctrl+C para parar o servidor")
        print("=" * 50)
        
        # Iniciar servidor
        app.run(host=host, port=port, debug=debug)
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print()
        print("🔧 SOLUÇÃO:")
        print("1. Instale as dependências:")
        print("   pip install flask beautifulsoup4 feedparser schedule requests")
        print("2. Verifique se os arquivos existem:")
        print("   - backend/app.py")
        print("   - news_agent.py")
        print("   - news_scheduler.py")
        
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        print()
        print("🔧 VERIFIQUE:")
        print("1. Se a porta 5000 está livre")
        print("2. Se as dependências estão instaladas")
        print("3. Se os arquivos do projeto existem")

if __name__ == "__main__":
    main()
