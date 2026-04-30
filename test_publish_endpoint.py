#!/usr/bin/env python3
"""Testa o endpoint de publicação de posts"""

import requests
import json

# Buscar um post para testar
response = requests.get('http://localhost:5000/api/social/posts?limit=1')
data = response.json()

if data.get('success') and data.get('posts'):
    post = data['posts'][0]
    post_id = post['id']
    print(f"Post encontrado: {post['title']}")
    print(f"ID: {post_id}")
    print(f"Status atual: {post['status']}")
    
    # Testar publicação
    print(f"\nTestando publicação do post {post_id}...")
    publish_response = requests.post(f'http://localhost:5000/api/social/posts/{post_id}/publish')
    publish_data = publish_response.json()
    
    print(f"Status da resposta: {publish_response.status_code}")
    print(f"Resposta: {json.dumps(publish_data, indent=2)}")
else:
    print("Nenhum post encontrado para teste")
