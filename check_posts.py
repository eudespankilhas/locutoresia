import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

print('Verificando posts no Supabase...')

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Posts recentes
    response = supabase.table('posts').select('*').order('created_at', desc=True).limit(10).execute()
    print(f'Total de posts: {len(response.data)}')
    
    if response.data:
        print('Posts recentes:')
        for i, post in enumerate(response.data[:5], 1):
            title = post.get('title', 'Sem titulo')[:50]
            status = post.get('status', 'N/A')
            voxcraft = post.get('metadata', {}).get('voxcraft', False)
            print(f'{i}. {title}...')
            print(f'   Status: {status}')
            print(f'   Voxcraft: {voxcraft}')
    
    # Posts NewsAgent
    newsagent_posts = supabase.table('posts').select('*').eq('metadata->>voxcraft', True).execute()
    print(f'Posts NewsAgent: {len(newsagent_posts.data)}')
    
    # Posts draft
    draft_posts = supabase.table('posts').select('*').eq('status', 'draft').execute()
    print(f'Posts draft: {len(draft_posts.data)}')
    
    # Posts ready
    ready_posts = supabase.table('posts').select('*').eq('status', 'ready').execute()
    print(f'Posts ready: {len(ready_posts.data)}')
    
except Exception as e:
    print(f'Erro: {e}')
