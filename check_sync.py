import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Verificar se o post foi sincronizado
result = supabase.table('newpost_posts').select('*').ilike('titulo', '%TESTE%').execute()

if result.data:
    print('SINCRONIZADO!')
    for post in result.data:
        print(f"ID: {post['id'][:8]}... | Titulo: {post['titulo'][:40]}")
else:
    print('NAO sincronizado - verificando posts recentes...')
    recent = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(5).execute()
    for p in recent.data:
        print(f"- {p['titulo'][:50]}")
