import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== ANALISE DE COMPATIBILIDADE ===")
print()

# Verificar estrutura atual da tabela posts
print("1. Estrutura atual da tabela 'posts':")
result = supabase.table('posts').select('*').limit(1).execute()
if result.data:
    post = result.data[0]
    current_fields = list(post.keys())
    print(f"   Campos existentes: {', '.join(current_fields)}")
    print()

# Campos que a NewPost-IA precisa
newpost_required = ['id', 'content', 'created_at', 'author_id', 'media_urls', 'media_types', 'audio_url', 'updated_at']
newpost_optional = ['is_ia_generated', 'tags', 'network']

# Campos que Locutores IA usa
locutores_uses = ['id', 'title', 'content', 'source_url', 'image_url', 'category', 'status', 'metadata', 'published_at', 'created_at', 'updated_at']

print("2. Analise de conflitos:")
print()

# Verificar quais campos da NewPost-IA ja existem
existing_newpost = [f for f in newpost_required if f in current_fields]
missing_newpost = [f for f in newpost_required if f not in current_fields]

print(f"   Campos da NewPost-IA que JA EXISTEM: {', '.join(existing_newpost) if existing_newpost else 'Nenhum'}")
print(f"   Campos da NewPost-IA que FALTAM: {', '.join(missing_newpost) if missing_newpost else 'Todos existem!'}")
print()

# Verificar conflitos de nome
print("3. Verificando conflitos:")
conflicts = []
if 'title' in current_fields and 'content' in current_fields:
    # Locutores usa 'title', NewPost-IA usa 'content'
    # Isso pode ser OK se ambos existirem
    pass

# Verificar se author_id existe
if 'author_id' not in current_fields:
    print("   ⚠️  author_id NAO existe - NewPost-IA vai quebrar!")
else:
    print("   ✅ author_id existe")

# Verificar se media_urls existe  
if 'media_urls' not in current_fields:
    print("   ⚠️  media_urls NAO existe - NewPost-IA nao vai mostrar imagens!")
else:
    print("   ✅ media_urls existe")

print()
print("4. Estrategias possiveis:")
print()
print("   A) ADICIONAR campos faltantes (author_id, media_urls, etc)")
print("      - Vantagem: NewPost-IA funciona")
print("      - Risco: Nenhum - campos novos nao afetam dados existentes")
print()
print("   B) Criar VIEW ou tabela separada")
print("      - Vantagem: Isolamento total")
print("      - Desvantagem: Mais complexo de manter")
print()
print("   RECOMENDACAO: Opcao A - Adicionar campos necessarios")
print("   Pois campos novos nao quebram dados existentes do Locutores IA")
