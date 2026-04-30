#!/usr/bin/env python3
"""Testa o endpoint de deletar posts"""

import requests
import json

# Buscar um post para testar
response = requests.get('http://localhost:5000/api/social/posts?limit=5')
data = response.json()

if data.get('success') and data.get('posts'):
    # Encontrar um post rejeitado se possível
    rejected_post = None
    for post in data['posts']:
        if post.get('status') == 'rejected' or post.get('status') == 'rejeitado':
            rejected_post = post
            break
    
    if rejected_post:
        post_id = rejected_post['id']
        print(f"Post rejeitado encontrado: {rejected_post['title']}")
        print(f"ID: {post_id}")
        print(f"Status: {rejected_post['status']}")
    else:
        # Usar o primeiro post se não houver rejeitado
        post = data['posts'][0]
        post_id = post['id']
        print(f"Usando primeiro post: {post['title']}")
        print(f"ID: {post_id}")
        print(f"Status: {post['status']}")
    
    # Primeiro rejeitar o post se não estiver rejeitado
    if rejected_post is None:
        print(f"\nRejeitando post {post_id}...")
        reject_response = requests.post(f'http://localhost:5000/api/social/posts/{post_id}/reject', 
                                      json={'reason': 'Teste de deleção'})
        reject_data = reject_response.json()
        print(f"Status da rejeição: {reject_response.status_code}")
        print(f"Resposta: {json.dumps(reject_data, indent=2)}")
    
    # Testar deleção
    print(f"\nTestando deleção do post {post_id}...")
    delete_response = requests.delete(f'http://localhost:5000/api/social/posts/{post_id}')
    delete_data = delete_response.json()
    
    print(f"Status da deleção: {delete_response.status_code}")
    print(f"Resposta: {json.dumps(delete_data, indent=2)}")
    
    # Verificar se foi deletado
    print(f"\nVerificando se o post foi deletado...")
    verify_response = requests.get(f'http://localhost:5000/api/social/posts/{post_id}')
    verify_data = verify_response.json()
    print(f"Status da verificação: {verify_response.status_code}")
    print(f"Resposta: {json.dumps(verify_data, indent=2)}")
else:
    print("Nenhum post encontrado para teste")
