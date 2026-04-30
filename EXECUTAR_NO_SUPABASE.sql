-- ===========================================
-- MIGRACAO: Adaptar tabela posts para NewPost-IA
-- Execute no Supabase Dashboard: SQL Editor -> New Query
-- ===========================================

-- 1. Adicionar campos necessarios na tabela posts
ALTER TABLE posts
    ADD COLUMN IF NOT EXISTS author_id UUID REFERENCES newpost_profiles(id),
    ADD COLUMN IF NOT EXISTS media_urls TEXT[],
    ADD COLUMN IF NOT EXISTS media_types TEXT[],
    ADD COLUMN IF NOT EXISTS audio_url TEXT,
    ADD COLUMN IF NOT EXISTS is_ia_generated BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS tags TEXT[];

-- 2. Criar tabela de reacoes (curtidas)
CREATE TABLE IF NOT EXISTS reactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    type TEXT NOT NULL DEFAULT 'like',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

-- 3. Criar tabela de comentarios
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Criar tabela de posts salvos
CREATE TABLE IF NOT EXISTS saved_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

-- 5. Criar indexes para performance
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_is_ia_generated ON posts(is_ia_generated);
CREATE INDEX IF NOT EXISTS idx_reactions_post_id ON reactions(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_saved_posts_user_id ON saved_posts(user_id);

-- 6. Atualizar posts existentes do NewsAgent para ter author_id
-- Isso faz posts antigos aparecerem na NewPost-IA
UPDATE posts 
SET author_id = '3a1a93d0-e451-47a4-a126-f1b7375895eb',
    is_ia_generated = TRUE
WHERE author_id IS NULL 
  AND (metadata->>'voxcraft' = 'true' OR metadata->>'author' = 'newsagent');

-- ===========================================
-- FIM DA MIGRACAO
-- ===========================================
