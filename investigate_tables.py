#!/usr/bin/env python3
"""Investiga quais tabelas do Supabase estão sendo usadas"""

import os
from supabase import create_client

SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

print("=" * 70)
print("INVESTIGAÇÃO: QUAIS TABELAS ESTÃO AS NOTÍCIAS?")
print("=" * 70)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Tabela 1: posts (onde o NewsAgent publica)
print("\n1. TABELA 'posts' (onde NewsAgent publica)")
print("-" * 70)
try:
    result = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()
    posts = result.data if result.data else []
    print(f"   Total de registros: {len(posts)}")
    if posts:
        print(f"   Exemplo mais recente:")
        post = posts[0]
        print(f"   - ID: {post.get('id')}")
        print(f"   - Título: {post.get('title', 'N/A')[:60]}...")
        print(f"   - Status: {post.get('status')}")
        print(f"   - Metadata voxcraft: {post.get('metadata', {}).get('voxcraft')}")
        print(f"   - Criado em: {post.get('created_at')}")
except Exception as e:
    print(f"   Erro: {e}")

# Tabela 2: newpost_posts (onde o dashboard busca dados)
print("\n2. TABELA 'newpost_posts' (onde dashboard busca dados)")
print("-" * 70)
try:
    result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()
    posts = result.data if result.data else []
    print(f"   Total de registros: {len(posts)}")
    if posts:
        print(f"   Exemplo mais recente:")
        post = posts[0]
        print(f"   - ID: {post.get('id')}")
        print(f"   - Título: {post.get('titulo', 'N/A')[:60]}...")
        print(f"   - Status: {post.get('status')}")
        print(f"   - Autor ID: {post.get('autor_id')}")
        print(f"   - Criado em: {post.get('criado_em')}")
except Exception as e:
    print(f"   Erro: {e}")

# Contagem total de cada tabela
print("\n3. CONTAGEM TOTAL DE REGISTROS")
print("-" * 70)
try:
    result_posts = supabase.table('posts').select('id', count='exact').execute()
    count_posts = result_posts.count if hasattr(result_posts, 'count') else len(result_posts.data)
    print(f"   Tabela 'posts': {count_posts} registros")
except Exception as e:
    print(f"   Erro ao contar 'posts': {e}")

try:
    result_newpost = supabase.table('newpost_posts').select('id', count='exact').execute()
    count_newpost = result_newpost.count if hasattr(result_newpost, 'count') else len(result_newpost.data)
    print(f"   Tabela 'newpost_posts': {count_newpost} registros")
except Exception as e:
    print(f"   Erro ao contar 'newpost_posts': {e}")

# Verificar se há posts com voxcraft=true na tabela posts
print("\n4. POSTS COM VOXCRAFT=TRUE NA TABELA 'posts'")
print("-" * 70)
try:
    result = supabase.table('posts').select('*').eq('metadata->>voxcraft', 'true').execute()
    voxcraft_posts = result.data if result.data else []
    print(f"   Total: {len(voxcraft_posts)}")
    if voxcraft_posts:
        print(f"   Status dos posts voxcraft:")
        for post in voxcraft_posts[:5]:
            print(f"   - {post.get('status')}: {post.get('title', 'N/A')[:50]}...")
except Exception as e:
    print(f"   Erro: {e}")

print("\n" + "=" * 70)
print("CONCLUSÃO:")
print("=" * 70)
print("O NewsAgent publica na tabela 'posts'")
print("O dashboard de 'Dados Reais' busca da tabela 'newpost_posts'")
print("São TABELAS DIFERENTES!")
print("=" * 70)
