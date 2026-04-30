"""
Teste final das correções implementadas
"""

import requests
import json

def test_news_apis():
    """Testa todas as novas APIs de notícias"""
    
    print("=" * 60)
    print("TESTE FINAL DAS CORREÇÕES")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    
    tests = [
        {
            "name": "API de Notícias Coletadas",
            "url": "/api/news/collected",
            "description": "Deve retornar notícias da tabela news_log do Supabase"
        },
        {
            "name": "API de Estatísticas",
            "url": "/api/news/statistics", 
            "description": "Deve retornar estatísticas reais do sistema"
        },
        {
            "name": "API de Status do Sistema",
            "url": "/api/system/status",
            "description": "Deve retornar status do agente e Supabase"
        },
        {
            "name": "API de Logs",
            "url": "/api/system/logs",
            "description": "Deve retornar logs dos ciclos de execução"
        }
    ]
    
    results = []
    
    for test in tests:
        print(f"\n🔍 Testando: {test['name']}")
        print(f"   URL: {base_url}{test['url']}")
        print(f"   Descrição: {test['description']}")
        
        try:
            response = requests.get(f"{base_url}{test['url']}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                success = data.get('success', False)
                
                if success:
                    print(f"   ✅ SUCESSO - Resposta OK")
                    
                    # Verificar conteúdo específico
                    if 'posts' in data:
                        print(f"   📰 Notícias encontradas: {len(data['posts'])}")
                    elif 'statistics' in data:
                        stats = data['statistics']
                        print(f"   📊 Total notícias: {stats.get('total_news', 0)}")
                        print(f"   📊 Notícias 24h: {stats.get('recent_news_24h', 0)}")
                    elif 'status' in data:
                        status = data['status']
                        print(f"   🤖 Status agente: {status.get('agent', 'N/A')}")
                        print(f"   🔗 Supabase: {'Conectado' if status.get('supabase_connected') else 'Erro'}")
                    elif 'logs' in data:
                        print(f"   📝 Logs encontrados: {len(data['logs'])}")
                        
                else:
                    print(f"   ❌ FALHA - Resposta sem sucesso")
                    print(f"   📄 Resposta: {data}")
                    
            else:
                print(f"   ❌ ERRO HTTP: {response.status_code}")
                print(f"   📄 Resposta: {response.text[:200]}")
                
        except Exception as e:
            print(f"   ❌ ERRO DE CONEXÃO: {str(e)}")
        
        results.append({
            "test": test['name'],
            "url": f"{base_url}{test['url']}",
            "status": response.status_code if 'response' in locals() else 'ERROR',
            "success": success if 'success' in locals() else False
        })
    
    print(f"\n{'='*80}")
    print("📋 RESUMO DOS TESTES:")
    print(f"{'='*80}")
    
    success_count = sum(1 for r in results if r['success'])
    total_tests = len(results)
    
    print(f"   ✅ Testes bem-sucedidos: {success_count}/{total_tests}")
    print(f"   📈 Taxa de sucesso: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print("   As correções foram implementadas com sucesso!")
        print("   Acesse http://127.0.0.1:5000/noticias para testar manualmente")
    else:
        print(f"\n⚠️  ALGUNS TESTES FALHARAM!")
        print("   Verifique os logs do servidor para mais detalhes")
    
    print(f"{'='*80}")
    
    return results

if __name__ == "__main__":
    test_news_apis()
