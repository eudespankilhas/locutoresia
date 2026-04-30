import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Testando acesso com ANON KEY (simulando interface) ===")
# Tentar acessar com anon key
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo"
supabase_anon = create_client(os.environ['SUPABASE_URL'], anon_key)

try:
    result = supabase_anon.table('newpost_posts').select('*').limit(3).execute()
    print(f"Anon key conseguiu ler {len(result.data)} posts")
    for post in result.data:
        print(f"  - {post.get('titulo', 'N/A')[:40]}")
except Exception as e:
    print(f"Erro com anon key: {e}")

print("\n=== Testando acesso com SERVICE KEY ===")
try:
    result = supabase.table('newpost_posts').select('*').limit(3).execute()
    print(f"Service key conseguiu ler {len(result.data)} posts")
    for post in result.data:
        print(f"  - {post.get('titulo', 'N/A')[:40]}")
except Exception as e:
    print(f"Erro com service key: {e}")

print("\n=== Verificando se há campo 'publicado' ou similar ===")
result = supabase.table('newpost_posts').select('*').limit(1).execute()
if result.data:
    post = result.data[0]
    print("Campos no post:")
    for key, value in post.items():
        print(f"  {key}: {type(value).__name__} = {str(value)[:30] if value else 'None'}")
