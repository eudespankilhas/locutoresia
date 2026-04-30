#!/usr/bin/env python3
"""Obtém um author_id válido da tabela profiles"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== BUSCANDO AUTHOR_ID VALIDO ===\n")

# Tentar buscar da tabela newpost_profiles
try:
    result = supabase.table('newpost_profiles').select('*').limit(5).execute()
    
    if result.data:
        print(f"Total de profiles: {len(result.data)}")
        print(f"Colunas: {list(result.data[0].keys())}")
        print(f"\n--- PROFILES ---")
        for profile in result.data:
            print(f"  ID: {profile.get('id')}")
            print(f"  Username: {profile.get('username', profile.get('name', 'N/A'))}")
            print(f"  Email: {profile.get('email', 'N/A')}")
            print()
        
        # Usar o primeiro profile
        author_id = result.data[0]['id']
        print(f"Author ID selecionado: {author_id}")
        
        # Salvar para uso futuro
        with open('newpost_author_id.txt', 'w') as f:
            f.write(author_id)
        print(f"ID salvo em newpost_author_id.txt")
    else:
        print("Nenhum profile encontrado")
        
except Exception as e:
    print(f"Erro ao buscar profiles: {e}")

# Tentar buscar da tabela user_roles (admin)
print("\n=== BUSCANDO ADMIN USER ID ===\n")

try:
    result = supabase.table('user_roles').select('*').eq('role', 'admin').limit(1).execute()
    
    if result.data:
        admin_id = result.data[0]['user_id']
        print(f"Admin User ID: {admin_id}")
        
        with open('newpost_admin_id.txt', 'w') as f:
            f.write(admin_id)
        print(f"ID salvo em newpost_admin_id.txt")
    else:
        print("Nenhum admin encontrado")
        
except Exception as e:
    print(f"Erro ao buscar admin: {e}")
