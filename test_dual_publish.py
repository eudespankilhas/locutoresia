#!/usr/bin/env python3
"""Testa publicação em ambas as tabelas"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_agent import NewsAgent

print("=== TESTANDO PUBLICACAO DUPLA ===\n")

agent = NewsAgent()

# Coletar algumas notícias
print("Coletando notícias de G1 - tecnologia...")
news = agent.collect_from_source("g1", "tecnologia")

print(f"Coletadas {len(news)} notícias\n")

# Salvar (isso vai publicar em ambas as tabelas)
print("Salvando e publicando em ambas as tabelas...")
saved, duplicates = agent.db.save_news(news)

print(f"\n✅ Resultado:")
print(f"  Salvas no SQLite: {saved}")
print(f"  Duplicadas: {duplicates}")

# Verificar ambas as tabelas
print("\n=== VERIFICANDO TABELA newpost_posts ===\n")

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

result_newpost = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(3).execute()
if result_newpost.data:
    print(f"Posts recentes em newpost_posts: {len(result_newpost.data)}")
    for post in result_newpost.data:
        print(f"  - {post['titulo'][:50]}... ({post['criado_em']})")

print("\n=== VERIFICANDO TABELA posts ===\n")

result_posts = supabase.table('posts').select('*').order('created_at', desc=True).limit(3).execute()
if result_posts.data:
    print(f"Posts recentes em posts: {len(result_posts.data)}")
    for post in result_posts.data:
        print(f"  - {post['title'][:50]}... ({post['created_at']})")

print("\n✅ Teste concluído! Verifique a NewPost-IA em: https://plugpost-ai.lovable.app")
