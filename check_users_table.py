#!/usr/bin/env python3
"""Verifica a tabela users para criar um usuario valido para o NewsAgent"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO TABELA users ===\n")

try:
    result = supabase.table('users').select('*').limit(5).execute()
    
    if result.data:
        print(f"Total de usuarios: {len(result.data)}")
        print(f"\nColunas: {list(result.data[0].keys())}")
        print(f"\n--- USUARIOS ---")
        for user in result.data:
            print(f"  ID: {user.get('id')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Nome: {user.get('name', user.get('full_name', 'N/A'))}")
            print()
    else:
        print("Tabela users vazia")
        
except Exception as e:
    print(f"Erro: {e}")

# Tentar criar um usuario para o NewsAgent
print("\n=== CRIANDO USUARIO PARA NEWSAGENT ===\n")

import uuid

newsagent_user = {
    "id": str(uuid.uuid4()),
    "email": "newsagent@locutoresia.com",
    "name": "NewsAgent AI",
    "full_name": "NewsAgent AI - Locutores IA"
}

try:
    result = supabase.table('users').insert(newsagent_user).execute()
    
    if result.data:
        print("✅ Usuario criado com sucesso!")
        print(f"  ID: {result.data[0]['id']}")
        print(f"  Email: {result.data[0]['email']}")
        print(f"  Nome: {result.data[0]['name']}")
        
        # Salvar o ID para uso futuro
        with open('newsagent_user_id.txt', 'w') as f:
            f.write(result.data[0]['id'])
        print(f"\nID salvo em newsagent_user_id.txt")
    else:
        print("❌ Erro ao criar usuario")
        
except Exception as e:
    print(f"❌ Erro: {e}")
