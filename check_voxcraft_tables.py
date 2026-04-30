#!/usr/bin/env python3
"""Investiga tabelas voxcraft mencionadas na Edge Function"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ravpbfkicqkwjxejuzty.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== INVESTIGANDO TABELAS VOXCRAFT ===\n")

voxcraft_tables = ['voxcraft_posts', 'voxcraft_status', 'voxcraft_logs']

for table in voxcraft_tables:
    try:
        result = supabase.table(table).select('*').limit(5).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
            print(f"\n  Dados:")
            for item in result.data[:2]:
                print(f"    {item}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:100]}")

print("\n" + "="*60)
print("=== LISTANDO TODAS AS TABELAS ===\n")

# Tentar listar todas as tabelas do schema public
tables_to_check = [
    'posts', 'newpost_posts', 'voxcraft_posts', 'social_posts', 
    'publications', 'profiles', 'newpost_profiles', 'user_roles',
    'voxcraft_status', 'voxcraft_logs', 'sources', 'automation_config',
    'news_cycles', 'scheduled_posts'
]

for table in tables_to_check:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
