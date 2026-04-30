#!/usr/bin/env python3
"""Testa configuração final: tabela posts com status 'ready' e voxcraft: True"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_agent import NewsAgent

print("=== TESTANDO CONFIGURAÇÃO FINAL ===\n")

agent = NewsAgent()

# Coletar algumas notícias
print("Coletando notícias de G1 - economia...")
news = agent.collect_from_source("g1", "economia")

print(f"Coletadas {len(news)} notícias\n")

# Salvar (isso vai publicar com status 'ready' e voxcraft: True)
print("Salvando e publicando com configuração final...")
saved, duplicates = agent.db.save_news(news)

print(f"\n✅ Resultado:")
print(f"  Salvas no SQLite: {saved}")
print(f"  Duplicadas: {duplicates}")

# Verificar posts na tabela
print("\n=== VERIFICANDO POSTS CRIADOS ===\n")

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Buscar posts criados nas últimas 5 minutos
cutoff_time = datetime.now() - timedelta(minutes=5)
cutoff_iso = cutoff_time.isoformat()

result = supabase.table('posts').select('*').gte('created_at', cutoff_iso).order('created_at', desc=True).execute()

if result.data:
    print(f"Posts criados nos últimos 5 minutos: {len(result.data)}")
    
    for post in result.data:
        print(f"\n--- POST ---")
        print(f"ID: {post['id']}")
        print(f"Título: {post.get('title', 'N/A')}")
        print(f"Status: {post.get('status')}")
        print(f"Category: {post.get('category')}")
        print(f"Metadata: {post.get('metadata')}")
        print(f"Criado: {post.get('created_at')}")
        
        # Verificar se tem a configuração correta
        metadata = post.get('metadata', {})
        if isinstance(metadata, dict):
            voxcraft = metadata.get('voxcraft', False)
            status = post.get('status')
            
            if status == 'ready' and voxcraft:
                print("✅ Configuração correta: status='ready' e voxcraft=True")
            else:
                print(f"⚠️  Configuração incorreta: status='{status}', voxcraft={voxcraft}")
else:
    print("Nenhum post criado nos últimos 5 minutos")

print("\n🔍 Verifique agora em: https://plugpost-ai.lovable.app")
print("Os posts devem aparecer pois têm status 'ready' e voxcraft: True")
