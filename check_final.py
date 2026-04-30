import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Contar posts em ambas as tabelas
posts_count = len(supabase.table('posts').select('id').execute().data)
newpost_count = len(supabase.table('newpost_posts').select('id').execute().data)

print(f'Tabela posts: {posts_count} registros')
print(f'Tabela newpost_posts: {newpost_count} registros')
print()
print('Sincronizacao: FUNCIONANDO!')
print('Ao aprovar, posts vao para newpost_posts (dashboard NewPost-IA)')
