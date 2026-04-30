import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
from datetime import datetime

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Buscar um post draft do NewsAgent
response = supabase.table('posts').select('*').eq('status', 'draft').execute()
draft_posts = [p for p in response.data if p.get('metadata', {}).get('voxcraft')]

if draft_posts:
    post = draft_posts[0]
    post_id = post['id']
    print(f'Post encontrado: {post_id}')
    print(f'Titulo: {post["title"][:50]}')
    print(f'Status atual: {post["status"]}')
    print(f'Voxcraft: {post.get("metadata", {}).get("voxcraft")}')
    print()
    
    # Testar aprovação (simular clique em Publicar na NewPost-IA)
    print('=== Testando aprovação ===')
    
    # 1. Atualizar status para ready
    metadata = post.get('metadata', {}) or {}
    update_data = {
        'status': 'ready',
        'metadata': {
            **metadata,
            'published_at': datetime.now().isoformat(),
            'approved_by_user': True,
            'approval_timestamp': datetime.now().isoformat()
        }
    }
    
    result = supabase.table('posts').update(update_data).eq('id', post_id).execute()
    print(f'Status atualizado para ready: {result.data[0]["status"] if result.data else "ERRO"}')
    
    # 2. Sincronizar com newpost_posts
    print()
    print('=== Sincronizando com newpost_posts ===')
    
    # Verificar se já existe
    existing = supabase.table('newpost_posts').select('*').eq('titulo', post.get('title', '')).execute()
    
    if not existing.data:
        newpost_data = {
            'titulo': post.get('title', ''),
            'descricao': post.get('title', ''),
            'conteudo': post.get('content', ''),
            'hashtags': post.get('hashtags', []),
            'audio_url': post.get('audio_url'),
            'autor_id': '3a1a93d0-e451-47a4-a126-f1b7375895eb',
            'criado_em': post.get('created_at'),
            'atualizado_em': datetime.now().isoformat()
        }
        sync_result = supabase.table('newpost_posts').insert(newpost_data).execute()
        if sync_result.data:
            print('✅ Sincronizado com sucesso!')
            print(f'ID no newpost_posts: {sync_result.data[0]["id"]}')
        else:
            print('❌ Erro ao sincronizar')
    else:
        print('ℹ️ Já existe em newpost_posts (titulo duplicado)')
        
    print()
    print('=== Verificando se aparece no dashboard ===')
    dashboard_posts = supabase.table('newpost_posts').select('*').eq('titulo', post.get('title', '')).execute()
    if dashboard_posts.data:
        print(f'✅ Post encontrado no dashboard: {dashboard_posts.data[0]["titulo"][:50]}')
    else:
        print('❌ Post NÃO encontrado no dashboard')
else:
    print('Nenhum post draft do NewsAgent encontrado')
