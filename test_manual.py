#!/usr/bin/env python3
"""
Teste manual do NewsAgent
"""

import sys
import os

# Adicionar path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_news_agent_manual():
    """Teste manual do NewsAgent"""
    print("🧪 TESTE MANUAL DO NEWSAGENT")
    print("=" * 50)
    
    try:
        from news_agent import NewsAgent
        
        # Criar agente
        agent = NewsAgent()
        print("✅ NewsAgent criado com sucesso")
        
        # Testar fontes
        sources = agent.get_sources()
        print(f"✅ Fontes disponíveis: {sources['total_sources']}")
        
        # Testar coleta do G1
        print("\n📰 Testando coleta do G1 - Brasil...")
        g1_news = agent.collect_from_source('g1', 'brasil')
        print(f"✅ Coletadas {len(g1_news)} notícias do G1")
        
        if g1_news:
            print("📝 Exemplo de notícia:")
            news = g1_news[0]
            print(f"   Título: {news.get('title', 'N/A')}")
            print(f"   Fonte: {news.get('source', 'N/A')}")
            print(f"   Categoria: {news.get('category', 'N/A')}")
            print(f"   URL: {news.get('url', 'N/A')}")
        
        # Testar cache
        print("\n💾 Testando cache local...")
        cached = agent.get_cached_news(limit=5)
        print(f"✅ Notícias em cache: {len(cached)}")
        
        # Testar status
        print("\n📊 Testando status...")
        status = agent.get_status()
        print(f"✅ Status obtido: {len(status.get('status', {}))} fontes")
        
        # Testar health check
        print("\n🏥 Testando health check...")
        health = agent.health_check()
        print(f"✅ Health: {health.get('status', 'unknown')}")
        
        print("\n🎉 TESTE MANUAL CONCLUÍDO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste manual: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scheduler_manual():
    """Teste manual do scheduler"""
    print("\n⏰ TESTE MANUAL DO SCHEDULER")
    print("=" * 50)
    
    try:
        from news_scheduler import NewsScheduler
        
        # Criar scheduler
        scheduler = NewsScheduler()
        print("✅ NewsScheduler criado com sucesso")
        
        # Testar configuração
        print(f"✅ Fontes habilitadas: {len(scheduler.config['enabled_sources'])}")
        print(f"✅ Categorias: {scheduler.config['categories']}")
        print(f"✅ Intervalo: {scheduler.config['collection_interval_minutes']} minutos")
        
        # Testar estatísticas
        stats = scheduler.get_stats_summary()
        print(f"✅ Coletas totais: {stats['total_collections']}")
        print(f"✅ Taxa de sucesso: {stats['success_rate']:.1f}%")
        
        print("\n🎉 SCHEDULER TESTADO COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste do scheduler: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO TESTES MANUAIS")
    print("=" * 50)
    
    success1 = test_news_agent_manual()
    success2 = test_scheduler_manual()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 TODOS OS TESTES MANUAIS PASSARAM!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
    print("=" * 50)
