"""
Script para testar a conexão com o Supabase
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis do .env
load_dotenv()

def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    
    print("=" * 50)
    print("TESTE DE CONEXÃO COM SUPABASE")
    print("=" * 50)
    
    # Obter credenciais
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon_key = os.getenv("SUPABASE_ANON_KEY")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    print("\n1. Verificando variáveis de ambiente:")
    print(f"   SUPABASE_URL: {'✓ Configurado' if supabase_url else '✗ Não encontrado'}")
    print(f"   SUPABASE_ANON_KEY: {'✓ Configurado' if supabase_anon_key else '✗ Não encontrado'}")
    print(f"   SUPABASE_SERVICE_KEY: {'✓ Configurado' if supabase_service_key else '✗ Não encontrado'}")
    
    if not supabase_url or not supabase_anon_key:
        print("\n✗ ERRO: Credenciais do Supabase não configuradas!")
        print("   Verifique o arquivo .env ou as variáveis de ambiente.")
        return False
    
    print(f"\n   URL: {supabase_url}")
    
    # Testar conexão HTTP
    print("\n2. Testando conexão HTTP...")
    
    try:
        import requests
        
        # Testar endpoint de posts
        posts_url = f"{supabase_url}/rest/v1/posts?limit=1"
        headers = {
            "Authorization": f"Bearer {supabase_anon_key}",
            "apikey": supabase_anon_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(posts_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("   ✓ Conexão bem-sucedida!")
            data = response.json()
            print(f"   Posts encontrados: {len(data)}")
            return True
        elif response.status_code == 401:
            print(f"   ✗ Erro de autenticação (401)")
            print("   Verifique se a chave está correta.")
            return False
        else:
            print(f"   ✗ Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ✗ Erro de conexão - não foi possível conectar ao Supabase")
        return False
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")
        return False

def test_supabase_service_role():
    """Testa a conexão com service role key"""
    
    print("\n3. Testando Service Role Key...")
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not supabase_service_key:
        print("   ⚠ Service Key não configurada")
        return False
    
    try:
        import requests
        
        headers = {
            "Authorization": f"Bearer {supabase_service_key}",
            "apikey": supabase_service_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{supabase_url}/rest/v1/posts?limit=1",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✓ Service Key funcionando!")
            return True
        else:
            print(f"   ✗ Erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    test_supabase_service_role()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ TESTE CONCLUÍDO COM SUCESSO!")
        sys.exit(0)
    else:
        print("✗ TESTE FALHOU")
        sys.exit(1)
