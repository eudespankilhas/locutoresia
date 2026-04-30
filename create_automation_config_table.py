# -*- coding: utf-8 -*-
"""
Script para criar a tabela automation_config no Supabase
Execute: python create_automation_config_table.py
"""
import sys, os, requests
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv('.env')

SUPABASE_URL   = os.getenv('SUPABASE_URL', '').rstrip('/')
SERVICE_KEY    = os.getenv('SUPABASE_SERVICE_KEY', os.getenv('SUPABASE_ANON_KEY', ''))
PROJECT_REF    = SUPABASE_URL.split('//')[1].split('.')[0] if '//' in SUPABASE_URL else ''

if not SUPABASE_URL or not SERVICE_KEY:
    print("[ERRO] Variaveis SUPABASE_URL e SUPABASE_SERVICE_KEY nao encontradas no .env")
    sys.exit(1)

print(f"[INFO] Projeto Supabase: {PROJECT_REF}")
print(f"[INFO] URL: {SUPABASE_URL}")

# SQL para criar a tabela automation_config
SQL = """
-- Remover tabela se existir (para limpar)
DROP TABLE IF EXISTS public.automation_config CASCADE;

-- Criar tabela automation_config (sem foreign key)
CREATE TABLE public.automation_config (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    active_categories TEXT[] DEFAULT '{}',
    schedule_time_1 TIME DEFAULT '09:10:00',
    schedule_time_2 TIME DEFAULT '12:00:00', 
    schedule_time_3 TIME DEFAULT '18:00:00',
    posts_per_category INTEGER DEFAULT 1,
    automation_status_7h BOOLEAN DEFAULT true,
    automation_status_12h BOOLEAN DEFAULT true,
    automation_status_18h BOOLEAN DEFAULT true,
    enabled BOOLEAN DEFAULT false,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Adicionar comentários
COMMENT ON TABLE public.automation_config IS 'Configuração de automação de posts sociais';
COMMENT ON COLUMN public.automation_config.active_categories IS 'Categorias ativas para automação';
COMMENT ON COLUMN public.automation_config.schedule_time_1 IS 'Horário 1 de publicação (7h)';
COMMENT ON COLUMN public.automation_config.schedule_time_2 IS 'Horário 2 de publicação (12h)';
COMMENT ON COLUMN public.automation_config.schedule_time_3 IS 'Horário 3 de publicação (18h)';
COMMENT ON COLUMN public.automation_config.posts_per_category IS 'Posts por categoria em cada horário';
COMMENT ON COLUMN public.automation_config.automation_status_7h IS 'Status da automação 7h';
COMMENT ON COLUMN public.automation_config.automation_status_12h IS 'Status da automação 12h';
COMMENT ON COLUMN public.automation_config.automation_status_18h IS 'Status da automação 18h';
COMMENT ON COLUMN public.automation_config.enabled IS 'Automação habilitada/desabilitada';

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_automation_config_enabled ON public.automation_config(enabled);
CREATE INDEX IF NOT EXISTS idx_automation_config_created_at ON public.automation_config(created_at DESC);

-- Habilitar RLS (Row Level Security)
ALTER TABLE public.automation_config ENABLE ROW LEVEL SECURITY;

-- Política para permitir leitura pública (somente para status)
CREATE POLICY "Permitir leitura pública de status" ON public.automation_config
    FOR SELECT USING (true);

-- Política para permitir inserção via service role
CREATE POLICY "Permitir inserção via service role" ON public.automation_config
    FOR INSERT WITH CHECK (true);

-- Política para permitir atualização via service role
CREATE POLICY "Permitir atualização via service role" ON public.automation_config
    FOR UPDATE USING (true);

-- Política para permitir deleção via service role
CREATE POLICY "Permitir deleção via service role" ON public.automation_config
    FOR DELETE USING (true);

-- Criar trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER automation_config_updated_at
    BEFORE UPDATE ON public.automation_config
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();
"""

# Headers para a requisição
headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=minimal'
}

# URL da API SQL do Supabase
sql_url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"

print("[INFO] Criando tabela automation_config via SQL...")

# URL para SQL Editor API
sql_headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json'
}

try:
    # Usar SQL Editor API
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/sql",
        headers=sql_headers,
        json={"query": SQL},
        timeout=30
    )
    
    if response.status_code in (200, 201, 204):
        print("[OK] Tabela automation_config criada com sucesso!")
    else:
        print(f"[AVISO] Método 1 falhou: {response.status_code}")
        print("[INFO] Tentando método alternativo...")
        
        # Método alternativo: criar tabela via INSERT direto (força criação)
        try:
            test_data = {
                "active_categories": ["Tecnologia"],
                "schedule_time_1": "09:10:00",
                "schedule_time_2": "12:00:00",
                "schedule_time_3": "18:00:00",
                "posts_per_category": 1,
                "enabled": True
            }
            
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/automation_config",
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            if response.status_code == 201:
                print("[OK] Tabela automation_config criada via INSERT!")
            else:
                print(f"[ERRO] Falha ao criar tabela: {response.status_code}")
                print(f"[ERRO] Resposta: {response.text}")
                print("\n[INFO] Por favor, crie a tabela manualmente no painel do Supabase:")
                print(f"URL: {SUPABASE_URL.replace('.supabase.co', '.supabase.co/project/_/sql')}")
                print("\nSQL para executar manualmente:")
                print(SQL[:500] + "...")
                sys.exit(1)
                
        except Exception as e2:
            print(f"[ERRO] Método alternativo falhou: {e2}")
            sys.exit(1)
        
except Exception as e:
    print(f"[ERRO] Exceção ao criar tabela: {e}")
    sys.exit(1)

print("[INFO] Verificando se tabela foi criada...")

# Verificar se tabela existe
try:
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/automation_config?select=id&limit=1",
        headers=headers,
        timeout=10
    )
    
    if response.status_code == 200:
        print("[OK] Tabela automation_config está acessível!")
        print("[OK] Configuração de automação pronta para uso!")
    else:
        print(f"[ERRO] Tabela não acessível: {response.status_code}")
        print(f"[ERRO] Resposta: {response.text}")
        
except Exception as e:
    print(f"[ERRO] Erro ao verificar tabela: {e}")

print("\n[INFO] Script concluído!")
