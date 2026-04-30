#!/usr/bin/env python3
"""
Script para iniciar o servidor Flask do NewsAgent
"""

import sys
import os

# Adicionar paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == '__main__':
    try:
        from backend.app import app
        
        port = int(os.environ.get('PORT', 5000))
        debug = os.environ.get('FLASK_ENV', 'development') == 'development'
        
        print("🚀 INICIANDO NEWSAGENT API")
        print("=" * 50)
        print(f"📡 Servidor: http://localhost:{port}")
        print("📰 Endpoints disponíveis:")
        print("   GET  /api/news/sources - Listar fontes")
        print("   GET  /api/news/status - Status das fontes")
        print("   GET  /api/news/health - Health check")
        print("   GET  /api/news/cache - Cache local")
        print("   GET  /api/news/collect/<source>/<category> - Coletar")
        print("   POST /api/news/execute - Coleta com filtros")
        print("=" * 50)
        print("⚠️ Pressione Ctrl+C para parar")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=port, debug=debug)
        
    except ImportError as e:
        print(f"❌ Erro ao importar: {e}")
        print("🔧 Verifique se as dependências estão instaladas:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
