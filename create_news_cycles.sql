-- SQL para criar apenas a tabela news_cycles que está faltando
-- Execute este SQL no painel do Supabase > SQL Editor

CREATE TABLE IF NOT EXISTS news_cycles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cycle_id TEXT UNIQUE NOT NULL,
    execution_timestamp TIMESTAMP WITH TIME ZONE,
    task_name TEXT,
    status TEXT,
    estatisticas JSONB,
    erros JSONB,
    mensagem TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índice para performance
CREATE INDEX IF NOT EXISTS idx_news_cycles_cycle_id ON news_cycles(cycle_id);
CREATE INDEX IF NOT EXISTS idx_news_cycles_created_at ON news_cycles(created_at);
