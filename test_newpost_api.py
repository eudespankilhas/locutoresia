#!/usr/bin/env python3
"""Testa a API do NewPost-IA para entender como publicar posts"""

import requests
import json

NEWPOST_URL = "https://plugpost-ai.lovable.app"

print("=== TESTANDO API DO NEWPOST-IA ===\n")

# Tentar diferentes endpoints
endpoints = [
    "/api/posts",
    "/api/publish",
    "/api/create-post",
    "/api/newpost",
    "/api/v1/posts",
]

for endpoint in endpoints:
    url = f"{NEWPOST_URL}{endpoint}"
    try:
        print(f"Testando: {url}")
        response = requests.get(url, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code != 404:
            print(f"  Response: {response.text[:200]}")
    except Exception as e:
        print(f"  Erro: {str(e)[:100]}")
    print()

# Tentar POST para criar um post
print("=== TENTANDO CRIAR POST VIA API ===\n")

test_post = {
    "titulo": "Teste de API NewsAgent",
    "descricao": "Este é um post de teste do NewsAgent",
    "conteudo": "Conteúdo completo do post de teste",
    "hashtags": ["teste", "newsagent", "newpost"],
    "autor_id": "newsagent"
}

for endpoint in ["/api/posts", "/api/publish", "/api/create-post"]:
    url = f"{NEWPOST_URL}{endpoint}"
    try:
        print(f"POST para: {url}")
        response = requests.post(url, json=test_post, timeout=10)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:300]}")
    except Exception as e:
        print(f"  Erro: {str(e)[:100]}")
    print()
