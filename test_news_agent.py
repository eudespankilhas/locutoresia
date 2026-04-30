#!/usr/bin/env python3
"""
Script de teste para validar a implementação do NewsAgent
"""

import sys
import os

def test_imports():
    """Testa se os módulos podem ser importados"""
    print("🔍 Testando imports...")
    
    try:
        # Testa import básico
        import sqlite3
        print("✅ sqlite3 importado")
    except ImportError as e:
        print(f"❌ Erro ao importar sqlite3: {e}")
        return False
    
    try:
        import requests
        print("✅ requests importado")
    except ImportError as e:
        print(f"❌ Erro ao importar requests: {e}")
        return False
    
    try:
        import feedparser
        print("✅ feedparser importado")
    except ImportError as e:
        print(f"❌ Erro ao importar feedparser: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup importado")
    except ImportError as e:
        print(f"❌ Erro ao importar BeautifulSoup: {e}")
        return False
    
    try:
        import schedule
        print("✅ schedule importado")
    except ImportError as e:
        print(f"❌ Erro ao importar schedule: {e}")
        return False
    
    return True

def test_news_agent_basic():
    """Testa funcionalidades básicas do NewsAgent sem depender de módulos externos"""
    print("\n🧪 Testando NewsAgent básico...")
    
    try:
        # Importa o módulo
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # Mock para módulos que podem faltar
        if 'bs4' not in sys.modules:
            class MockBeautifulSoup:
                def __init__(self, *args, **kwargs):
                    pass
                def find(self, tag):
                    return None
            sys.modules['bs4'] = type('MockModule', (), {'BeautifulSoup': MockBeautifulSoup})()
        
        # Tenta importar o NewsAgent
        from news_agent import NewsAgent, DatabaseManager, SOURCES
        print("✅ NewsAgent importado")
        
        # Testa configuração de fontes
        print(f"✅ Fontes configuradas: {len(SOURCES)}")
        for source, config in SOURCES.items():
            print(f"   - {config['name']}: {len(config['categories'])} categorias")
        
        # Testa DatabaseManager
        db = DatabaseManager("test_news.db")
        print("✅ DatabaseManager criado")
        
        # Testa métodos básicos
        sources = db.get_source_status()
        print(f"✅ Status das fontes: {len(sources)}")
        
        cached = db.get_cached_news(5)
        print(f"✅ Cache recuperado: {len(cached)} notícias")
        
        # Limpa banco de teste
        if os.path.exists("test_news.db"):
            os.remove("test_news.db")
            print("✅ Banco de teste removido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do NewsAgent: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Testa se os endpoints da API foram adicionados corretamente"""
    print("\n🌐 Testando endpoints da API...")
    
    try:
        # Verifica se o backend/app.py contém os novos endpoints
        app_file = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')
        
        if not os.path.exists(app_file):
            print("❌ Arquivo backend/app.py não encontrado")
            return False
        
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica endpoints
        endpoints = [
            '/api/news/sources',
            '/api/news/execute',
            '/api/news/status',
            '/api/news/cache',
            '/api/news/collect',
            '/api/news/health'
        ]
        
        for endpoint in endpoints:
            if endpoint in content:
                print(f"✅ Endpoint {endpoint} encontrado")
            else:
                print(f"❌ Endpoint {endpoint} não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar endpoints: {e}")
        return False

def test_scheduler():
    """Testa se o scheduler foi criado corretamente"""
    print("\n⏰ Testando NewsScheduler...")
    
    try:
        scheduler_file = os.path.join(os.path.dirname(__file__), 'news_scheduler.py')
        
        if not os.path.exists(scheduler_file):
            print("❌ Arquivo news_scheduler.py não encontrado")
            return False
        
        with open(scheduler_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verifica funcionalidades
        features = [
            'class NewsScheduler',
            'def collect_news_job',
            'def setup_schedule',
            'def run_once',
            'def run_continuous'
        ]
        
        for feature in features:
            if feature in content:
                print(f"✅ {feature} encontrado")
            else:
                print(f"❌ {feature} não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar scheduler: {e}")
        return False

def main():
    """Função principal de testes"""
    print("🚀 INICIANDO TESTES DO NEWSAGENT")
    print("=" * 50)
    
    all_passed = True
    
    # Testa imports
    if not test_imports():
        all_passed = False
        print("⚠️ Alguns imports falharam, mas continuando...")
    
    # Testa NewsAgent básico
    if not test_news_agent_basic():
        all_passed = False
    
    # Testa endpoints
    if not test_api_endpoints():
        all_passed = False
    
    # Testa scheduler
    if not test_scheduler():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ NewsAgent implementado com sucesso!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima e ajuste a implementação")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
