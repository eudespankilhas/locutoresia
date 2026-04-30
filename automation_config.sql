-- SQL para criar tabela automation_config no Supabase
-- Execute este SQL manualmente no painel do Supabase: https://ykswhzqdjoshjoaruhqs.supabase.co/project/_/sql

-- Remover tabela se existir
DROP TABLE IF EXISTS public.automation_config CASCADE;

-- Criar tabela automation_config (sem user_id para simplificar)
CREATE TABLE public.automation_config (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    active_categories TEXT[] DEFAULT '{}',
    schedule_time_1 TIME DEFAULT '09:10:00',
    schedule_time_2 TIME DEFAULT '12:00:00', 
    schedule_time_3 TIME DEFAULT '18:00:00',
    posts_per_category INTEGER DEFAULT 1,
    automation_status_7h BOOLEAN DEFAULT true,
    automation_status_12h BOOLEAN DEFAULT true,
    automation_status_18h BOOLEAN DEFAULT true,
    enabled BOOLEAN DEFAULT false,
    timezone TEXT DEFAULT 'America/Sao_Paulo',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Adicionar comentários
COMMENT ON TABLE public.automation_config IS 'Configuração de automação de posts sociais';
COMMENT ON COLUMN public.automation_config.active_categories IS 'Categorias ativas para automação';
COMMENT ON COLUMN public.automation_config.schedule_time_1 IS 'Horário 1 de publicação (7h)';
COMMENT ON COLUMN public.automation_config.schedule_time_2 IS 'Horário 2 de publicação (12h)';
COMMENT ON COLUMN public.automation_config.schedule_time_3 IS 'Horário 3 de publicação (18h)';
COMMENT ON COLUMN public.automation_config.posts_per_category IS 'Posts por categoria em cada horário';
COMMENT ON COLUMN public.automation_config.enabled IS 'Automação habilitada/desabilitada';

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_automation_config_enabled ON public.automation_config(enabled);
CREATE INDEX IF NOT EXISTS idx_automation_config_created_at ON public.automation_config(created_at DESC);

-- Habilitar RLS (Row Level Security)
ALTER TABLE public.automation_config ENABLE ROW LEVEL SECURITY;

-- Políticas para permitir acesso total (para simplificar)
CREATE POLICY "Permitir tudo" ON public.automation_config FOR ALL USING (true);

-- Criar trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER automation_config_updated_at
    BEFORE UPDATE ON public.automation_config
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();

-- Inserir configuração padrão para teste
INSERT INTO public.automation_config (active_categories, enabled)
VALUES (ARRAY['Tecnologia', 'Esportes'], true);
