-- Tabela para log de notícias
CREATE TABLE IF NOT EXISTS news_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    url TEXT UNIQUE NOT NULL,
    titulo TEXT NOT NULL,
    fonte TEXT,
    categoria TEXT,
    status TEXT DEFAULT 'publicada',
    agente_origem TEXT DEFAULT 'vessel',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela para ciclos de execução
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

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_news_log_url ON news_log(url);
CREATE INDEX IF NOT EXISTS idx_news_log_created_at ON news_log(created_at);
CREATE INDEX IF NOT EXISTS idx_news_cycles_cycle_id ON news_cycles(cycle_id);
CREATE INDEX IF NOT EXISTS idx_news_cycles_created_at ON news_cycles(created_at);