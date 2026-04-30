#!/usr/bin/env python3
"""
Teste dos endpoints da API NewsAgent
"""

import requests
import json
import time

def test_api_endpoints():
    """Testa todos os endpoints da API"""
    print("🌐 TESTANDO ENDPOINTS DA API NEWSAGENT")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Testar se servidor está rodando
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor Flask está rodando")
        else:
            print("❌ Servidor não está respondendo corretamente")
            return False
    except requests.exceptions.RequestException:
        print("❌ Servidor não está rodando. Inicie com: python app.py")
        return False
    
    # Testar endpoints
    endpoints = [
        {
            "method": "GET",
            "url": "/api/news/sources",
            "description": "Listar fontes disponíveis"
        },
        {
            "method": "GET", 
            "url": "/api/news/status",
            "description": "Verificar status das fontes"
        },
        {
            "method": "GET",
            "url": "/api/news/health",
            "description": "Health check do serviço"
        },
        {
            "method": "GET",
            "url": "/api/news/cache?limit=5",
            "description": "Obter notícias em cache"
        },
        {
            "method": "GET",
            "url": "/api/news/collect/g1/brasil",
            "description": "Coletar notícias do G1 - Brasil"
        }
    ]
    
    results = []
    
    for endpoint in endpoints:
        try:
            print(f"\n🔍 Testando: {endpoint['description']}")
            print(f"   {endpoint['method']} {endpoint['url']}")
            
            if endpoint['method'] == 'GET':
                response = requests.get(f"{base_url}{endpoint['url']}", timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Sucesso: {data.get('success', False)}")
                
                # Mostrar informações específicas
                if 'sources' in endpoint['url']:
                    sources = data.get('sources', [])
                    print(f"   📰 Fontes: {len(sources)}")
                    for source in sources[:2]:  # Mostra 2 exemplos
                        print(f"      - {source['label']}: {len(source['categories'])} categorias")
                
                elif 'cache' in endpoint['url']:
                    cached = data.get('total_cached', 0)
                    print(f"   💾 Notícias em cache: {cached}")
                
                elif 'collect' in endpoint['url']:
                    total = data.get('total', 0)
                    print(f"   📰 Notícias coletadas: {total}")
                
                elif 'health' in endpoint['url']:
                    status = data.get('status', 'unknown')
                    print(f"   🏥 Status: {status}")
                
                results.append(True)
                
            else:
                print(f"   ❌ Erro: {response.text}")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            results.append(False)
    
    # Testar POST endpoint
    try:
        print(f"\n🔍 Testando: Coleta com filtros")
        print(f"   POST /api/news/execute")
        
        payload = {
            "enabled_sources": {
                "g1": True,
                "folha": True
            },
            "categories": ["brasil"],
            "limit": 10
        }
        
        response = requests.post(
            f"{base_url}/api/news/execute", 
            json=payload, 
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Sucesso: {data.get('success', False)}")
            print(f"   📰 Notícias coletadas: {data.get('total_news', 0)}")
            
            # Mostrar estatísticas
            stats = data.get('collection_stats', {})
            for source, stat in stats.items():
                collected = stat.get('collected', 0)
                print(f"      - {source}: {collected} notícias")
            
            results.append(True)
        else:
            print(f"   ❌ Erro: {response.text}")
            results.append(False)
            
    except Exception as e:
        print(f"   ❌ Exceção: {e}")
        results.append(False)
    
    # Resumo
    passed = sum(results)
    total = len(results)
    
    print(f"\n" + "=" * 50)
    print(f"📊 RESUMO: {passed}/{total} endpoints funcionando")
    
    if passed == total:
        print("🎉 TODOS OS ENDPOINTS ESTÃO FUNCIONANDO!")
        print("\n✅ NewsAgent API está pronta para uso!")
    else:
        print("⚠️ Alguns endpoints precisam de atenção")
    
    return passed == total

def show_usage_examples():
    """Mostra exemplos de uso"""
    print("\n📚 EXEMPLOS DE USO")
    print("=" * 50)
    
    examples = [
        {
            "title": "Listar fontes disponíveis",
            "command": "curl http://localhost:5000/api/news/sources"
        },
        {
            "title": "Coletar notícias do G1",
            "command": "curl http://localhost:5000/api/news/collect/g1/brasil"
        },
        {
            "title": "Ver status das fontes", 
            "command": "curl http://localhost:5000/api/news/status"
        },
        {
            "title": "Coleta com filtros (POST)",
            "command": '''curl -X POST http://localhost:5000/api/news/execute \\
  -H "Content-Type: application/json" \\
  -d '{"enabled_sources": {"g1": true, "folha": true}, "categories": ["brasil"], "limit": 20}' '''
        },
        {
            "title": "Obter cache local",
            "command": "curl 'http://localhost:5000/api/news/cache?limit=10'"
        },
        {
            "title": "Health check",
            "command": "curl http://localhost:5000/api/news/health"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}:")
        print(f"   {example['command']}")

def main():
    """Função principal"""
    print("🚀 TESTE COMPLETO DA API NEWSAGENT")
    print("=" * 50)
    
    # Testar endpoints
    success = test_api_endpoints()
    
    # Mostrar exemplos
    show_usage_examples()
    
    print(f"\n" + "=" * 50)
    if success:
        print("🎉 API TESTADA COM SUCESSO!")
        print("\n📋 PRÓXIMOS PASSOS:")
        print("1. ✅ API está funcionando")
        print("2. Use os exemplos acima para testar")
        print("3. Configure o scheduler: python news_scheduler.py")
    else:
        print("⚠️ VERIFIQUE OS ERROS ACIMA")
        print("🔧 Certifique-se de que o servidor está rodando: python app.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
