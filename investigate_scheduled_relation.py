#!/usr/bin/env python3
"""Investiga a relacao entre scheduled_posts e newpost_posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.supabase_config import get_supabase_client

supabase = get_supabase_client()

print("=== INVESTIGANDO RELACAO ENTRE TABELAS ===\n")

# Buscar todos os scheduled_posts
result_scheduled = supabase.table('scheduled_posts').select('*').execute()
scheduled = result_scheduled.data if result_scheduled.data else []

print(f"Total de agendamentos: {len(scheduled)}\n")

# Buscar todos os newpost_posts
result_posts = supabase.table('newpost_posts').select('*').execute()
posts = result_posts.data if result_posts.data else []

print(f"Total de posts: {len(posts)}\n")

# Verificar se há alguma coluna que relaciona as tabelas
print("=== ANALISANDO COLUNAS ===\n")
print("scheduled_posts:", list(scheduled[0].keys()) if scheduled else "vazio")
print("newpost_posts:", list(posts[0].keys()) if posts else "vazio")

# Verificar se há posts com a mesma categoria dos agendamentos
print("\n=== ANALISANDO CATEGORIAS ===\n")
scheduled_categories = set([s['category'] for s in scheduled])
post_categories = set()

for post in posts:
    # Tentar extrair categoria de hashtags ou metadata
    if post.get('hashtags'):
        for tag in post['hashtags']:
            post_categories.add(tag)

print(f"Categorias agendadas: {scheduled_categories}")
print(f"Categorias nos posts (hashtags): {post_categories}")

# Verificar timestamps
print("\n=== ANALISANDO TIMESTAMPS ===\n")
if scheduled:
    print("Agendamentos mais recentes:")
    for s in sorted(scheduled, key=lambda x: x['created_at'], reverse=True)[:3]:
        print(f"  {s['scheduled_time']} - {s['category']} - {s['status']} - {s['created_at']}")

if posts:
    print("\nPosts mais recentes:")
    for p in sorted(posts, key=lambda x: x['criado_em'], reverse=True)[:3]:
        print(f"  {p['titulo'][:50]} - {p['criado_em']}")

# Verificar se há alguma tabela de social_posts ou similar
print("\n=== VERIFICANDO OUTRAS TABELAS DE POSTS ===\n")
other_tables = ['social_posts', 'posts_agendados', 'automation_posts', 'news_posts']

for table in other_tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
