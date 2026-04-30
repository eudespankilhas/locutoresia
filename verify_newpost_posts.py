#!/usr/bin/env python3
"""Verifica os posts mais recentes na NewPost-IA"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO POSTS NA NEWPOST-IA ===\n")

# Buscar posts das últimas 2 horas
cutoff_time = datetime.now() - timedelta(hours=2)
cutoff_iso = cutoff_time.isoformat()

result = supabase.table('newpost_posts').select('*').gte('criado_em', cutoff_iso).order('criado_em', desc=True).execute()

if result.data:
    print(f"Total de posts nas últimas 2 horas: {len(result.data)}")
    print(f"\n--- POSTS RECENTES ---")
    for i, post in enumerate(result.data, 1):
        print(f"\n{i}. {post['titulo']}")
        print(f"   Autor: {post['autor_id']}")
        print(f"   Criado: {post['criado_em']}")
        print(f"   Hashtags: {post['hashtags']}")
        print(f"   Descricao: {post['descricao'][:100]}...")
else:
    print("Nenhum post encontrado nas últimas 2 horas")

# Verificar total de posts
print("\n" + "="*60)
print("=== TOTAL DE POSTS NA TABELA ===\n")

result_total = supabase.table('newpost_posts').select('id', count='exact').execute()
print(f"Total de posts: {result_total.count}")

# Verificar se há alguma outra tabela que a NewPost-IA usa
print("\n" + "="*60)
print("=== VERIFICANDO OUTRAS TABELAS ===\n")

other_tables = ['posts', 'social_posts', 'publications']

for table in other_tables:
    try:
        result = supabase.table(table).select('*').order('created_at', desc=True).limit(5).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros recentes")
            for post in result.data[:2]:
                print(f"  - {post.get('title', post.get('titulo', 'N/A'))[:50]}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
