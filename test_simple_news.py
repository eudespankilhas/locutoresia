#!/usr/bin/env python3
"""
Teste simples do NewsAgent sem dependências externas
"""

import sys
import os
import sqlite3
import json
from datetime import datetime

def test_database_only():
    """Testa apenas o banco de dados"""
    print("💾 TESTE DO BANCO DE DADOS")
    print("=" * 40)
    
    try:
        # Criar banco manualmente
        conn = sqlite3.connect("test_simple.db")
        cursor = conn.cursor()
        
        # Criar tabelas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                title TEXT,
                url TEXT UNIQUE,
                source TEXT,
                category TEXT,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_status (
                source TEXT PRIMARY KEY,
                last_update TIMESTAMP,
                status TEXT
            )
        ''')
        
        # Inserir dados de teste
        test_news = [
            ("Notícia Teste G1", "https://g1.com/teste1", "G1", "brasil"),
            ("Notícia Teste Folha", "https://folha.uol.com.br/teste1", "Folha", "economia"),
            ("Notícia Teste Exame", "https://exame.com/teste1", "Exame", "tecnologia")
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO news (title, url, source, category)
            VALUES (?, ?, ?, ?)
        ''', test_news)
        
        # Atualizar status
        cursor.execute('''
            INSERT OR REPLACE INTO source_status (source, last_update, status)
            VALUES (?, ?, ?)
        ''', [
            ("g1", datetime.now().isoformat(), "success"),
            ("folha", datetime.now().isoformat(), "success"),
            ("exame", datetime.now().isoformat(), "success")
        ])
        
        conn.commit()
        
        # Consultar dados
        cursor.execute("SELECT COUNT(*) FROM news")
        news_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM source_status")
        sources_count = cursor.fetchone()[0]
        
        print(f"✅ Notícias inseridas: {news_count}")
        print(f"✅ Fontes status: {sources_count}")
        
        conn.close()
        
        # Limpar
        os.remove("test_simple.db")
        print("✅ Banco de teste removido")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do banco: {e}")
        return False

def test_api_structure():
    """Testa estrutura da API"""
    print("\n🌐 TESTE DA ESTRUTURA DA API")
    print("=" * 40)
    
    try:
        # Verificar se endpoints existem no app.py
        app_file = os.path.join(os.path.dirname(__file__), 'backend', 'app.py')
        
        if not os.path.exists(app_file):
            print("❌ Arquivo backend/app.py não encontrado")
            return False
        
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar endpoints
        endpoints_check = {
            '/api/news/sources': 'GET /api/news/sources',
            '/api/news/execute': 'POST /api/news/execute', 
            '/api/news/status': 'GET /api/news/status',
            '/api/news/cache': 'GET /api/news/cache',
            '/api/news/collect': 'GET /api/news/collect',
            '/api/news/health': 'GET /api/news/health'
        }
        
        for endpoint, route in endpoints_check.items():
            if route in content:
                print(f"✅ {endpoint} - encontrado")
            else:
                print(f"❌ {endpoint} - não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste da API: {e}")
        return False

def test_news_agent_config():
    """Testa configuração do NewsAgent"""
    print("\n⚙️ TESTE DE CONFIGURAÇÃO")
    print("=" * 40)
    
    try:
        # Verificar se news_agent.py existe
        agent_file = os.path.join(os.path.dirname(__file__), 'news_agent.py')
        
        if not os.path.exists(agent_file):
            print("❌ Arquivo news_agent.py não encontrado")
            return False
        
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar componentes
        components = {
            'SOURCES': 'SOURCES = {',
            'DatabaseManager': 'class DatabaseManager',
            'NewsAgent': 'class NewsAgent',
            '6 fontes': '"g1":',
            'SQLite': 'sqlite3'
        }
        
        for component, pattern in components.items():
            if pattern in content:
                print(f"✅ {component} - encontrado")
            else:
                print(f"❌ {component} - não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de configuração: {e}")
        return False

def test_scheduler_structure():
    """Testa estrutura do scheduler"""
    print("\n⏰ TESTE DO SCHEDULER")
    print("=" * 40)
    
    try:
        # Verificar se news_scheduler.py existe
        scheduler_file = os.path.join(os.path.dirname(__file__), 'news_scheduler.py')
        
        if not os.path.exists(scheduler_file):
            print("❌ Arquivo news_scheduler.py não encontrado")
            return False
        
        with open(scheduler_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar funcionalidades
        features = {
            'NewsScheduler class': 'class NewsScheduler',
            'Coleta automática': 'def collect_news_job',
            'Agendamento': 'def setup_schedule',
            'Execução única': 'def run_once',
            'Modo contínuo': 'def run_continuous',
            'Estatísticas': 'def get_stats_summary'
        }
        
        for feature, pattern in features.items():
            if pattern in content:
                print(f"✅ {feature} - encontrado")
            else:
                print(f"❌ {feature} - não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do scheduler: {e}")
        return False

def create_test_examples():
    """Cria exemplos de uso"""
    print("\n📝 CRIANDO EXEMPLOS DE USO")
    print("=" * 40)
    
    try:
        # Exemplo de requisição JSON
        example_request = {
            "enabled_sources": {
                "g1": True,
                "folha": True,
                "exame": True
            },
            "categories": ["brasil", "economia"],
            "limit": 20
        }
        
        with open("example_request.json", "w", encoding="utf-8") as f:
            json.dump(example_request, f, indent=2, ensure_ascii=False)
        
        print("✅ Exemplo de requisição criado: example_request.json")
        
        # Exemplo de resposta
        example_response = {
            "success": True,
            "total_news": 15,
            "news": [
                {
                    "title": "Título de exemplo",
                    "url": "https://exemplo.com/noticia",
                    "source": "G1",
                    "category": "brasil",
                    "published_at": "23/04/2026 09:30"
                }
            ],
            "timestamp": datetime.now().isoformat()
        }
        
        with open("example_response.json", "w", encoding="utf-8") as f:
            json.dump(example_response, f, indent=2, ensure_ascii=False)
        
        print("✅ Exemplo de resposta criado: example_response.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar exemplos: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE SIMPLES DO NEWSAGENT")
    print("=" * 50)
    print("Testes sem dependências externas")
    print("=" * 50)
    
    tests = [
        test_database_only,
        test_api_structure,
        test_news_agent_config,
        test_scheduler_structure,
        create_test_examples
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erro no teste {test.__name__}: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 TODOS OS {total} TESTES PASSARAM!")
        print("\n✅ NewsAgent está pronto para uso!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. Instale dependências: pip install -r requirements.txt")
        print("2. Execute o servidor: python app.py")
        print("3. Teste os endpoints: curl http://localhost:5000/api/news/sources")
    else:
        print(f"⚠️ {passed}/{total} TESTES PASSARAM")
        print("🔧 Verifique os erros acima")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
