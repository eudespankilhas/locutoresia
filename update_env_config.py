"""
Script para atualizar .env.local com configurações Supabase corrigidas
"""

import os
import shutil
from datetime import datetime

def update_env_local():
    """Atualiza .env.local com as configurações corrigidas do Supabase"""
    
    print("=" * 60)
    print("ATUALIZANDO .env.local COM CONFIGURAÇÕES SUPABASE")
    print("=" * 60)
    
    # Fazer backup do .env.local atual
    if os.path.exists('.env.local'):
        backup_name = f".env.local.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy('.env.local', backup_name)
        print(f"1. Backup criado: {backup_name}")
    
    # Ler configurações corrigidas
    try:
        with open('.env.supabase_fixed', 'r', encoding='utf-8') as f:
            supabase_config = f.read()
        print("2. Configurações Supabase lidas com sucesso")
    except FileNotFoundError:
        print("2. ERRO: Arquivo .env.supabase_fixed não encontrado!")
        return False
    
    # Ler .env.local atual
    current_env = {}
    if os.path.exists('.env.local'):
        try:
            with open('.env.local', 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        current_env[key] = value
            print("3. Configurações atuais do .env.local lidas")
        except Exception as e:
            print(f"3. Erro ao ler .env.local: {e}")
    
    # Atualizar apenas as variáveis Supabase
    lines_to_update = []
    for line in supabase_config.split('\n'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            lines_to_update.append((key, value))
    
    # Criar novo conteúdo .env.local
    new_env_lines = []
    
    # Adicionar configurações não-Supabase existentes
    for key, value in current_env.items():
        if not key.startswith('SUPABASE_'):
            new_env_lines.append(f"{key}={value}")
    
    # Adicionar configurações Supabase corrigidas
    new_env_lines.append("")
    new_env_lines.append("# Configurações do Supabase - ATUALIZADO")
    for key, value in lines_to_update:
        new_env_lines.append(f"{key}={value}")
    
    # Escrever novo .env.local
    try:
        with open('.env.local', 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_env_lines))
        print("4. .env.local atualizado com sucesso!")
    except Exception as e:
        print(f"4. ERRO ao atualizar .env.local: {e}")
        return False
    
    # Verificar atualização
    print("\n5. Verificando configurações atualizadas:")
    supabase_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY']
    
    for var in supabase_vars:
        value = os.getenv(var)
        if value:
            print(f"   {var}: {'OK' if 'supabase' in value.lower() else 'PROBLEMA'}")
        else:
            print(f"   {var}: Não encontrada (recarregue as variáveis)")
    
    print("\n6. Para recarregar as variáveis de ambiente:")
    print("   - Reinicie seu terminal")
    print("   - Ou execute: python -c \"from dotenv import load_dotenv; load_dotenv()\"")
    
    return True

def test_updated_config():
    """Testa a configuração atualizada"""
    
    print("\n" + "=" * 60)
    print("TESTANDO CONFIGURAÇÃO ATUALIZADA")
    print("=" * 60)
    
    # Recarregar variáveis
    from dotenv import load_dotenv
    load_dotenv('.env.local')
    
    # Verificar variáveis
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY']
    
    print("\n1. Verificando variáveis de ambiente:")
    all_ok = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'supabase' in value.lower():
                print(f"   {var}: OK")
            else:
                print(f"   {var}: Formato inválido?")
                all_ok = False
        else:
            print(f"   {var}: Não encontrada")
            all_ok = False
    
    if not all_ok:
        print("\nERRO: Algumas variáveis não estão configuradas corretamente!")
        return False
    
    print("\n2. Testando conexão com Supabase:")
    
    try:
        from supabase import create_client
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        supabase = create_client(url, key)
        print("   Cliente Supabase criado com sucesso")
        
        # Testar se as tabelas existem
        try:
            response = supabase.table('news_log').select('count').execute()
            print("   Tabela news_log: OK")
        except Exception as e:
            print(f"   Tabela news_log: Não encontrada (normal se ainda não criada)")
        
        try:
            response = supabase.table('news_cycles').select('count').execute()
            print("   Tabela news_cycles: OK")
        except Exception as e:
            print(f"   Tabela news_cycles: Não encontrada (normal se ainda não criada)")
        
        print("\n   Conexão estabelecida com sucesso!")
        return True
        
    except Exception as e:
        print(f"   ERRO na conexão: {e}")
        return False

if __name__ == "__main__":
    success = update_env_local()
    
    if success:
        test_updated_config()
        
        print("\n" + "=" * 60)
        print("RESUMO:")
        print("1. .env.local atualizado com configurações Supabase corrigidas")
        print("2. Backup criado do arquivo original")
        print("3. Próximo passo: Execute o SQL supabase_tables.sql no painel Supabase")
        print("4. Depois: Teste com python test_supabase_news_integration.py")
        print("=" * 60)
    else:
        print("\nERRO: Falha na atualização do .env.local")
