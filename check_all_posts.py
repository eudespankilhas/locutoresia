import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== TODOS os posts em newpost_posts (ordenados por data) ===")
result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).execute()
print(f"Total: {len(result.data)} posts\n")

for i, post in enumerate(result.data):
    print(f"{i+1}. {post['criado_em'][:16]} | {post['titulo'][:45]}")
    print(f"   Autor: {post['autor_id'][:20]}...")
    # Verificar se há campos adicionais
    if 'status' in post:
        print(f"   Status: {post['status']}")
    if 'publicado' in post:
        print(f"   Publicado: {post['publicado']}")
    if 'visivel' in post:
        print(f"   Visivel: {post['visivel']}")
    print()

# Verificar se nossos posts recentes estão lá
print("\n=== Buscando posts de 27/04 ===")
recent_posts = [p for p in result.data if '2026-04-27' in p['criado_em']]
print(f"Posts de 27/04: {len(recent_posts)}")
for post in recent_posts:
    print(f"  - {post['titulo'][:50]}")
