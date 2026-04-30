#!/usr/bin/env python3
"""Verifica se um post específico foi sincronizado"""

from supabase import create_client

SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Buscar posts recentes em newpost_posts
print("Últimos 5 registros em newpost_posts:")
result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()

for post in result.data:
    print(f"\n- ID: {post.get('id')}")
    print(f"  Título: {post.get('titulo', 'N/A')[:60]}...")
    print(f"  Autor ID: {post.get('autor_id')}")
    print(f"  Criado em: {post.get('criado_em')}")
