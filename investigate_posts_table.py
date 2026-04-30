import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Verificando tabela 'posts' (usada pela NewPost-IA) ===")
try:
    # Buscar posts que a NewPost-IA usaria
    result = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()
    print(f"Total de posts: {len(result.data)}")
    print()
    
    for i, post in enumerate(result.data):
        print(f"Post {i+1}:")
        print(f"  ID: {post.get('id', 'N/A')}")
        print(f"  Content: {post.get('content', 'N/A')[:50] if post.get('content') else 'None'}")
        print(f"  Created_at: {post.get('created_at', 'N/A')}")
        print(f"  Author_id: {post.get('author_id', 'N/A')}")
        print(f"  Media_urls: {post.get('media_urls', 'N/A')}")
        print(f"  Media_types: {post.get('media_types', 'N/A')}")
        print(f"  Audio_url: {post.get('audio_url', 'N/A')}")
        print()
    
    # Verificar estrutura completa do primeiro post
    if result.data:
        print("=== Campos disponiveis ===")
        post = result.data[0]
        for key, value in post.items():
            print(f"  {key}: {type(value).__name__} = {str(value)[:30] if value else 'None'}")
            
except Exception as e:
    print(f"Erro: {e}")

print("\n=== Comparando com newpost_posts ===")
try:
    result = supabase.table('newpost_posts').select('*').limit(1).execute()
    if result.data:
        print("Campos em newpost_posts:")
        for key in result.data[0].keys():
            print(f"  - {key}")
except Exception as e:
    print(f"Erro: {e}")
