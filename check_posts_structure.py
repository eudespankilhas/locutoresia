#!/usr/bin/env python3
"""Verifica a estrutura real da tabela posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO ESTRUTURA DA TABELA posts ===\n")

result = supabase.table('posts').select('*').limit(1).execute()

if result.data:
    print(f"Colunas da tabela posts:")
    for col in result.data[0].keys():
        print(f"  - {col}")
else:
    print("Tabela vazia")

# Verificar também a estrutura de um post existente
print("\n=== DADOS DE UM POST EXISTENTE ===\n")

result = supabase.table('posts').select('*').order('created_at', desc=True).limit(1).execute()

if result.data:
    post = result.data[0]
    for key, value in post.items():
        print(f"{key}: {value}")
