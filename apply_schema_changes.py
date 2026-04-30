"""
Script para aplicar alteracoes de schema no Supabase
Adiciona campos necessarios para NewPost-IA na tabela posts
"""
import os
import sys

os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

def check_column_exists(table_name, column_name):
    """Verifica se uma coluna existe na tabela"""
    try:
        # Tentar selecionar a coluna
        result = supabase.table(table_name).select(column_name).limit(1).execute()
        return True
    except Exception as e:
        if 'column' in str(e).lower() and 'does not exist' in str(e).lower():
            return False
        # Se der outro erro, a coluna pode existir mas ter outro problema
        return True

def add_column_via_rpc(column_name, column_type, default_value=None):
    """Tenta adicionar coluna via RPC (funcao customizada)"""
    try:
        # Tentar usar a funcao exec_sql se existir
        query = f"ALTER TABLE posts ADD COLUMN IF NOT EXISTS {column_name} {column_type}"
        if default_value is not None:
            query += f" DEFAULT {default_value}"
        
        result = supabase.rpc('exec_sql', {'query': query}).execute()
        print(f"✓ Coluna {column_name} adicionada via RPC")
        return True
    except Exception as e:
        print(f"✗ RPC falhou para {column_name}: {e}")
        return False

def main():
    print("=== Aplicando alteracoes de schema ===")
    print()
    
    # Verificar colunas necessarias
    columns_needed = {
        'author_id': 'uuid',
        'media_urls': 'text[]',
        'media_types': 'text[]',
        'audio_url': 'text',
        'is_ia_generated': 'boolean',
        'tags': 'text[]'
    }
    
    print("1. Verificando colunas existentes:")
    for col_name, col_type in columns_needed.items():
        exists = check_column_exists('posts', col_name)
        if exists:
            print(f"   ✓ {col_name}: ja existe")
        else:
            print(f"   ✗ {col_name}: NAO existe (necessario adicionar)")
    
    print()
    print("2. Tentando adicionar colunas via API:")
    
    # Como nao podemos executar SQL diretamente via REST API sem funcao RPC,
    # vamos criar um registro de teste para verificar a estrutura
    
    print()
    print("=== INSTRUCOES MANUAIS ===")
    print()
    print("Execute o seguinte SQL no Dashboard do Supabase:")
    print("(SQL Editor -> New Query)")
    print()
    print("-" * 60)
    
    sql = """
-- Adicionar campos necessarios para NewPost-IA
ALTER TABLE posts 
    ADD COLUMN IF NOT EXISTS author_id UUID REFERENCES newpost_profiles(id),
    ADD COLUMN IF NOT EXISTS media_urls TEXT[],
    ADD COLUMN IF NOT EXISTS media_types TEXT[],
    ADD COLUMN IF NOT EXISTS audio_url TEXT,
    ADD COLUMN IF NOT EXISTS is_ia_generated BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS tags TEXT[];

-- Criar tabelas auxiliares
CREATE TABLE IF NOT EXISTS reactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    type TEXT NOT NULL DEFAULT 'like',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS saved_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

-- Atualizar posts existentes do NewsAgent
UPDATE posts 
SET author_id = '3a1a93d0-e451-47a4-a126-f1b7375895eb',
    is_ia_generated = TRUE
WHERE author_id IS NULL 
  AND metadata->>'voxcraft' = 'true';
"""
    print(sql)
    print("-" * 60)
    
    # Salvar SQL em arquivo
    with open('apply_schema_manual.sql', 'w', encoding='utf-8') as f:
        f.write(sql)
    
    print()
    print("SQL tambem salvo em: apply_schema_manual.sql")
    print()
    print("=== PROXIMA ETAPA ===")
    print("Apos executar o SQL manualmente, atualizaremos o codigo")
    print("para sincronizar posts corretamente.")

if __name__ == '__main__':
    main()
