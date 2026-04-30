import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Verificar se existe tabela 'profiles' (sem prefixo)
print("=== Verificando tabela 'profiles' ===")
try:
    result = supabase.table('profiles').select('*').limit(3).execute()
    print(f"✓ Tabela 'profiles' existe! {len(result.data)} registros")
    for p in result.data:
        print(f"  - ID: {p.get('id', 'N/A')[:20]}...")
        print(f"    Nome: {p.get('display_name', p.get('nome', 'N/A'))}")
        print(f"    Email: {p.get('email', 'N/A')}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Verificar se existe tabela 'posts' (sem prefixo)
print("\n=== Verificando tabela 'posts' ===")
try:
    result = supabase.table('posts').select('*').limit(3).execute()
    print(f"✓ Tabela 'posts' existe! {len(result.data)} registros")
    for p in result.data:
        print(f"  - ID: {p.get('id', 'N/A')[:20]}...")
        print(f"    Titulo: {p.get('title', p.get('titulo', 'N/A'))[:40]}")
        print(f"    Status: {p.get('status', 'N/A')}")
except Exception as e:
    print(f"✗ Erro: {e}")

# Listar todas as tabelas disponiveis
print("\n=== Listando tabelas com 'post' no nome ===")
try:
    # Nao conseguimos listar tabelas diretamente via REST API
    # Mas podemos tentar algumas tabelas comuns
    tables_to_check = ['posts', 'post', 'publications', 'content', 'feed', 'timeline']
    for table in tables_to_check:
        try:
            result = supabase.table(table).select('count').limit(1).execute()
            print(f"  ✓ {table}: existe")
        except:
            print(f"  ✗ {table}: nao existe ou sem acesso")
except Exception as e:
    print(f"Erro: {e}")
