"""
Verificar quais colunas existem na tabela posts
"""
import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Verificando colunas na tabela 'posts' ===")
print()

# Verificar cada coluna necessaria
columns_to_check = [
    ('author_id', 'UUID do autor'),
    ('media_urls', 'Array de URLs de midia'),
    ('media_types', 'Array de tipos de midia'),
    ('audio_url', 'URL do audio'),
    ('is_ia_generated', 'Flag de IA'),
    ('tags', 'Tags do post')
]

missing_columns = []

for col_name, description in columns_to_check:
    try:
        result = supabase.table('posts').select(col_name).limit(1).execute()
        print(f"[OK] {col_name}: existe ({description})")
    except Exception as e:
        if 'does not exist' in str(e).lower():
            print(f"[MISSING] {col_name}: NAO EXISTE ({description})")
            missing_columns.append(col_name)
        else:
            print(f"[ERROR] {col_name}: erro ao verificar - {e}")

print()
print("=" * 50)
if missing_columns:
    print(f"Colunas faltantes: {', '.join(missing_columns)}")
    print()
    print("Execute este SQL no Supabase Dashboard:")
    print()
    print("ALTER TABLE posts")
    for i, col in enumerate(missing_columns):
        comma = "," if i < len(missing_columns) - 1 else ";"
        if col == 'author_id':
            print(f"    ADD COLUMN IF NOT EXISTS {col} UUID REFERENCES newpost_profiles(id){comma}")
        elif col in ['media_urls', 'media_types', 'tags']:
            print(f"    ADD COLUMN IF NOT EXISTS {col} TEXT[]{comma}")
        elif col == 'is_ia_generated':
            print(f"    ADD COLUMN IF NOT EXISTS {col} BOOLEAN DEFAULT FALSE{comma}")
        else:
            print(f"    ADD COLUMN IF NOT EXISTS {col} TEXT{comma}")
else:
    print("Todas as colunas existem! Schema esta pronto.")
