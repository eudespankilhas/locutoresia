#!/usr/bin/env python3
"""Testa a sincronização entre tabelas posts e newpost_posts"""

import requests
import json
from supabase import create_client

BASE_URL = 'http://localhost:5000'
SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

print("=" * 70)
print("TESTE DE SINCRONIZAÇÃO: posts → newpost_posts")
print("=" * 70)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# 1. Buscar um post do NewsAgent com status draft
print("\n1. Buscando post do NewsAgent para testar...")
try:
    result = supabase.table('posts').select('*').eq('metadata->>voxcraft', 'true').eq('status', 'draft').limit(1).execute()
    
    if result.data:
        test_post = result.data[0]
        post_id = test_post['id']
        print(f"   Post encontrado: {test_post['title'][:50]}...")
        print(f"   ID: {post_id}")
        print(f"   Status atual: {test_post['status']}")
        
        # 2. Aprovar o post (isso deve sincronizar)
        print(f"\n2. Aprovando post (deve sincronizar com newpost_posts)...")
        try:
            response = requests.post(f'{BASE_URL}/api/social/posts/{post_id}/publish-newsagent')
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Synced: {data.get('synced_with_newpost')}")
        except Exception as e:
            print(f"   Erro ao aprovar: {e}")
        
        # 3. Verificar se foi sincronizado
        print(f"\n3. Verificando sincronização...")
        try:
            result_sync = supabase.table('newpost_posts').select('*').eq('posts_id', post_id).execute()
            
            if result_sync.data:
                synced_post = result_sync.data[0]
                print(f"   ✅ SINCRONIZADO COM SUCESSO!")
                print(f"   ID em newpost_posts: {synced_post.get('id')}")
                print(f"   Título: {synced_post.get('titulo', 'N/A')[:50]}...")
                print(f"   Autor ID: {synced_post.get('autor_id')}")
                print(f"   Status: {synced_post.get('status')}")
            else:
                print(f"   ❌ NÃO sincronizado")
        except Exception as e:
            print(f"   Erro ao verificar sincronização: {e}")
    else:
        print("   Nenhum post draft do NewsAgent encontrado")
        print("   Tentando buscar qualquer post do NewsAgent...")
        
        result = supabase.table('posts').select('*').eq('metadata->>voxcraft', 'true').limit(1).execute()
        if result.data:
            test_post = result.data[0]
            post_id = test_post['id']
            print(f"   Post encontrado (status: {test_post['status']}): {test_post['title'][:50]}...")
            print(f"   ID: {post_id}")
            
            # Tentar aprovar mesmo que não seja draft
            print(f"\n2. Aprovando post...")
            try:
                response = requests.post(f'{BASE_URL}/api/social/posts/{post_id}/publish-newsagent')
                data = response.json()
                print(f"   Status: {response.status_code}")
                print(f"   Success: {data.get('success')}")
                print(f"   Message: {data.get('message')}")
            except Exception as e:
                print(f"   Erro: {e}")
        else:
            print("   Nenhum post do NewsAgent encontrado")
            
except Exception as e:
    print(f"   Erro: {e}")

print("\n" + "=" * 70)
print("TESTE CONCLUÍDO")
print("=" * 70)
