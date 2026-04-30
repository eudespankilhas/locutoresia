-- Adicionar coluna audio_url à tabela social_posts
ALTER TABLE social_posts ADD COLUMN IF NOT EXISTS audio_url TEXT DEFAULT '';

-- Verificar se foi adicionada
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'social_posts'
ORDER BY ordinal_position;
