import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Verificar generated_posts
print("=== Verificando 'generated_posts' ===")
try:
    result = supabase.table('generated_posts').select('*').limit(3).execute()
    print(f"Registros: {len(result.data)}")
    for post in result.data:
        print(f"\nID: {post.get('id')}")
        for key, value in post.items():
            print(f"  {key}: {str(value)[:40] if value else 'None'}")
except Exception as e:
    print(f"Erro: {e}")

# Verificar todas as tabelas com "post" no nome
print("\n=== Tabelas com 'post' no nome ===")
tables = ['posts', 'newpost_posts', 'generated_posts', 'user_posts', 'feed', 'timeline']
for table in tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        print(f"OK: {table} - {len(result.data)} amostras")
        if result.data:
            print(f"  Campos: {', '.join(result.data[0].keys())[:80]}")
    except Exception as e:
        if 'Could not find' in str(e):
            print(f"NAO EXISTE: {table}")
        else:
            print(f"ERRO em {table}: {str(e)[:50]}")
