#!/usr/bin/env python3
"""Testa o NewsAgent coletando notícias e publicando na NewPost-IA"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_agent import NewsAgent

print("=== TESTANDO NEWSAGENT + NEWPOST-IA ===\n")

agent = NewsAgent()

# Coletar notícias de uma fonte
print("Coletando notícias de G1 - Brasil...")
news = agent.collect_from_source("g1", "brasil")

print(f"Coletadas {len(news)} notícias\n")

# Salvar no banco (isso vai publicar na NewPost-IA automaticamente)
print("Salvando e publicando na NewPost-IA...")
saved, duplicates = agent.db.save_news(news)

print(f"\n✅ Resultado:")
print(f"  Salvas no SQLite: {saved}")
print(f"  Duplicadas: {duplicates}")
print(f"  Total processadas: {len(news)}")

# Verificar se foram publicadas na NewPost-IA
print("\n=== VERIFICANDO PUBLICACOES NA NEWPOST-IA ===\n")

try:
    from supabase import create_client
    
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Buscar posts recentes
    result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()
    
    if result.data:
        print(f"Total de posts na NewPost-IA: {len(result.data)}")
        print(f"\n--- POSTS MAIS RECENTES ---")
        for i, post in enumerate(result.data, 1):
            print(f"\n{i}. {post['titulo']}")
            print(f"   Autor: {post['autor_id']}")
            print(f"   Criado: {post['criado_em']}")
            print(f"   Hashtags: {post['hashtags']}")
    else:
        print("Nenhum post encontrado")
        
except Exception as e:
    print(f"Erro ao verificar: {e}")
