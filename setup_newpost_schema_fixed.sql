-- ===========================================
-- MIGRACAO: Adaptar tabela posts para NewPost-IA (SEM foreign key)
-- Data: 2026-04-28
-- ===========================================

-- 1. Adicionar campos necessarios na tabela posts (se nao existirem)
DO $$
BEGIN
    -- Adicionar author_id (UUID, sem foreign key para compatibilidade)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'author_id') THEN
        ALTER TABLE posts ADD COLUMN author_id UUID;
        COMMENT ON COLUMN posts.author_id IS 'ID do autor do post';
    END IF;

    -- Adicionar media_urls (array de textos)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'media_urls') THEN
        ALTER TABLE posts ADD COLUMN media_urls TEXT[] DEFAULT NULL;
        COMMENT ON COLUMN posts.media_urls IS 'Array de URLs de midia (imagens, videos)';
    END IF;

    -- Adicionar media_types (array de textos)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'media_types') THEN
        ALTER TABLE posts ADD COLUMN media_types TEXT[] DEFAULT NULL;
        COMMENT ON COLUMN posts.media_types IS 'Array de tipos de midia (image, video, audio)';
    END IF;

    -- Adicionar audio_url (texto)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'audio_url') THEN
        ALTER TABLE posts ADD COLUMN audio_url TEXT DEFAULT NULL;
        COMMENT ON COLUMN posts.audio_url IS 'URL do arquivo de audio do post';
    END IF;

    -- Adicionar is_ia_generated (booleano)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'is_ia_generated') THEN
        ALTER TABLE posts ADD COLUMN is_ia_generated BOOLEAN DEFAULT FALSE;
        COMMENT ON COLUMN posts.is_ia_generated IS 'Indica se o post foi gerado por IA';
    END IF;

    -- Adicionar tags (array de textos)
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'posts' AND column_name = 'tags') THEN
        ALTER TABLE posts ADD COLUMN tags TEXT[] DEFAULT NULL;
        COMMENT ON COLUMN posts.tags IS 'Tags/hashtags do post';
    END IF;
END $$;

-- 2. Criar tabela de reacoes (curtidas) se nao existir
CREATE TABLE IF NOT EXISTS reactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    type TEXT NOT NULL DEFAULT 'like',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id, type)
);

COMMENT ON TABLE reactions IS 'Reacoes (curtidas) nos posts';

-- 3. Criar tabela de comentarios se nao existir
CREATE TABLE IF NOT EXISTS comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE comments IS 'Comentarios nos posts';

-- 4. Criar tabela de posts salvos se nao existir
CREATE TABLE IF NOT EXISTS saved_posts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(post_id, user_id)
);

COMMENT ON TABLE saved_posts IS 'Posts salvos pelos usuarios';

-- 5. Criar indexes para performance
CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_reactions_post_id ON reactions(post_id);
CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id);
CREATE INDEX IF NOT EXISTS idx_saved_posts_user_id ON saved_posts(user_id);

-- 6. Atualizar TODOS os posts existentes para ter author_id padrao
-- Usando o autor padrao (usuario principal: newplugpostia@gmail.com)
UPDATE posts 
SET author_id = '3a1a93d0-e451-47a4-a126-f1b7375895eb',
    is_ia_generated = TRUE
WHERE author_id IS NULL;

-- ===========================================
-- MIGRACAO CONCLUIDA
-- ===========================================
