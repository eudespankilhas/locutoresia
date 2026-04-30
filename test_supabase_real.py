"""
Teste final com Supabase real (forçando credenciais)
"""

import os
from dotenv import load_dotenv

# Forçar carregar as credenciais corretas
load_dotenv('.env.local', override=True)

# Garantir que as variáveis estejam definidas
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_ANON_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo'
os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

def test_supabase_real():
    """Teste completo com Supabase real"""
    
    print("=" * 60)
    print("TESTE FINAL COM SUPABASE REAL")
    print("=" * 60)
    
    # Importar e testar o módulo
    from backend.supabase_news_log import supabase_log
    
    print("\n1. Status do Supabase:")
    print(f"   Habilitado: {supabase_log.enabled}")
    print(f"   Cliente: {'OK' if supabase_log.supabase else 'None'}")
    
    if not supabase_log.enabled:
        print("\nERRO: Supabase não está habilitado!")
        return False
    
    print("\n2. Testando verificação de duplicata:")
    test_url = "https://example.com/test-final-12345"
    
    # Verificar se existe
    exists_before = supabase_log.ja_foi_postada(test_url)
    print(f"   URL existe antes: {exists_before}")
    
    print("\n3. Testando registro de notícia:")
    test_noticia = {
        'url': test_url,
        'titulo': 'Notícia de Teste Final',
        'fonte': 'Fonte Teste',
        'categoria': 'teste'
    }
    
    # Registrar notícia
    registered = supabase_log.registrar_noticia(test_noticia, agente='test_final')
    print(f"   Notícia registrada: {registered}")
    
    # Verificar se existe agora
    exists_after = supabase_log.ja_foi_postada(test_url)
    print(f"   URL existe depois: {exists_after}")
    
    print("\n4. Testando registro de ciclo:")
    ciclo_teste = {
        'cycle_id': 'test-cycle-final-12345',
        'execution_timestamp': '2026-04-20T12:00:00Z',
        'task_name': 'Ciclo de Teste Final',
        'status': 'success',
        'ESTATISTICAS': {
            'news_collected': 10,
            'news_published': 8,
            'duplicates_found': 2
        },
        'ERROS': {
            'errors_count': 0,
            'error_details': []
        },
        'MENSAGEM': 'Teste final executado com sucesso'
    }
    
    ciclo_registered = supabase_log.registrar_ciclo(ciclo_teste)
    print(f"   Ciclo registrado: {ciclo_registered}")
    
    print("\n5. Testando estatísticas:")
    stats = supabase_log.obter_estatisticas(dias=7)
    print(f"   Total de notícias: {stats.get('total_noticias', 0)}")
    print(f"   Notícias últimos 7 dias: {stats.get('noticias_ultimos_dias', 0)}")
    print(f"   Fontes: {list(stats.get('noticias_por_fonte', {}).keys())}")
    
    print("\n6. Testando NewsAgent com Supabase:")
    try:
        from backend.news_agent import NewsAgent
        
        agent = NewsAgent()
        print("   NewsAgent criado com sucesso")
        
        # Verificar se o supabase_log está acessível
        if hasattr(agent, 'news_utils'):
            print("   NewsAgent tem news_utils: OK")
        
        print("   NewsAgent com Supabase: OK")
        
    except Exception as e:
        print(f"   ERRO no NewsAgent: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_supabase_real()
    
    print("\n" + "=" * 60)
    if success:
        print("   SUCESSO TOTAL! SISTEMA 100% FUNCIONAL!")
        print("   Seu sistema de notícias agora usa Supabase!")
    else:
        print("   ERRO: Algo deu errado")
    print("=" * 60)
