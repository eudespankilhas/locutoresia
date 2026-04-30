#!/usr/bin/env python3
"""Investiga a tabela scheduled_post no Supabase"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.supabase_config import get_supabase_client

supabase = get_supabase_client()

print("=== INVESTIGANDO TABELA scheduled_post ===\n")

# Tentar acessar a tabela scheduled_posts (plural)
try:
    result = supabase.table('scheduled_posts').select('*').limit(10).execute()
    
    if result.data:
        print(f"[OK] scheduled_post: {len(result.data)} registros")
        print(f"\nColunas: {list(result.data[0].keys())}")
        print(f"\n--- PRIMEIROS REGISTROS ---")
        for i, post in enumerate(result.data[:5], 1):
            print(f"\nRegistro {i}:")
            for key, value in post.items():
                print(f"  {key}: {value}")
    else:
        print("[OK] scheduled_post: tabela vazia")
        
except Exception as e:
    print(f"[ERRO] scheduled_post: {str(e)}")

print("\n" + "="*60)
print("=== VERIFICANDO OUTRAS TABELAS RELACIONADAS ===\n")

# Verificar outras tabelas que podem estar relacionadas
related_tables = ['newpost_posts', 'posts', 'publications', 'automation_config', 'news_cycles']

for table in related_tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
