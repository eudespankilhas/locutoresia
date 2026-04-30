#!/usr/bin/env python3
"""Verifica se o post de teste está na tabela newpost_posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO POST DE TESTE EM newpost_posts ===\n")

# Buscar posts criados nas últimas 2 horas
cutoff_time = datetime.now() - timedelta(hours=2)
cutoff_iso = cutoff_time.isoformat()

result = supabase.table('newpost_posts').select('*').gte('criado_em', cutoff_iso).order('criado_em', desc=True).execute()

if result.data:
    print(f"Posts em newpost_posts nas últimas 2 horas: {len(result.data)}")
    
    for post in result.data:
        print(f"\n--- POST ---")
        print(f"ID: {post['id']}")
        print(f"Título: {post.get('titulo', 'N/A')}")
        print(f"Autor ID: {post.get('autor_id')}")
        print(f"Descrição: {post.get('descricao', 'N/A')[:100]}...")
        print(f"Hashtags: {post.get('hashtags')}")
        print(f"Criado em: {post.get('criado_em')}")
else:
    print("Nenhum post encontrado em newpost_posts nas últimas 2 horas")

# Buscar especificamente o post de teste
print("\n" + "="*60)
print("=== BUSCANDO POST DE TESTE ESPECÍFICO ===\n")

result_test = supabase.table('newpost_posts').select('*').eq('titulo', 'Teste NewsAgent newpost_posts - 09:51:12 - Tecnologia Brasileira').execute()

if result_test.data:
    print("Post de teste encontrado em newpost_posts:")
    post = result_test.data[0]
    for key, value in post.items():
        print(f"  {key}: {value}")
else:
    print("Post de teste NÃO encontrado em newpost_posts")

# Verificar total de posts em newpost_posts
print("\n" + "="*60)
print("=== TOTAL DE POSTS EM newpost_posts ===\n")

result_total = supabase.table('newpost_posts').select('id', count='exact').execute()
print(f"Total de posts: {result_total.count}")

# Listar os 5 posts mais recentes
print("\n=== 5 POSTS MAIS RECENTES EM newpost_posts ===\n")

result_recent = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()

if result_recent.data:
    for i, post in enumerate(result_recent.data, 1):
        print(f"\n{i}. {post['titulo']}")
        print(f"   Autor: {post['autor_id']}")
        print(f"   Criado: {post['criado_em']}")
        print(f"   Hashtags: {post['hashtags']}")
