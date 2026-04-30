-- Criar tabela de posts para Locutores IA
CREATE TABLE IF NOT EXISTS posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT,
    content TEXT NOT NULL,
    image_url TEXT,
    hashtags TEXT[] DEFAULT '{}',
    status TEXT DEFAULT 'draft',
    source TEXT DEFAULT 'manual',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status);
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);

-- Habilitar RLS (Row Level Security)
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Política para permitir leitura pública
CREATE POLICY "Allow public read" ON posts
    FOR SELECT USING (true);

-- Política para permitir escrita com service role
CREATE POLICY "Allow service role write" ON posts
    FOR ALL USING (true) WITH CHECK (true);

-- Comentário da tabela
COMMENT ON TABLE posts IS 'Posts sociais do Locutores IA';
