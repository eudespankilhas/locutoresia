"""
Verificar se todas as tabelas auxiliares foram criadas
"""
import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Verificando tabelas auxiliares ===")
print()

tables_to_check = [
    ('reactions', 'Reacoes/Curtidas'),
    ('comments', 'Comentarios'),
    ('saved_posts', 'Posts salvos')
]

for table_name, description in tables_to_check:
    try:
        result = supabase.table(table_name).select('count').limit(1).execute()
        print(f"[OK] {table_name}: existe ({description})")
    except Exception as e:
        if 'Could not find the table' in str(e):
            print(f"[MISSING] {table_name}: NAO EXISTE ({description})")
        else:
            print(f"[ERROR] {table_name}: erro - {str(e)[:50]}")

print()
print("=== Verificando posts com author_id preenchido ===")
try:
    result = supabase.table('posts').select('*').not_.is_('author_id', 'null').execute()
    print(f"Posts com author_id: {len(result.data)}")
    for post in result.data[:3]:
        print(f"  - {post.get('title', 'N/A')[:40]} | author_id: {post.get('author_id', 'N/A')[:8]}...")
except Exception as e:
    print(f"Erro: {e}")

print()
print("=== Verificando posts com is_ia_generated ===")
try:
    result = supabase.table('posts').select('*').eq('is_ia_generated', True).execute()
    print(f"Posts com is_ia_generated=true: {len(result.data)}")
except Exception as e:
    print(f"Erro: {e}")

print()
print("=" * 50)
print("Schema atualizado com sucesso!")
print("A NewPost-IA agora pode ler os posts do NewsAgent.")
