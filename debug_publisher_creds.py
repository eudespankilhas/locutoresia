# -*- coding: utf-8 -*-
"""Debug interno: imprimir credenciais DENTRO do publisher após import"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Importar o publisher (que roda load_dotenv internamente)
from backend.social_post_publisher import social_publisher

print("=== CREDENCIAIS DENTRO DO PUBLISHER ===")
print(f"newpost_supabase_url : {social_publisher.newpost_supabase_url}")
print(f"newpost_supabase_key : {str(social_publisher.newpost_supabase_key)[:50]}..." if social_publisher.newpost_supabase_key else "newpost_supabase_key : [VAZIA!]")
print(f"local_url            : {social_publisher.local_url}")
print(f"local_key            : {str(social_publisher.local_key)[:40]}..." if social_publisher.local_key else "local_key            : [VAZIA!]")
print()

# Testar inserção direta usando as credenciais do publisher
import requests
if social_publisher.newpost_supabase_url and social_publisher.newpost_supabase_key:
    headers = {
        "apikey": social_publisher.newpost_supabase_key,
        "Authorization": f"Bearer {social_publisher.newpost_supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    payload = {
        "autor_id": "3a1a93d0-e451-47a4-a126-f1b7375895eb",
        "titulo": "Debug Publisher Test",
        "descricao": "Teste direto com credenciais do publisher",
        "conteudo": "Debug test post",
        "hashtags": ["debug"],
        "audio_url": None,
    }
    r = requests.post(
        f"{social_publisher.newpost_supabase_url}/rest/v1/newpost_posts",
        headers=headers, json=payload, timeout=15
    )
    print(f"Teste direto via credenciais do publisher: HTTP {r.status_code}")
    if r.status_code in (200, 201):
        print(f"✅ FUNCIONA! ID: {r.json()[0]['id'] if r.json() else 'N/A'}")
    else:
        print(f"❌ Falha: {r.text[:200]}")
else:
    print("❌ Credenciais newpost VAZIAS no publisher!")
