#!/usr/bin/env python3
"""Verifica publicações recentes do NewsAgent"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime, timedelta

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO PUBLICAÇÕES RECENTES DO NEWSAGENT ===\n")

# Buscar posts criados nos últimos 10 minutos
cutoff_time = datetime.now() - timedelta(minutes=10)
cutoff_iso = cutoff_time.isoformat()

result = supabase.table('posts').select('*').gte('created_at', cutoff_iso).order('created_at', desc=True).execute()

if result.data:
    print(f"Posts criados nos últimos 10 minutos: {len(result.data)}")
    
    for post in result.data:
        print(f"\n--- POST ---")
        print(f"Título: {post.get('title', 'N/A')}")
        print(f"Status: {post.get('status')}")
        print(f"Category: {post.get('category')}")
        
        metadata = post.get('metadata', {})
        if isinstance(metadata, dict):
            voxcraft = metadata.get('voxcraft', False)
            author = metadata.get('author', 'N/A')
            print(f"Author: {author}")
            print(f"Voxcraft: {voxcraft}")
            
            if post.get('status') == 'ready' and voxcraft:
                print("✅ Configuração correta - deve aparecer na interface")
            else:
                print("⚠️  Configuração incorreta - pode não aparecer")
        
        print(f"Criado: {post.get('created_at')}")
else:
    print("Nenhum post criado nos últimos 10 minutos")

print("\n🔍 Verifique em: https://plugpost-ai.lovable.app")
