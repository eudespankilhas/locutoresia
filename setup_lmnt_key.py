"""
Script para configurar API Key do LMNT

Execute este script para configurar sua API Key real do LMNT.
"""

import os

def setup_lmnt_key():
    """Configura a API Key do LMNT"""
    
    print("🔧 Configurando API Key do LMNT")
    print("=" * 40)
    
    # Pedir API Key ao usuário
    api_key = input("Digite sua API Key do LMNT: ").strip()
    
    if not api_key:
        print("❌ API Key não pode ser vazia!")
        return False
    
    # Configurar variável de ambiente para a sessão atual
    os.environ['LMNT_API_KEY'] = api_key
    
    # Salvar em arquivo .env (se não existir)
    env_file = '.env'
    try:
        with open(env_file, 'w') as f:
            f.write(f"LMNT_API_KEY={api_key}\n")
        print(f"✅ API Key salva em {env_file}")
    except Exception as e:
        print(f"⚠️  Não foi possível salvar em .env: {e}")
        print("   A API Key está configurada apenas para esta sessão.")
    
    print(f"✅ API Key configurada: {api_key[:10]}...")
    return True

def test_connection():
    """Testa a conexão com a API Key configurada"""
    
    print("\n🧪 Testando conexão com LMNT...")
    
    try:
        from lmnt import Lmnt
        
        client = Lmnt()
        account = client.accounts.retrieve()
        
        print("✅ Conexão bem-sucedida!")
        print(f"   Email: {account.email}")
        print(f"   Créditos restantes: {account.credits_remaining}")
        print(f"   Plano: {account.plan}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

if __name__ == "__main__":
    # Configurar API Key
    if setup_lmnt_key():
        # Testar conexão
        if test_connection():
            print("\n🎉 Tudo pronto! Você já pode usar o SDK LMNT.")
            print("\n💡 Para testar novamente, execute:")
            print("   py test_lmnt_official.py")
        else:
            print("\n⚠️  Verifique sua API Key e tente novamente.")
    else:
        print("\n❌ Configuração cancelada.")
