#!/usr/bin/env python3
"""Lista todas as tabelas do Supabase para encontrar a tabela de usuarios"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== LISTANDO TODAS AS TABELAS DO SUPABASE ===\n")

# Tentar usar RPC para listar tabelas
try:
    result = supabase.rpc('get_tables').execute()
    print("Tabelas via RPC:", result.data)
except Exception as e:
    print(f"RPC nao disponivel: {e}")

# Tentar tabelas comuns
tables = [
    'users', 'auth.users', 'profiles', 'accounts', 'user_profiles',
    'newpost_posts', 'scheduled_posts', 'social_posts', 'posts',
    'publications', 'automation_config', 'news_cycles'
]

for table in tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
