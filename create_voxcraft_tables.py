#!/usr/bin/env python3
"""Executa o SQL para criar tabelas do VoxCraft Engine"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ravpbfkicqkwjxejuzty.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Ler arquivo SQL
sql_file = os.path.join(os.path.dirname(__file__), 'CREATE_VOXCRAFT_TABLES.sql')

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Dividir em statements individuais
statements = [s.strip() for s in sql_content.split(';') if s.strip()]

print("=== CRIANDO TABELAS VOXCRAFT ===\n")

for i, statement in enumerate(statements, 1):
    if not statement or statement.startswith('--'):
        continue
    
    try:
        # Executar via RPC (para DDL)
        result = supabase.rpc('exec_sql', {'sql': statement}).execute()
        print(f"[{i}] ✅ Sucesso")
    except Exception as e:
        # Tentar via REST API direta
        try:
            import requests
            headers = {
                'apikey': SUPABASE_SERVICE_KEY,
                'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                'Content-Type': 'application/json'
            }
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
                json={'sql': statement},
                headers=headers
            )
            if response.status_code in (200, 201):
                print(f"[{i}] ✅ Sucesso (via REST)")
            else:
                print(f"[{i}] ⚠️ Aviso: {response.text[:100]}")
        except Exception as e2:
            print(f"[{i}] ❌ Erro: {str(e)[:100]}")

print("\n=== VERIFICANDO TABELAS CRIADAS ===\n")

# Verificar se tabelas existem
for table in ['voxcraft_posts', 'voxcraft_logs']:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        print(f"✅ {table}: criada com sucesso")
    except Exception as e:
        print(f"❌ {table}: {str(e)[:100]}")

print("\n=== CONCLUÍDO ===")
