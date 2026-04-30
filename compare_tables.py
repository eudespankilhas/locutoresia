#!/usr/bin/env python3
"""Compara as tabelas newpost_posts e posts para descobrir qual a NewPost-IA usa"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== COMPARANDO TABELAS newpost_posts VS posts ===\n")

# Buscar dados de newpost_posts
result_newpost = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()
print(f"newpost_posts: {len(result_newpost.data) if result_newpost.data else 0} registros recentes")
if result_newpost.data:
    print(f"Colunas: {list(result_newpost.data[0].keys())}")
    for post in result_newpost.data[:3]:
        print(f"  - {post['titulo'][:50]}... ({post['criado_em']})")

print("\n" + "-"*60 + "\n")

# Buscar dados de posts
result_posts = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()
print(f"posts: {len(result_posts.data) if result_posts.data else 0} registros recentes")
if result_posts.data:
    print(f"Colunas: {list(result_posts.data[0].keys())}")
    for post in result_posts.data[:3]:
        print(f"  - {post['title'][:50]}... ({post['created_at']})")

print("\n" + "="*60)
print("=== TESTANDO PUBLICAR EM 'posts' ===\n")

# Tentar publicar na tabela 'posts' também
test_post = {
    "title": "Teste de Publicação em posts - NewsAgent",
    "content": "Conteúdo de teste do NewsAgent",
    "source_url": "https://locutoresia.com",
    "image_url": None,
    "category": "teste",
    "status": "published",
    "metadata": {"source": "newsagent"}
}

try:
    result = supabase.table('posts').insert(test_post).execute()
    if result.data:
        print("✅ Publicado na tabela 'posts' com sucesso!")
        print(f"  ID: {result.data[0]['id']}")
        print(f"  Criado: {result.data[0]['created_at']}")
    else:
        print("❌ Erro ao publicar na tabela 'posts'")
except Exception as e:
    print(f"❌ Erro: {e}")
