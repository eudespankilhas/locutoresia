-- ============================================================
-- CRIAR TABELA social_posts NO SUPABASE
-- Locutores IA × NewPost-IA
--
-- COMO USAR:
-- 1. Acesse: https://supabase.com/dashboard/project/ykswhzqdjoshjoaruhqs/sql/new
-- 2. Cole este SQL inteiro
-- 3. Clique em "Run"
-- ============================================================

-- Criar a extensão uuid-ossp se não existir
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Remover tabela se existir (para recriar limpa)
-- DROP TABLE IF EXISTS public.social_posts;

-- Criar tabela social_posts
CREATE TABLE IF NOT EXISTS public.social_posts (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,

    -- Conteúdo do post
    title       TEXT NOT NULL DEFAULT '',
    caption     TEXT DEFAULT '',
    audio_url   TEXT DEFAULT '',
    audio_project_id TEXT DEFAULT '',
    image_url   TEXT DEFAULT '',

    -- Plataformas e hashtags (JSONB para flexibilidade)
    platforms   JSONB DEFAULT '["newpost_ia"]'::jsonb,
    hashtags    JSONB DEFAULT '[]'::jsonb,

    -- Status do post
    status      TEXT DEFAULT 'rascunho'
                CHECK (status IN ('rascunho','pendente','aprovado','rejeitado','agendado','publicado','erro')),

    -- Aprovação pelo gestor
    approval_status TEXT DEFAULT 'pendente'
                    CHECK (approval_status IN ('pendente','aprovado','rejeitado')),
    rejection_reason TEXT DEFAULT '',
    approved_by TEXT DEFAULT '',
    approved_at TIMESTAMPTZ,

    -- Agendamento e publicação
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,

    -- Resultado da publicação por plataforma (JSON)
    publish_results JSONB DEFAULT '{}'::jsonb,

    -- Flags IA
    ai_caption_generated BOOLEAN DEFAULT FALSE,

    -- Timestamps
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE public.social_posts ENABLE ROW LEVEL SECURITY;

-- Política: acesso total (ajuste se usar autenticação)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE tablename = 'social_posts' AND policyname = 'social_posts_all_access'
  ) THEN
    CREATE POLICY "social_posts_all_access"
      ON public.social_posts
      FOR ALL
      USING (true)
      WITH CHECK (true);
  END IF;
END
$$;

-- ============================================================
-- ÍNDICES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_social_posts_status
    ON public.social_posts(status);

CREATE INDEX IF NOT EXISTS idx_social_posts_created
    ON public.social_posts(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_social_posts_approval
    ON public.social_posts(approval_status);

-- ============================================================
-- TRIGGER: atualiza updated_at automaticamente
-- ============================================================
CREATE OR REPLACE FUNCTION public.set_social_posts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_social_posts_updated ON public.social_posts;
CREATE TRIGGER trg_social_posts_updated
    BEFORE UPDATE ON public.social_posts
    FOR EACH ROW
    EXECUTE FUNCTION public.set_social_posts_updated_at();

-- ============================================================
-- VERIFICAÇÃO FINAL
-- ============================================================
SELECT
    column_name,
    data_type,
    column_default,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'social_posts'
ORDER BY ordinal_position;
