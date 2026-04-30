# -*- coding: utf-8 -*-
"""Debug: ver quais variáveis o publisher está usando de fato"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Simular o carregamento exato do publisher
from dotenv import load_dotenv
load_dotenv()  # carrega .env
load_dotenv('.env.local', override=True)  # carrega .env.local

NEWPOST_SUPABASE_URL = os.getenv("NEWPOST_SUPABASE_URL", "")
NEWPOST_SUPABASE_KEY = os.getenv("NEWPOST_SUPABASE_SERVICE_KEY", os.getenv("NEWPOST_SUPABASE_ANON_KEY", ""))
LOCAL_SUPABASE_URL   = os.getenv("SUPABASE_URL", "").rstrip("/")
LOCAL_SUPABASE_KEY   = os.getenv("SUPABASE_SERVICE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))

print("=== VARIÁVEIS CARREGADAS ===")
print(f"NEWPOST_SUPABASE_URL  : {NEWPOST_SUPABASE_URL}")
print(f"NEWPOST_SUPABASE_KEY  : {NEWPOST_SUPABASE_KEY[:40]}..." if NEWPOST_SUPABASE_KEY else "NEWPOST_SUPABASE_KEY  : [VAZIA!]")
print(f"LOCAL_SUPABASE_URL    : {LOCAL_SUPABASE_URL}")
print(f"LOCAL_SUPABASE_KEY    : {LOCAL_SUPABASE_KEY[:40]}..." if LOCAL_SUPABASE_KEY else "LOCAL_SUPABASE_KEY    : [VAZIA!]")
print()

# Testar conexão Supabase NewPost com essas credenciais
import requests
if NEWPOST_SUPABASE_URL and NEWPOST_SUPABASE_KEY:
    headers = {
        "apikey": NEWPOST_SUPABASE_KEY,
        "Authorization": f"Bearer {NEWPOST_SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    payload = {
        "autor_id": "3a1a93d0-e451-47a4-a126-f1b7375895eb",
        "titulo": "Teste debug variáveis",
        "descricao": "Verificando se as credenciais estão corretas",
        "conteudo": "Post de diagnóstico de variáveis de ambiente",
        "hashtags": ["debug", "teste"],
        "audio_url": None,
    }
    print("Tentando inserir em newpost_posts com as credenciais carregadas...")
    r = requests.post(
        f"{NEWPOST_SUPABASE_URL}/rest/v1/newpost_posts",
        headers=headers,
        json=payload,
        timeout=15
    )
    print(f"HTTP {r.status_code}")
    if r.status_code in (200, 201):
        d = r.json()
        record = d[0] if isinstance(d, list) else d
        print(f"✅ Sucesso! ID: {record.get('id')}")
    else:
        print(f"❌ Falha: {r.text[:300]}")
else:
    print("❌ Credenciais NEWPOST vazias — publisher vai cair no fallback!")
