#!/usr/bin/env python3
"""Investiga tabelas de sincronização e views"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== INVESTIGANDO TABELAS DE SINCRONIZAÇÃO ===\n")

# Tabelas possíveis de sincronização
sync_tables = [
    'sync_posts', 'post_sync', 'feed_posts', 'timeline_posts',
    'home_feed', 'user_feed', 'public_feed', 'all_posts_view',
    'published_posts', 'active_posts', 'visible_posts'
]

for table in sync_tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")

print("\n" + "="*60)
print("=== COMPARANDO ESTRUTURA DAS TABELAS PRINCIPAIS ===\n")

# Comparar estrutura de posts vs newpost_posts
print("Tabela posts:")
try:
    result_posts = supabase.table('posts').select('*').limit(1).execute()
    if result_posts.data:
        print(f"  Colunas: {list(result_posts.data[0].keys())}")
except Exception as e:
    print(f"  Erro: {e}")

print("\nTabela newpost_posts:")
try:
    result_newpost = supabase.table('newpost_posts').select('*').limit(1).execute()
    if result_newpost.data:
        print(f"  Colunas: {list(result_newpost.data[0].keys())}")
except Exception as e:
    print(f"  Erro: {e}")

print("\nTabela social_posts:")
try:
    result_social = supabase.table('social_posts').select('*').limit(1).execute()
    if result_social.data:
        print(f"  Colunas: {list(result_social.data[0].keys())}")
except Exception as e:
    print(f"  Erro: {e}")

print("\n" + "="*60)
print("=== VERIFICANDO SE HÁ ALGUMA TRIGGER OU FUNCTION ===\n")

# Tentar executar uma query SQL para verificar triggers
try:
    # Verificar se há alguma tabela que conecta newpost_posts com posts
    print("Tentando identificar relação entre tabelas...")
    
    # Buscar posts que aparecem na interface (status 'ready')
    result_ready = supabase.table('posts').select('*').eq('status', 'ready').order('created_at', desc=True).limit(3).execute()
    
    if result_ready.data:
        print(f"\nPosts com status 'ready' (que aparecem na interface): {len(result_ready.data)}")
        for post in result_ready.data:
            print(f"  - {post.get('title', 'N/A')[:50]}...")
            print(f"    Metadata: {post.get('metadata')}")
    
    # Verificar se há algum padrão nos títulos
    print("\n=== ANALISANDO PADRÕES DE TÍTULOS ===\n")
    
    result_all_posts = supabase.table('posts').select('*').order('created_at', desc=True).limit(10).execute()
    
    if result_all_posts.data:
        print("Últimos 10 posts na tabela posts:")
        for post in result_all_posts.data:
            title = post.get('title', 'N/A')
            status = post.get('status', 'N/A')
            metadata = post.get('metadata', {})
            voxcraft = metadata.get('voxcraft', False) if isinstance(metadata, dict) else False
            
            print(f"  {title[:50]}... | Status: {status} | Voxcraft: {voxcraft}")
            
except Exception as e:
    print(f"Erro na análise: {e}")
