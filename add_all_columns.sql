-- Adicionar todas as colunas necessárias à tabela social_posts

ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS audio_url TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS ai_caption_generated BOOLEAN DEFAULT FALSE;
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS ai_caption TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS voice_id TEXT DEFAULT '';
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS voice_name TEXT DEFAULT '';
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
