#!/usr/bin/env python3
"""Executa comandos SQL para ativar RLS e criar políticas no Supabase"""

import requests
import sys

# Configuração do Supabase local
SUPABASE_URL = "https://ravpbfkicqkwjxejuzty.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM"

headers = {
    'apikey': SUPABASE_SERVICE_KEY,
    'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

# Comandos SQL para executar
commands = [
    "ALTER TABLE posts ENABLE ROW LEVEL SECURITY;",
    "CREATE POLICY IF NOT EXISTS \"Permitir inserção de posts\" ON posts FOR INSERT WITH CHECK (true);",
    "CREATE POLICY IF NOT EXISTS \"Permitir atualizar posts\" ON posts FOR UPDATE USING (true) WITH CHECK (true);",
    "CREATE POLICY IF NOT EXISTS \"Permitir ler posts\" ON posts FOR SELECT USING (true);"
]

print("=" * 60)
print("APLICANDO RLS E POLÍTICAS NA TABELA posts")
print("=" * 60)
print(f"URL: {SUPABASE_URL}")
print()

for i, sql in enumerate(commands, 1):
    print(f"{i}. Executando: {sql[:50]}...")
    
    # Tentar executar via RPC
    try:
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
            json={'query': sql},
            headers=headers,
            timeout=10
        )
        
        if response.status_code in (200, 201, 204):
            print(f"   ✅ OK (Status: {response.status_code})")
        else:
            print(f"   ⚠️ Resposta: {response.status_code}")
            if response.text:
                print(f"   Detalhes: {response.text[:100]}")
                
    except Exception as e:
        print(f"   ❌ Erro: {e}")

print()
print("=" * 60)
print("Verifique no painel do Supabase se as políticas foram criadas:")
print(f"https://supabase.com/dashboard/project/ravpbfkicqkwjxejuzty")
print("Database → Tables → posts → Policies")
print("=" * 60)
