# -*- coding: utf-8 -*-
"""
Diagnóstico DIRETO da conexão com NewPost-IA (Supabase)
Testa: conexão, autenticação, tabela certa e inserção
"""
import sys
import os
import json
import requests
sys.stdout.reconfigure(encoding='utf-8')

# ── Credenciais NewPost-IA ──────────────────────────────────
NEWPOST_URL  = "https://ykswhzqdjoshjoaruhqs.supabase.co"
NEWPOST_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8"
AUTOR_ID     = "3a1a93d0-e451-47a4-a126-f1b7375895eb"  # do newpost_author_id.txt

HEADERS = {
    "apikey": NEWPOST_KEY,
    "Authorization": f"Bearer {NEWPOST_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

print("=" * 60)
print("DIAGNÓSTICO: CONEXÃO COM NEWPOST-IA (Supabase)")
print("=" * 60)

# ── PASSO 1: Testar conectividade básica ────────────────────
print("\n[1] Testando conectividade com Supabase NewPost-IA...")
try:
    r = requests.get(f"{NEWPOST_URL}/rest/v1/", headers=HEADERS, timeout=10)
    print(f"    Status: {r.status_code}")
    if r.status_code == 200:
        print("    ✅ Conexão OK!")
    else:
        print(f"    ❌ Falha: {r.text[:200]}")
except Exception as e:
    print(f"    ❌ Erro de rede: {e}")

# ── PASSO 2: Listar tabelas disponíveis ─────────────────────
print("\n[2] Listando tabelas disponíveis na NewPost-IA...")
tables_to_check = ["newpost_posts", "posts", "social_posts", "articles", "content"]
for table in tables_to_check:
    try:
        r = requests.get(
            f"{NEWPOST_URL}/rest/v1/{table}?limit=1",
            headers=HEADERS,
            timeout=8
        )
        icon = "✅" if r.status_code == 200 else "❌"
        print(f"    {icon} Tabela '{table}': HTTP {r.status_code}", end="")
        if r.status_code == 200:
            data = r.json()
            print(f" ({len(data)} registros encontrados)")
        else:
            print(f" — {r.text[:80]}")
    except Exception as e:
        print(f"    ❌ Erro em '{table}': {e}")

# ── PASSO 3: Inserir post de teste na tabela correta ────────
print("\n[3] Tentando inserir post de teste na tabela 'newpost_posts'...")
payload = {
    "autor_id":  AUTOR_ID,
    "titulo":    "Teste Locutores IA — diagnóstico",
    "descricao": "Post de teste gerado automaticamente pelo script de diagnóstico",
    "conteudo":  "Este post foi criado para verificar a integração entre Locutores IA e NewPost-IA. #teste #ia",
    "hashtags":  ["teste", "ia", "locutores"],
    "audio_url": None,
}

try:
    r = requests.post(
        f"{NEWPOST_URL}/rest/v1/newpost_posts",
        headers=HEADERS,
        json=payload,
        timeout=15
    )
    print(f"    Status: {r.status_code}")
    if r.status_code in (200, 201):
        data = r.json()
        record = data[0] if isinstance(data, list) else data
        print(f"    ✅ POST CRIADO COM SUCESSO NA NEWPOST-IA!")
        print(f"    ID gerado: {record.get('id', 'N/A')}")
        print(f"    Título:    {record.get('titulo', 'N/A')}")
    else:
        print(f"    ❌ Falha ao inserir: HTTP {r.status_code}")
        print(f"    Resposta: {r.text[:300]}")
except Exception as e:
    print(f"    ❌ Exceção: {e}")

# ── PASSO 4: Verificar se o autor_id existe ─────────────────
print(f"\n[4] Verificando se autor_id '{AUTOR_ID}' existe...")
try:
    r = requests.get(
        f"{NEWPOST_URL}/rest/v1/users?id=eq.{AUTOR_ID}&limit=1",
        headers=HEADERS,
        timeout=8
    )
    if r.status_code == 200:
        data = r.json()
        if data:
            print(f"    ✅ Autor encontrado: {data[0].get('email', data[0].get('username', 'sem nome'))}")
        else:
            print(f"    ⚠️  Autor NÃO encontrado na tabela 'users' — pode estar em outra tabela!")
    else:
        print(f"    ❌ Erro ao consultar users: HTTP {r.status_code} — {r.text[:80]}")
except Exception as e:
    print(f"    ❌ Exceção: {e}")

print("\n" + "=" * 60)
print("DIAGNÓSTICO CONCLUÍDO")
print("=" * 60)
