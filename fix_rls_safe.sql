-- Ativar RLS e recriar políticas (versão segura)

-- 1. Ativar RLS (ignora se já estiver ativado)
ALTER TABLE IF EXISTS posts ENABLE ROW LEVEL SECURITY;

-- 2. Remover políticas existentes (se houver) para recriar
DROP POLICY IF EXISTS "Permitir inserção de posts" ON posts;
DROP POLICY IF EXISTS "Permitir atualizar posts" ON posts;
DROP POLICY IF EXISTS "Permitir ler posts" ON posts;

-- 3. Criar políticas novas
CREATE POLICY "Permitir inserção de posts"
ON posts FOR INSERT
WITH CHECK (true);

CREATE POLICY "Permitir atualizar posts"
ON posts FOR UPDATE
USING (true)
WITH CHECK (true);

CREATE POLICY "Permitir ler posts"
ON posts FOR SELECT
USING (true);

-- 4. Política para DELETE (opcional, mas útil)
CREATE POLICY "Permitir deletar posts"
ON posts FOR DELETE
USING (true);
