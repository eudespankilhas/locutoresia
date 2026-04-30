"""
Debug detalhado do problema de publicação
"""

import os
from dotenv import load_dotenv
from supabase import create_client
from backend.supabase_news_log import SupabaseNewsLog
from backend.news_utils import NewsUtils

def debug_duplicate_check():
    """Testa a verificação de duplicatas em detalhe"""
    
    print("🔍 DEBUG DA VERIFICAÇÃO DE DUPLICATAS")
    print("=" * 60)
    
    # Carregar variáveis
    load_dotenv('.env.local', override=True)
    
    # Inicializar componentes
    supabase_log = SupabaseNewsLog()
    news_utils = NewsUtils()
    
    print(f"Supabase habilitado: {supabase_log.enabled}")
    
    if not supabase_log.enabled:
        print("❌ Supabase não está habilitado!")
        return
    
    # Teste com URLs reais que o agente pode encontrar
    test_urls = [
        "https://exame.com/tecnologia/ia-teste-1",
        "https://g1.globo.com/tecnologia/noticia/2025/04/teste-2.ghtml",
        "https://folha.uol.com.br/mercado/2025/teste-3.shtml"
    ]
    
    print("\n🧪 TESTANDO VERIFICAÇÃO DE DUPLICATAS:")
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. Testando URL: {url}")
        
        # Verificar se já existe
        is_duplicate = supabase_log.ja_foi_postada(url)
        print(f"   É duplicata? {is_duplicate}")
        
        # Verificar diretamente no Supabase
        supabase_url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        supabase = create_client(supabase_url, service_key)
        
        res = supabase.table('news_log').select('id', count='exact').eq('url', url).execute()
        print(f"   Count direto: {res.count}")
        print(f"   Existe? {res.count > 0}")

def test_news_utils_save():
    """Testa o método save_to_supabase do NewsUtils"""
    
    print("\n🧪 DEBUG DO NEWSUTILS.SAVE_TO_SUPABASE")
    print("=" * 60)
    
    # Carregar variáveis
    load_dotenv('.env.local', override=True)
    
    news_utils = NewsUtils()
    
    # Criar notícia de teste
    test_news = {
        "title": "Notícia de Teste Debug",
        "content": "Conteúdo de teste para debug",
        "source_url": "https://debug-test.com/noticia-unica",
        "source": "Fonte Debug",
        "category": "Teste",
        "image_url": None
    }
    
    print(f"Testando save_to_supabase com:")
    print(f"   URL: {test_news['source_url']}")
    print(f"   Título: {test_news['title']}")
    
    try:
        success, msg = news_utils.save_to_supabase(test_news)
        print(f"   Sucesso: {success}")
        print(f"   Mensagem: {msg}")
        
        # Verificar se foi salvo
        supabase_url = os.getenv("SUPABASE_URL")
        service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        supabase = create_client(supabase_url, service_key)
        
        res = supabase.table('news_log').select('*').eq('url', test_news['source_url']).execute()
        print(f"   Salvo no banco: {len(res.data) > 0}")
        if res.data:
            print(f"   ID: {res.data[0].get('id')}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def check_supabase_logs():
    """Verifica logs de execução no Supabase"""
    
    print("\n📋 VERIFICANDO LOGS DE EXECUÇÃO")
    print("=" * 60)
    
    load_dotenv('.env.local', override=True)
    
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    supabase = create_client(supabase_url, service_key)
    
    # Verificar logs recentes
    res = supabase.table('news_cycles').select('*').order('created_at', desc=True).limit(3).execute()
    
    print(f"Total de ciclos: {len(res.data) if res.data else 0}")
    
    if res.data:
        for i, cycle in enumerate(res.data, 1):
            print(f"\n{i}. Ciclo: {cycle.get('cycle_id', 'N/A')[:8]}...")
            print(f"   Status: {cycle.get('status', 'N/A')}")
            print(f"   Data: {cycle.get('created_at', 'N/A')}")
            print(f"   Mensagem: {cycle.get('mensagem', 'N/A')}")
            
            stats = cycle.get('estatisticas', {})
            print(f"   Estatísticas:")
            print(f"     - Coletadas: {stats.get('news_collected', 0)}")
            print(f"     - Publicadas: {stats.get('news_published', 0)}")
            print(f"     - Duplicatas: {stats.get('duplicates_found', 0)}")

if __name__ == "__main__":
    debug_duplicate_check()
    test_news_utils_save()
    check_supabase_logs()
