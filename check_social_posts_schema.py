"""
Verificar schema da tabela social_posts
"""
import os
os.environ['SUPABASE_URL'] = 'https://ravpbfkicqkwjxejuzty.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM'

import requests

supabase_url = os.environ['SUPABASE_URL'].rstrip('/')
supabase_key = os.environ['SUPABASE_SERVICE_KEY']

headers = {
    'apikey': supabase_key,
    'Authorization': f'Bearer {supabase_key}',
    'Content-Type': 'application/json'
}

# Tenta buscar colunas da tabela social_posts
try:
    response = requests.get(
        f"{supabase_url}/rest/v1/social_posts?select=*&limit=1",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            print("Colunas encontradas na tabela social_posts:")
            for col in data[0].keys():
                print(f"  - {col}")
        else:
            print("Tabela social_posts existe mas está vazia")
            print("Verificando schema via RPC...")
    else:
        print(f"Erro ao buscar social_posts: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Erro: {e}")

# Tenta verificar se a tabela existe
print("\nVerificando se tabela social_posts existe...")
try:
    response = requests.get(
        f"{supabase_url}/rest/v1/social_posts?select=count",
        headers=headers,
        timeout=10
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Tabela social_posts existe")
    else:
        print(f"Erro: {response.text}")
except Exception as e:
    print(f"Erro: {e}")
