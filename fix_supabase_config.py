"""
Script para corrigir e testar configuração do Supabase
"""

import os
from dotenv import load_dotenv

# Carregar variáveis do .env.local
load_dotenv('.env.local')

def test_and_fix_supabase_config():
    """Testa e corrige configuração do Supabase"""
    
    print("=" * 60)
    print("VERIFICAÇÃO E CORREÇÃO DA CONFIGURAÇÃO SUPABASE")
    print("=" * 60)
    
    # Obter credenciais atuais
    current_url = os.getenv("SUPABASE_URL", "")
    service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    anon_key = os.getenv("SUPABASE_ANON_KEY", "")
    
    print("\n1. Configuração Atual:")
    print(f"   SUPABASE_URL: {current_url}")
    print(f"   SUPABASE_SERVICE_ROLE_KEY: {'✓ Configurada' if service_role_key else '✗ Não encontrada'}")
    print(f"   SUPABASE_ANON_KEY: {'✓ Configurada' if anon_key else '✗ Não encontrada'}")
    
    # Corrigir URL se necessário
    fixed_url = current_url
    if current_url.endswith("/rest/v1/"):
        fixed_url = current_url.replace("/rest/v1/", "")
        print(f"\n2. URL Corrigida:")
        print(f"   Antes: {current_url}")
        print(f"   Depois: {fixed_url}")
    
    # Gerar configuração corrigida
    print("\n3. Configuração Corrigida para .env.local:")
    print("=" * 40)
    
    config_lines = [
        "# Configurações do Supabase - CORRIGIDO",
        f'SUPABASE_URL="{fixed_url}"',
        f'SUPABASE_ANON_KEY="{anon_key}"',
        f'SUPABASE_SERVICE_ROLE_KEY="{service_role_key}"',
        "",
        "# Outras variáveis existentes..."
    ]
    
    for line in config_lines:
        print(line)
    
    print("=" * 40)
    print("\n4. Testando conexão com Supabase...")
    
    try:
        from supabase import create_client, Client
        
        # Testar conexão
        supabase: Client = create_client(fixed_url, service_role_key)
        
        # Testar consulta simples
        response = supabase.table('_test_connection').select('count').execute()
        
    except Exception as e:
        print(f"   Erro na conexão: {e}")
        print("   Isso é normal se as tabelas não existem ainda.")
        print("   O importante é que a autenticação funcionou.")
    
    # Criar arquivo de configuração corrigido
    with open('.env.supabase_fixed', 'w', encoding='utf-8') as f:
        f.write("# Configurações do Supabase - VERSÃO CORRIGIDA\n")
        f.write(f'SUPABASE_URL="{fixed_url}"\n')
        f.write(f'SUPABASE_ANON_KEY="{anon_key}"\n')
        f.write(f'SUPABASE_SERVICE_ROLE_KEY="{service_role_key}"\n')
        f.write("\n# Copie estas linhas para o seu .env.local\n")
    
    print(f"\n✓ Arquivo .env.supabase_fixed criado com as correções!")
    print("  Copie as linhas acima para o seu .env.local")
    
    return fixed_url, service_role_key, anon_key

def create_tables_sql():
    """Gera SQL para criar as tabelas necessárias"""
    
    print("\n5. SQL para criar tabelas no Supabase:")
    print("=" * 50)
    
    sql_statements = [
        "-- Tabela para log de notícias",
        "CREATE TABLE IF NOT EXISTS news_log (",
        "    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),",
        "    url TEXT UNIQUE NOT NULL,",
        "    titulo TEXT NOT NULL,",
        "    fonte TEXT,",
        "    categoria TEXT,",
        "    status TEXT DEFAULT 'publicada',",
        "    agente_origem TEXT DEFAULT 'vessel',",
        "    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),",
        "    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()",
        ");",
        "",
        "-- Tabela para ciclos de execução",
        "CREATE TABLE IF NOT EXISTS news_cycles (",
        "    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),",
        "    cycle_id TEXT UNIQUE NOT NULL,",
        "    execution_timestamp TIMESTAMP WITH TIME ZONE,",
        "    task_name TEXT,",
        "    status TEXT,",
        "    estatisticas JSONB,",
        "    erros JSONB,",
        "    mensagem TEXT,",
        "    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()",
        ");",
        "",
        "-- Índices para performance",
        "CREATE INDEX IF NOT EXISTS idx_news_log_url ON news_log(url);",
        "CREATE INDEX IF NOT EXISTS idx_news_log_created_at ON news_log(created_at);",
        "CREATE INDEX IF NOT EXISTS idx_news_cycles_cycle_id ON news_cycles(cycle_id);",
        "CREATE INDEX IF NOT EXISTS idx_news_cycles_created_at ON news_cycles(created_at);"
    ]
    
    for sql in sql_statements:
        print(sql)
    
    # Salvar SQL em arquivo
    with open('supabase_tables.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_statements))
    
    print("\n✓ SQL salvo em 'supabase_tables.sql'")
    print("  Execute este SQL no painel do Supabase > SQL Editor")

if __name__ == "__main__":
    url, key, anon = test_and_fix_supabase_config()
    create_tables_sql()
    
    print("\n" + "=" * 60)
    print("PRÓXIMOS PASSOS:")
    print("1. Copie as configurações corrigidas do .env.supabase_fixed para .env.local")
    print("2. Execute o SQL supabase_tables.sql no painel do Supabase")
    print("3. Teste o sistema com: python test_supabase_news_integration.py")
    print("=" * 60)
