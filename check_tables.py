import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Verificar detalhes dos posts em newpost_posts
print("=== Detalhes newpost_posts ===")
result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(3).execute()
for post in result.data:
    print(f"\nPost: {post['id']}")
    print(f"  Titulo: {post.get('titulo', 'N/A')}")
    print(f"  Descricao: {post.get('descricao', 'N/A')[:50]}")
    print(f"  Conteudo: {post.get('conteudo', 'N/A')[:50] if post.get('conteudo') else 'None'}")
    print(f"  Autor ID: {post.get('autor_id')}")
    print(f"  Hashtags: {post.get('hashtags')}")
    print(f"  Audio URL: {post.get('audio_url')}")
    print(f"  Criado em: {post.get('criado_em')}")

print("\n\n=== Verificando profiles para encontrar autor valido ===")
try:
    profiles = supabase.table('profiles').select('*').limit(3).execute()
    print(f"Perfis encontrados: {len(profiles.data)}")
    for profile in profiles.data:
        print(f"  - ID: {profile.get('id', 'N/A')}")
        print(f"    Nome: {profile.get('nome', profile.get('name', 'N/A'))}")
        print(f"    Email: {profile.get('email', 'N/A')}")
except Exception as e:
    print(f"Erro ao buscar profiles: {e}")
