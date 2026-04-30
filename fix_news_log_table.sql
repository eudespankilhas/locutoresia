-- SQL para adicionar coluna created_at na tabela news_log
-- Execute este SQL no painel do Supabase > SQL Editor

ALTER TABLE news_log ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
ALTER TABLE news_log ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();

-- Criar índice para created_at se não existir
CREATE INDEX IF NOT EXISTS idx_news_log_created_at ON news_log(created_at);
