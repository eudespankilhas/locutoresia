-- Adicionar TODAS as colunas necessárias à tabela social_posts

-- Colunas básicas
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS caption TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS platform TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS approval_status TEXT DEFAULT 'pending';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS priority INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS scheduled_at TIMESTAMPTZ;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS error_message TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS retry_count INTEGER DEFAULT 0;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}';

-- Colunas de áudio/IA
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS audio_url TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS ai_caption_generated BOOLEAN DEFAULT FALSE;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS ai_caption TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS voice_id TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS voice_name TEXT DEFAULT '';

-- Colunas de publicação
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS published_to TEXT[] DEFAULT '{}';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS is_auto_generated BOOLEAN DEFAULT FALSE;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS news_source TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS news_url TEXT DEFAULT '';

-- Verificar todas as colunas
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'social_posts'
ORDER BY ordinal_position;
