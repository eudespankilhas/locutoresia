"""
Debug detalhado da coleta de notícias
"""

import os
from dotenv import load_dotenv
from supabase import create_client
import requests

def debug_supabase_connection():
    """Verifica conexão e dados do Supabase"""
    
    print("🔍 DEBUG DA CONEXÃO SUPABASE")
    print("=" * 50)
    
    # Carregar variáveis
    load_dotenv('.env.local', override=True)
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    print(f"URL: {supabase_url}")
    print(f"Key: {'✓ Configurada' if service_key else '✗ Não configurada'}")
    
    if not supabase_url or not service_key:
        print("❌ Credenciais não configuradas")
        return False
    
    try:
        # Criar cliente
        supabase = create_client(supabase_url, service_key)
        print("✅ Cliente Supabase criado")
        
        # Verificar tabela news_log
        print("\n📊 VERIFICANDO TABELA news_log:")
        res = supabase.table('news_log').select('*').execute()
        
        print(f"Total de registros: {len(res.data) if res.data else 0}")
        
        if res.data:
            print("\nRegistros existentes:")
            for i, item in enumerate(res.data[:3]):  # Mostrar só 3
                print(f"  {i+1}. URL: {item.get('url', 'N/A')}")
                print(f"     Título: {item.get('titulo', 'N/A')[:50]}...")
                print(f"     Fonte: {item.get('fonte', 'N/A')}")
                print()
        
        # Testar verificação de duplicata
        print("🔍 TESTANDO VERIFICAÇÃO DE DUPLICATA:")
        test_url = "https://exemplo.com/noticia-teste"
        
        res_check = supabase.table('news_log').select('id', count='exact').eq('url', test_url).execute()
        print(f"URL teste: {test_url}")
        print(f"Existe no banco: {res_check.count > 0}")
        print(f"Count retornado: {res_check.count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_news_collection_step_by_step():
    """Testa a coleta passo a passo"""
    
    print("\n🔄 TESTE DE COLETA PASSO A PASSO")
    print("=" * 50)
    
    try:
        # 1. Chamar API de coleta
        print("1. Chamando API de coleta...")
        response = requests.post('http://127.0.0.1:5000/api/news/collect', timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('result', {})
            
            print(f"   Status: {result.get('status')}")
            print(f"   Mensagem: {result.get('MENSAGEM')}")
            
            stats = result.get('ESTATISTICAS', {})
            print(f"   Coletadas: {stats.get('news_collected', 0)}")
            print(f"   Publicadas: {stats.get('news_published', 0)}")
            print(f"   Duplicatas: {stats.get('duplicates_found', 0)}")
            print(f"   Erros: {stats.get('supabase_errors', 0)}")
            
            # 2. Verificar se algo foi adicionado ao Supabase
            print("\n2. Verificando se algo foi adicionado ao Supabase...")
            
            load_dotenv('.env.local', override=True)
            supabase_url = os.getenv("SUPABASE_URL")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            supabase = create_client(supabase_url, service_key)
            res_after = supabase.table('news_log').select('*').execute()
            
            print(f"   Total após coleta: {len(res_after.data) if res_after.data else 0}")
            
            if res_after.data:
                print("\n   Últimas notícias:")
                for i, item in enumerate(res_after.data[-3:]):  # Últimas 3
                    created = item.get('created_at', 'N/A')
                    print(f"   {i+1}. {created}")
                    print(f"      {item.get('titulo', 'N/A')[:50]}...")
                    print(f"      Fonte: {item.get('fonte', 'N/A')}")
        
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")

if __name__ == "__main__":
    debug_supabase_connection()
    test_news_collection_step_by_step()
