"""
Teste manual de publicação para debug
"""

import os
from dotenv import load_dotenv
import requests
import json

def test_manual_publish():
    """Testa publicação manual direta no Supabase"""
    
    print("🧪 TESTE MANUAL DE PUBLICAÇÃO")
    print("=" * 50)
    
    # Carregar variáveis
    load_dotenv('.env.local', override=True)
    
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    if not supabase_url.endswith("/rest/v1/news_log"):
        supabase_url = f"{supabase_url.rstrip('/')}/rest/v1/news_log"
    
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    
    print(f"URL: {supabase_url}")
    print(f"Key: {'✓' if supabase_key else '✗'}")
    
    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    # Payload de teste
    payload = {
        "titulo": "Notícia de Teste Manual",
        "url": "https://teste-manual.com/noticia-12345",
        "fonte": "Teste Manual",
        "categoria": "teste",
        "status": "publicada",
        "agente_origem": "manual_test",
        "created_at": "2026-04-20T13:00:00.000Z"
    }
    
    print(f"\n📤 Enviando payload:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    try:
        response = requests.post(supabase_url, json=payload, headers=headers, timeout=20)
        
        print(f"\n📥 Resposta:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.text:
            print(f"Response Body: {response.text}")
        
        if response.status_code in [200, 201]:
            print("✅ Publicação bem-sucedida!")
            
            # Verificar se foi salvo
            print("\n🔍 Verificando se foi salvo...")
            check_url = f"{os.getenv('SUPABASE_URL').rstrip('/')}/rest/v1/news_log?url=eq.{payload['url']}"
            check_response = requests.get(check_url, headers=headers)
            
            if check_response.status_code == 200:
                data = check_response.json()
                print(f"✅ Encontrado no banco: {len(data)} registros")
                if data:
                    print(f"   ID: {data[0].get('id')}")
                    print(f"   Título: {data[0].get('titulo')}")
            else:
                print(f"❌ Erro ao verificar: {check_response.status_code}")
        
        else:
            print("❌ Falha na publicação!")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def check_table_structure():
    """Verifica estrutura da tabela news_log"""
    
    print("\n🏗️ VERIFICANDO ESTRUTURA DA TABELA")
    print("=" * 50)
    
    load_dotenv('.env.local', override=True)
    
    supabase_url = os.getenv("SUPABASE_URL", "").strip()
    supabase_key = os.getenv("SUPABASE_ANON_KEY", "").strip()
    
    # Tentar obter schema da tabela
    try:
        headers = {"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}"}
        
        # Tentativa 1: SELECT sem campos específicos
        url = f"{supabase_url.rstrip('/')}/rest/v1/news_log?select=*"
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data:
                print("Campos encontrados:")
                for campo in data[0].keys():
                    print(f"  - {campo}")
            else:
                print("Tabela vazia, mas acessível")
        else:
            print(f"Erro: {response.text}")
            
    except Exception as e:
        print(f"Erro ao verificar estrutura: {e}")

if __name__ == "__main__":
    check_table_structure()
    test_manual_publish()
