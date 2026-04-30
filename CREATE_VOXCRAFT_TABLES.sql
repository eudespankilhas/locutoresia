-- Criar tabelas do VoxCraft Engine para workflow completo de publicação automática
-- Projeto: ravpbfkicqkwjxejuzty

-- Tabela voxcraft_posts: Metadata dos posts gerados (workflow de curadoria)
CREATE TABLE IF NOT EXISTS public.voxcraft_posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    original_title TEXT,
    original_url TEXT,
    source_name TEXT,
    category TEXT NOT NULL,
    keywords TEXT[] DEFAULT '{}',
    coherence_score NUMERIC DEFAULT 0 CHECK (coherence_score >= 0 AND coherence_score <= 10),
    image_source TEXT DEFAULT 'pollinations',
    status TEXT DEFAULT 'pendente' CHECK (status IN ('pendente', 'aprovado', 'revisao_humana', 'disparado', 'descartado')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabela voxcraft_logs: Logs do sistema em tempo real
CREATE TABLE IF NOT EXISTS public.voxcraft_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    event TEXT NOT NULL,
    detail TEXT,
    category TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_voxcraft_posts_status ON public.voxcraft_posts(status);
CREATE INDEX IF NOT EXISTS idx_voxcraft_posts_category ON public.voxcraft_posts(category);
CREATE INDEX IF NOT EXISTS idx_voxcraft_posts_created_at ON public.voxcraft_posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_voxcraft_logs_created_at ON public.voxcraft_logs(created_at DESC);

-- Trigger para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_voxcraft_posts_updated_at
    BEFORE UPDATE ON public.voxcraft_posts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Habilitar RLS (Row Level Security)
ALTER TABLE public.voxcraft_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.voxcraft_logs ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso (permitir tudo para service role)
CREATE POLICY "Service role full access on voxcraft_posts"
    ON public.voxcraft_posts
    FOR ALL
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role full access on voxcraft_logs"
    ON public.voxcraft_logs
    FOR ALL
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');

-- Comentários
COMMENT ON TABLE public.voxcraft_posts IS 'Metadata dos posts gerados pelo VoxCraft Engine - workflow de curadoria';
COMMENT ON TABLE public.voxcraft_logs IS 'Logs do sistema VoxCraft em tempo real';
