#!/usr/bin/env python3
"""Testar tabela social_posts"""

import os
from pathlib import Path

# Carregar .env.local
env_path = Path(__file__).parent / '.env.local'
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

print("="*60)
print("TESTANDO TABELA social_posts")
print("="*60)

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Criar post
    print("\n📤 Criando post...")
    post = {
        'title': 'Teste social_posts',
        'content': 'Post de teste na tabela correta!',
        'hashtags': ['#teste', '#social'],
        'status': 'draft'
    }
    
    result = supabase.table('social_posts').insert(post).execute()
    
    if result.data:
        print(f"✅ Post criado: {result.data[0]['id']}")
        
        # Listar
        print("\n📋 Listando posts:")
        all_posts = supabase.table('social_posts').select('*').execute()
        for p in all_posts.data:
            print(f"  - [{p['status']}] {p['title']}")
        
        print("\n" + "="*60)
        print("🎉 TABELA social_posts FUNCIONANDO!")
        print("="*60)
    
except Exception as e:
    print(f"❌ ERRO: {e}")
