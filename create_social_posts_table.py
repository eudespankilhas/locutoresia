# -*- coding: utf-8 -*-
"""
Script para criar a tabela social_posts diretamente no Supabase
via API Management (usando a chave service_role)
Execute: C:\Python313\python.exe create_social_posts_table.py
"""
import sys, os, requests
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, '.')
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv('.env')

SUPABASE_URL   = os.getenv('SUPABASE_URL', '').rstrip('/')
SERVICE_KEY    = os.getenv('SUPABASE_SERVICE_KEY', os.getenv('SUPABASE_ANON_KEY', ''))
PROJECT_REF    = SUPABASE_URL.split('//')[1].split('.')[0] if '//' in SUPABASE_URL else ''

if not SUPABASE_URL or not SERVICE_KEY:
    print("[ERRO] Variaveis SUPABASE_URL e SUPABASE_SERVICE_KEY nao encontradas no .env")
    sys.exit(1)

print(f"[INFO] Projeto Supabase: {PROJECT_REF}")
print(f"[INFO] URL: {SUPABASE_URL}")

# SQL para criar a tabela
SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS public.social_posts (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title       TEXT NOT NULL DEFAULT '',
    caption     TEXT DEFAULT '',
    audio_url   TEXT DEFAULT '',
    audio_project_id TEXT DEFAULT '',
    image_url   TEXT DEFAULT '',
    platforms   JSONB DEFAULT '["newpost_ia"]'::jsonb,
    hashtags    JSONB DEFAULT '[]'::jsonb,
    status      TEXT DEFAULT 'rascunho'
                CHECK (status IN ('rascunho','pendente','aprovado','rejeitado','agendado','publicado','erro')),
    approval_status TEXT DEFAULT 'pendente'
                    CHECK (approval_status IN ('pendente','aprovado','rejeitado')),
    rejection_reason TEXT DEFAULT '',
    approved_by TEXT DEFAULT '',
    approved_at TIMESTAMPTZ,
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    publish_results JSONB DEFAULT '{}'::jsonb,
    ai_caption_generated BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.social_posts ENABLE ROW LEVEL SECURITY;

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies
    WHERE tablename = 'social_posts' AND policyname = 'social_posts_all_access'
  ) THEN
    CREATE POLICY "social_posts_all_access"
      ON public.social_posts FOR ALL USING (true) WITH CHECK (true);
  END IF;
END $$;

CREATE INDEX IF NOT EXISTS idx_social_posts_status    ON public.social_posts(status);
CREATE INDEX IF NOT EXISTS idx_social_posts_created   ON public.social_posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_social_posts_approval  ON public.social_posts(approval_status);

CREATE OR REPLACE FUNCTION public.set_social_posts_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_social_posts_updated ON public.social_posts;
CREATE TRIGGER trg_social_posts_updated
    BEFORE UPDATE ON public.social_posts
    FOR EACH ROW EXECUTE FUNCTION public.set_social_posts_updated_at();

SELECT 'Tabela social_posts criada com sucesso!' AS resultado;
"""

# Tentar via API de management SQL (requer service_role)
print("\n[...] Criando tabela social_posts via API Supabase...")

# Endpoint SQL direto
headers = {
    'apikey': SERVICE_KEY,
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
}

# Tentativa via SQL Management API
mgmt_url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"
resp = requests.post(mgmt_url, headers={
    'Authorization': f'Bearer {SERVICE_KEY}',
    'Content-Type': 'application/json',
}, json={'query': SQL}, timeout=30)

if resp.status_code == 200:
    print("[OK] Tabela criada via Management API!")
    print(resp.text[:300])
else:
    print(f"[AVISO] Management API retornou {resp.status_code}: {resp.text[:200]}")
    print()
    print("=" * 60)
    print("SOLUCAO MANUAL (30 segundos):")
    print("=" * 60)
    print(f"1. Abra: https://supabase.com/dashboard/project/{PROJECT_REF}/sql/new")
    print("2. Cole o SQL abaixo e clique em 'Run':")
    print("-" * 60)

    # SQL simplificado para copiar facilmente
    sql_simples = """CREATE TABLE IF NOT EXISTS public.social_posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL DEFAULT '',
    caption TEXT DEFAULT '',
    audio_url TEXT DEFAULT '',
    audio_project_id TEXT DEFAULT '',
    image_url TEXT DEFAULT '',
    platforms JSONB DEFAULT '["newpost_ia"]'::jsonb,
    hashtags JSONB DEFAULT '[]'::jsonb,
    status TEXT DEFAULT 'rascunho',
    approval_status TEXT DEFAULT 'pendente',
    rejection_reason TEXT DEFAULT '',
    approved_by TEXT DEFAULT '',
    approved_at TIMESTAMPTZ,
    scheduled_at TIMESTAMPTZ,
    published_at TIMESTAMPTZ,
    publish_results JSONB DEFAULT '{}'::jsonb,
    ai_caption_generated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.social_posts ENABLE ROW LEVEL SECURITY;
CREATE POLICY "social_posts_all_access" ON public.social_posts FOR ALL USING (true) WITH CHECK (true);
"""
    print(sql_simples)
    print("-" * 60)

# Verificar se a tabela existe agora
print("\n[...] Verificando se a tabela existe...")
check = requests.get(
    f"{SUPABASE_URL}/rest/v1/social_posts?limit=1",
    headers=headers,
    timeout=10
)
if check.status_code == 200:
    print("[OK] Tabela social_posts encontrada e funcionando!")
    print("[OK] Pode usar o sistema de Posts Sociais normalmente.")
else:
    print(f"[ERRO] Tabela ainda nao existe (HTTP {check.status_code})")
    print("Por favor, execute o SQL manualmente no Supabase Dashboard.")
    print(f"Link: https://supabase.com/dashboard/project/{PROJECT_REF}/sql/new")
