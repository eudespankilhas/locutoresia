#!/usr/bin/env python3
"""Testa os novos endpoints do NewsAgent"""

import requests
import json

BASE_URL = 'http://localhost:5000'

print("=" * 60)
print("TESTANDO NOVOS ENDPOINTS DO NEWSAGENT")
print("=" * 60)

# Teste 1: Listar posts pendentes
print("\n1. Testando GET /api/social/posts/pending-approval/newsagent")
try:
    response = requests.get(f'{BASE_URL}/api/social/posts/pending-approval/newsagent')
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Success: {data.get('success')}")
    print(f"   Count: {data.get('count', 0)}")
    if data.get('posts'):
        print(f"   Primeiro post: {data['posts'][0].get('title', 'N/A')[:50]}...")
except Exception as e:
    print(f"   Erro: {e}")

# Teste 2: Buscar um post para testar aprovação/rejeição
print("\n2. Buscando um post para testar aprovação/rejeição...")
try:
    response = requests.get(f'{BASE_URL}/api/social/posts?limit=5')
    data = response.json()
    
    if data.get('success') and data.get('posts'):
        test_post = data['posts'][0]
        post_id = test_post['id']
        print(f"   Post encontrado: {test_post['title'][:50]}...")
        print(f"   ID: {post_id}")
        print(f"   Status atual: {test_post.get('status')}")
        
        # Teste 3: Aprovar post
        print(f"\n3. Testando POST /api/social/posts/{post_id}/publish-newsagent")
        try:
            response = requests.post(f'{BASE_URL}/api/social/posts/{post_id}/publish-newsagent')
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message', 'N/A')}")
        except Exception as e:
            print(f"   Erro: {e}")
        
        # Teste 4: Rejeitar post
        print(f"\n4. Testando POST /api/social/posts/{post_id}/reject-newsagent")
        try:
            response = requests.post(
                f'{BASE_URL}/api/social/posts/{post_id}/reject-newsagent',
                json={'reason': 'Teste de rejeição'}
            )
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Success: {data.get('success')}")
            print(f"   Message: {data.get('message', 'N/A')}")
        except Exception as e:
            print(f"   Erro: {e}")
    else:
        print("   Nenhum post encontrado para teste")
except Exception as e:
    print(f"   Erro: {e}")

print("\n" + "=" * 60)
print("TESTES CONCLUÍDOS")
print("=" * 60)
