#!/usr/bin/env python3
"""Testa publicação com estrutura correta da tabela posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_agent import NewsAgent

print("=== TESTANDO PUBLICACAO COM ESTRUTURA CORRETA ===\n")

agent = NewsAgent()

# Coletar algumas notícias
print("Coletando notícias de G1 - tecnologia...")
news = agent.collect_from_source("g1", "tecnologia")

print(f"Coletadas {len(news)} notícias\n")

# Salvar (isso vai publicar com estrutura correta)
print("Salvando e publicando com estrutura correta...")
saved, duplicates = agent.db.save_news(news)

print(f"\n✅ Resultado:")
print(f"  Salvas no SQLite: {saved}")
print(f"  Duplicadas: {duplicates}")

# Verificar posts na tabela
print("\n=== VERIFICANDO TABELA posts ===\n")

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

result = supabase.table('posts').select('*').order('created_at', desc=True).limit(5).execute()
if result.data:
    print(f"Posts recentes: {len(result.data)}")
    for post in result.data:
        print(f"\n  ID: {post['id']}")
        print(f"  Author: {post.get('author_id')}")
        print(f"  Status: {post.get('status')}")
        print(f"  IA Generated: {post.get('is_ia_generated')}")
        print(f"  Privacy: {post.get('privacy')}")
        print(f"  Content: {post.get('content', '')[:100]}...")
        print(f"  Tags: {post.get('tags')}")
        print(f"  AI Tags: {post.get('ai_tags')}")
        print(f"  Media URLs: {post.get('media_urls')}")
        print(f"  Criado: {post.get('created_at')}")

print("\n✅ Teste concluído! Verifique a NewPost-IA em: https://plugpost-ai.lovable.app")
