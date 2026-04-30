#!/usr/bin/env python3
"""
Testar sistema Posts Sociais com novo Supabase
"""

import os
import sys

# Forçar carregar .env.local
from pathlib import Path
env_path = Path(__file__).parent / '.env.local'
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Verificar credenciais
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')

print("="*60)
print("TESTE POSTS SOCIAIS - NOVO SUPABASE")
print("="*60)
print(f"\nURL: {SUPABASE_URL}")
print(f"Service Key: {SUPABASE_SERVICE_KEY[:50]}..." if SUPABASE_SERVICE_KEY else "❌ Não configurada")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("\n❌ Credenciais não encontradas no .env.local")
    sys.exit(1)

# Testar conexão
try:
    from supabase import create_client
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    print("\n✅ Conexão estabelecida!")
    
    # Testar inserir um post de exemplo
    print("\n📤 Criando post de teste...")
    
    post_data = {
        'title': 'Post Social de Teste',
        'content': 'Este é um post criado pelo sistema Posts Sociais do Locutores IA! 🎉',
        'hashtags': ['#LocutoresIA', '#Teste', '#Social'],
        'status': 'draft'
    }
    
    result = supabase.table('posts').insert(post_data).execute()
    
    if result.data:
        post_id = result.data[0]['id']
        print(f"✅ Post criado: {post_id}")
        
        # Buscar posts
        print("\n📋 Listando posts...")
        posts = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()
        
        print(f"\nTotal de posts: {len(posts.data)}")
        for p in posts.data:
            status = p.get('status', 'unknown')
            title = p.get('title', 'Sem título')[:40]
            print(f"  - [{status}] {title}...")
        
        print("\n" + "="*60)
        print("🎉 SISTEMA POSTS SOCIAIS FUNCIONANDO!")
        print("="*60)
        print("\nAcesse: http://localhost:5000/social-posts")
        
    else:
        print("❌ Erro ao criar post")
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
