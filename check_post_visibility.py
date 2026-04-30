#!/usr/bin/env python3
"""Verifica por que os posts não aparecem na interface"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== ANALISANDO POSTS CRIADOS PELO NEWSAGENT ===\n")

# Buscar posts criados nas últimas 2 horas
cutoff_time = datetime.now() - timedelta(hours=2)
cutoff_iso = cutoff_time.isoformat()

result = supabase.table('posts').select('*').gte('created_at', cutoff_iso).order('created_at', desc=True).execute()

if result.data:
    print(f"Posts criados nas últimas 2 horas: {len(result.data)}")
    
    for post in result.data:
        print(f"\n--- POST ---")
        print(f"ID: {post['id']}")
        print(f"Título: {post.get('title', 'N/A')}")
        print(f"Status: {post.get('status')}")
        print(f"Category: {post.get('category')}")
        print(f"Image URL: {post.get('image_url', 'N/A')}")
        print(f"Source URL: {post.get('source_url', 'N/A')}")
        print(f"Metadata: {post.get('metadata')}")
        print(f"Criado: {post.get('created_at')}")
        
        # Verificar se há algum campo que possa estar bloqueando a exibição
        if post.get('status') != 'published':
            print(f"⚠️  Status não é 'published': {post.get('status')}")
else:
    print("Nenhum post criado nas últimas 2 horas")

# Comparar com posts que aparecem na interface (posts mais antigos)
print("\n" + "="*60)
print("=== COMPARANDO COM POSTS MAIS ANTIGOS ===\n")

result_old = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()

if result_old.data:
    print("Posts mais antigos (que podem aparecer na interface):")
    for post in result_old.data:
        print(f"\nID: {post['id']}")
        print(f"Título: {post.get('title', 'N/A')[:50]}...")
        print(f"Status: {post.get('status')}")
        print(f"Category: {post.get('category')}")
        print(f"Metadata: {post.get('metadata')}")
        print(f"Criado: {post.get('created_at')}")

# Verificar se há alguma tabela de views ou filtros
print("\n" + "="*60)
print("=== VERIFICANDO SE HÁ ALGUMA VIEW OU TABELA DE FEED ===\n")

possible_feed_tables = ['feed', 'timeline', 'home_posts', 'user_posts', 'all_posts']

for table in possible_feed_tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
