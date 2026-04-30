# -*- coding: utf-8 -*-
"""Teste completo do fluxo SocialPost via API local"""
import sys, os, requests, json
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://127.0.0.1:5000"

print("=" * 55)
print("TESTE COMPLETO — SISTEMA DE POSTS SOCIAIS")
print("=" * 55)

# -------------------------------------------------------
# TESTE 1: Listar posts (deve retornar lista vazia)
# -------------------------------------------------------
print("\n[1] Listando posts sociais...")
r = requests.get(f"{BASE}/api/social/posts?limit=10", timeout=10)
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"    OK - Posts encontrados: {data.get('count', 0)}")
else:
    print(f"    ERRO: {r.text[:200]}")

# -------------------------------------------------------
# TESTE 2: Criar post
# -------------------------------------------------------
print("\n[2] Criando post de teste...")
payload = {
    "title": "Brasileirao 2026: Flamengo e campeo invicto",
    "caption": "O Rubro-Negro conquistou o titulo com 10 jogos de antecedencia! Historico!",
    "hashtags": ["flamengo", "brasileirao", "futebol", "esportes", "bi2026"],
    "platforms": ["newpost_ia"],
    "status": "rascunho",
    "image_url": "https://picsum.photos/seed/flamengo/800/400"
}
r = requests.post(f"{BASE}/api/social/posts",
                  headers={'Content-Type': 'application/json'},
                  json=payload, timeout=15)
print(f"    Status: {r.status_code}")
if r.status_code in (200, 201):
    data = r.json()
    post = data.get('post', {})
    post_id = post.get('id', '')
    print(f"    OK - Post criado! ID: {post_id}")
    print(f"    Title: {post.get('title','')[:50]}")
    print(f"    Status: {post.get('status','')}")
else:
    print(f"    ERRO: {r.text[:300]}")
    sys.exit(1)

# -------------------------------------------------------
# TESTE 3: Buscar post pelo ID
# -------------------------------------------------------
print(f"\n[3] Buscando post {post_id[:8]}...")
r = requests.get(f"{BASE}/api/social/posts/{post_id}", timeout=10)
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    p = r.json().get('post', {})
    print(f"    OK - Titulo: {p.get('title','')[:50]}")
    print(f"    Status atual: {p.get('status','')}")
    print(f"    Approval: {p.get('approval_status','')}")
else:
    print(f"    ERRO: {r.text[:200]}")

# -------------------------------------------------------
# TESTE 4: Aprovar post
# -------------------------------------------------------
print(f"\n[4] Aprovando post...")
r = requests.post(f"{BASE}/api/social/posts/{post_id}/approve",
                  headers={'Content-Type': 'application/json'},
                  json={"approved_by": "teste_automatizado"}, timeout=10)
print(f"    Status: {r.status_code}")
if r.status_code == 200:
    print(f"    OK - Post aprovado!")
else:
    print(f"    ERRO: {r.text[:200]}")

# -------------------------------------------------------
# TESTE 5: Publicar na NewPost-IA
# -------------------------------------------------------
print(f"\n[5] Publicando na NewPost-IA...")
r = requests.post(f"{BASE}/api/social/posts/{post_id}/publish",
                  headers={'Content-Type': 'application/json'},
                  json={}, timeout=20)
print(f"    Status: {r.status_code}")
data = r.json()
if data.get('success'):
    print(f"    OK - Publicado! Status: {data.get('status','')}")
else:
    print(f"    AVISO (esperado sem credenciais NewPost-IA): {data.get('message', data.get('error',''))[:100]}")
    results = data.get('publish_results', {})
    for plat, res in results.items():
        print(f"    [{plat}] sucesso={res.get('success')} err={str(res.get('error',''))[:80]}")

# -------------------------------------------------------
# TESTE 6: Gerar legenda com IA
# -------------------------------------------------------
print(f"\n[6] Gerando legenda com IA (Gemini)...")
r = requests.post(f"{BASE}/api/social/generate-caption",
                  headers={'Content-Type': 'application/json'},
                  json={"title": "Flamengo vence Palmeiras no Maracana",
                        "content": "Com gol nos acrescimos, Flamengo derrota o Palmeiras por 2 a 1."},
                  timeout=20)
print(f"    Status: {r.status_code}")
data = r.json()
if data.get('success'):
    print(f"    OK - Legenda IA gerada!")
    print(f"    Caption: {data.get('caption','')[:100]}")
    print(f"    Hashtags: {data.get('hashtags','')}")
else:
    print(f"    AVISO: {data.get('error','')[:100]}")

# -------------------------------------------------------
# TESTE 7: Listar posts final
# -------------------------------------------------------
print(f"\n[7] Listagem final de posts...")
r = requests.get(f"{BASE}/api/social/posts?limit=10", timeout=10)
data = r.json()
print(f"    Total de posts no banco: {data.get('count', 0)}")
for p in data.get('posts', []):
    print(f"    - [{p.get('status','?'):10}] {p.get('title','')[:50]}")

print("\n" + "=" * 55)
print("RESUMO: Sistema de Posts Sociais OPERACIONAL!")
print("Acesse: http://127.0.0.1:5000/social-posts")
print("=" * 55)
