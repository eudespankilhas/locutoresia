-- Ativar RLS e criar políticas para a tabela posts
-- Isso permite que o NewsAgent salve notícias corretamente

-- 1. Ativar RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 2. Criar política para INSERT (permitir publicação)
CREATE POLICY "Permitir inserção de posts"
ON posts FOR INSERT
WITH CHECK (true);

-- 3. Criar política para UPDATE (permitir atualizar status)
CREATE POLICY "Permitir atualizar posts"
ON posts FOR UPDATE
USING (true)
WITH CHECK (true);

-- 4. Criar política para SELECT (permitir ler posts)
CREATE POLICY "Permitir ler posts"
ON posts FOR SELECT
USING (true);
