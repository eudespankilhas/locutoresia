import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Verificando tabela newpost_posts ===")
# Buscar posts recentes em newpost_posts
result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()
print(f"Total em newpost_posts: {len(result.data)}")
for post in result.data:
    print(f"  - ID: {post['id'][:8]}... | Titulo: {post.get('titulo', 'N/A')[:40]}")
    print(f"    Autor: {post.get('autor_id', 'N/A')}")
    print(f"    Criado: {post.get('criado_em', 'N/A')}")
    print()

print("\n=== Verificando tabela posts (voxcraft=True, status=ready) ===")
# Buscar posts ready do NewsAgent
posts_result = supabase.table('posts').select('*').eq('status', 'ready').execute()
voxcraft_ready = [p for p in posts_result.data if p.get('metadata', {}).get('voxcraft')]
print(f"Posts ready com voxcraft=True: {len(voxcraft_ready)}")
for post in voxcraft_ready[:3]:
    print(f"  - ID: {post['id'][:8]}... | Titulo: {post.get('title', 'N/A')[:40]}")
    print(f"    Status: {post.get('status')}")
    print()

print("\n=== Analisando estrutura newpost_posts ===")
if result.data:
    post = result.data[0]
    print("Campos disponiveis:")
    for key in post.keys():
        value = post[key]
        value_str = str(value)[:50] if value is not None else "None"
        print(f"  - {key}: {value_str}")
