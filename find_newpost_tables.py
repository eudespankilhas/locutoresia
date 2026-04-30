import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Tentar acessar tabelas comuns de redes sociais
print("=== Procurando tabela da NewPost-IA ===")

tables_to_try = [
    'posts',           # Ja vimos - Locutores IA
    'newpost_posts',   # Tabela de sincronizacao
    'publications',
    'feed_posts',
    'timeline_posts',
    'social_posts',
    'content_posts',
    'user_posts',
]

for table in tables_to_try:
    try:
        result = supabase.table(table).select('count').limit(1).execute()
        # Se chegou aqui, a tabela existe
        count_result = supabase.table(table).select('*', count='exact').limit(100).execute()
        count = len(count_result.data)
        print(f"✓ {table}: {count} registros")
        
        # Se for posts, verificar estrutura
        if table == 'posts' and count > 0:
            sample = count_result.data[0]
            print(f"  Campos: {', '.join(sample.keys())}")
            
    except Exception as e:
        error_msg = str(e)
        if 'Could not find the table' in error_msg:
            print(f"✗ {table}: nao existe")
        else:
            print(f"? {table}: erro - {error_msg[:50]}")

print("\n=== Verificando se posts tem author_id ===")
try:
    # Verificar se algum post tem author_id preenchido
    result = supabase.table('posts').select('*').not_.is_('author_id', 'null').limit(5).execute()
    print(f"Posts com author_id: {len(result.data)}")
    for p in result.data[:3]:
        print(f"  - {p.get('author_id', 'N/A')[:20]}... | Content: {str(p.get('content', 'N/A'))[:30]}")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== Posts SEM author_id (Locutores IA) ===")
try:
    result = supabase.table('posts').select('*').is_('author_id', 'null').limit(5).execute()
    print(f"Posts sem author_id: {len(result.data)}")
    for p in result.data[:3]:
        print(f"  - {p.get('id', 'N/A')[:20]}... | Status: {p.get('status', 'N/A')} | Title: {str(p.get('title', 'N/A'))[:30]}")
except Exception as e:
    print(f"Erro: {e}")
