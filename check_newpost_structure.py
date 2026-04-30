#!/usr/bin/env python3
"""Verifica a estrutura da tabela newpost_posts"""

from supabase import create_client

SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

print("Verificando estrutura da tabela newpost_posts...")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

result = supabase.table('newpost_posts').select('*').limit(1).execute()

if result.data:
    print("Colunas da tabela newpost_posts:")
    for col in result.data[0].keys():
        print(f"  - {col}")
else:
    print("Nenhum dado encontrado")
