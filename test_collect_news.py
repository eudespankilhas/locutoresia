import requests
import json

def test_news_collection():
    """Testa a API de coleta de notícias"""
    
    print("🔍 Testando coleta de notícias...")
    
    try:
        response = requests.post('http://127.0.0.1:5000/api/news/collect', timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API respondeu com sucesso!")
            print(f"Status: {data.get('result', {}).get('status', 'N/A')}")
            print(f"Mensagem: {data.get('result', {}).get('MENSAGEM', 'N/A')}")
            
            # Estatísticas
            stats = data.get('result', {}).get('ESTATISTICAS', {})
            print(f"\n📊 Estatísticas:")
            print(f"   - Coletadas: {stats.get('news_collected', 0)}")
            print(f"   - Publicadas: {stats.get('news_published', 0)}")
            print(f"   - Duplicatas: {stats.get('duplicates_found', 0)}")
            print(f"   - Erros: {stats.get('supabase_errors', 0)}")
            
            # Verificar se houve sucesso
            if data.get('result', {}).get('status') == 'success':
                print("\n🎉 Coleta executada com sucesso!")
            else:
                print("\n⚠️ Coleta executada com problemas")
                
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    test_news_collection()
