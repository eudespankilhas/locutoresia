-- Criar tabela social_posts (nome correto para o sistema)
CREATE TABLE IF NOT EXISTS social_posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL DEFAULT '',
    caption TEXT DEFAULT '',
    content TEXT NOT NULL DEFAULT '',
    image_url TEXT DEFAULT '',
    hashtags TEXT[] DEFAULT '{}',
    platform TEXT DEFAULT '',
    status TEXT DEFAULT 'draft',
    approval_status TEXT DEFAULT 'pending',
    priority INTEGER DEFAULT 0,
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE social_posts ENABLE ROW LEVEL SECURITY;

-- Política de acesso
CREATE POLICY "social_posts_all_access" ON social_posts FOR ALL USING (true) WITH CHECK (true);

-- Índices
CREATE INDEX IF NOT EXISTS idx_social_posts_status ON social_posts(status);
CREATE INDEX IF NOT EXISTS idx_social_posts_created ON social_posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_social_posts_approval ON social_posts(approval_status);
