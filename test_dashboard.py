#!/usr/bin/env python3
"""
Teste do Dashboard NewsAgent
Execute com o servidor rodando em background
"""

import requests
import json
import time
from datetime import datetime

def test_dashboard_endpoints():
    """Testa os endpoints do dashboard"""
    print("🧪 TESTE DO DASHBOARD NEWSAGENT")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Testar se servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print("✅ Servidor está rodando")
    except requests.exceptions.RequestException:
        print("❌ Servidor não está rodando. Inicie com: python backend/app.py")
        return False
    
    # Testar endpoint de trends
    try:
        print("\n📊 Testando API de Trends...")
        response = requests.get(f"{base_url}/api/advanced/trends?hours=24", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Trends funcionando")
            
            if data.get('success'):
                trends = data.get('trends', {})
                print(f"   📰 Total de notícias: {trends.get('total_news', 0)}")
                print(f"   📊 Fontes: {len(trends.get('by_source', {}))}")
                print(f"   📂 Categorias: {len(trends.get('by_category', {}))}")
                print(f"   🔥 Tópicos em alta: {len(trends.get('trending_topics', []))}")
                print(f"   🔑 Palavras-chave: {len(trends.get('global_keywords', []))}")
                
                # Mostrar exemplos
                by_source = trends.get('by_source', {})
                if by_source:
                    print(f"\n   📰 Notícias por fonte:")
                    for source, count in list(by_source.items())[:3]:
                        print(f"      - {source}: {count} notícias")
                
                trending_topics = trends.get('trending_topics', [])
                if trending_topics:
                    print(f"\n   🔥 Tópicos em alta:")
                    for i, topic in enumerate(trending_topics[:3], 1):
                        print(f"      {i}. {topic['topic']} - {topic['mentions']} menções")
                
                return True
            else:
                print(f"❌ Erro na API: {data.get('error')}")
                return False
        else:
            print(f"❌ Status HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar trends: {e}")
        return False

def test_dashboard_html():
    """Testa se o dashboard HTML está acessível"""
    try:
        print("\n🌐 Testando Dashboard HTML...")
        base_url = "http://localhost:5000"
        response = requests.get(f"{base_url}/dashboard-advanced", timeout=10)
        
        if response.status_code == 200:
            content = response.text
            if "Dashboard NewsAgent" in content and "cdn.jsdelivr.net/npm/chart.js" in content:
                print("✅ Dashboard HTML carregado com sucesso")
                print("   📊 Gráficos Chart.js integrados")
                print("   🎨 Interface responsiva carregada")
                return True
            else:
                print("❌ Dashboard HTML incompleto")
                return False
        else:
            print(f"❌ Status HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao carregar dashboard: {e}")
        return False

def show_usage_instructions():
    """Mostra instruções de uso"""
    print("\n📋 COMO USAR O DASHBOARD")
    print("=" * 50)
    
    print("\n1️⃣ Acesse o dashboard:")
    print("   http://localhost:5000/dashboard")
    
    print("\n2️⃣ Funcionalidades disponíveis:")
    print("   📊 Gráficos interativos de notícias por fonte")
    print("   📈 Análise de sentimentos (positivo/negativo/neutro)")
    print("   📂 Distribuição por categorias")
    print("   🔥 Tópicos em alta com menções")
    print("   🔑 Palavras-chave mais frequentes")
    print("   ⏰ Filtro por período (6h a 72h)")
    
    print("\n3️⃣ Atualização automática:")
    print("   🔄 Atualiza a cada 5 minutos automaticamente")
    print("   🔄 Botão de atualização manual")
    
    print("\n4️⃣ API de Trends (para desenvolvedores):")
    print("   GET /api/advanced/trends?hours=24")
    print("   Retorna JSON com todas as análises")
    
    print("\n5️⃣ Requisitos:")
    print("   ✅ Servidor Flask rodando")
    print("   ✅ Banco de dados com notícias")
    print("   ✅ Conexão com internet para gráficos Chart.js")

def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO DO DASHBOARD")
    print("=" * 50)
    
    # Testar endpoints
    trends_ok = test_dashboard_endpoints()
    html_ok = test_dashboard_html()
    
    # Mostrar instruções
    show_usage_instructions()
    
    # Resumo
    print(f"\n" + "=" * 50)
    if trends_ok and html_ok:
        print("🎉 DASHBOARD TESTADO COM SUCESSO!")
        print("\n✅ Acesse agora: http://localhost:5000/dashboard")
        print("✅ API Trends: http://localhost:5000/api/advanced/trends")
    else:
        print("⚠️ VERIFIQUE OS ERROS ACIMA")
        print("🔧 Certifique-se de que:")
        print("   - Servidor está rodando: python backend/app.py")
        print("   - Banco de dados existe: news_cache.db")
        print("   - Há notícias coletadas")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
