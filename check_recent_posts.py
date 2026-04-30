from supabase import create_client

supabase = create_client(
    'https://ykswhzqdjoshjoaruhqs.supabase.co', 
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'
)

result = supabase.table('newpost_posts').select('*').order('criado_em', desc=True).limit(10).execute()

print('=== Posts recentes em newpost_posts ===')
for p in result.data:
    titulo = p.get('titulo', 'N/A')[:50]
    criado = p.get('criado_em', 'N/A')
    print(f"- {titulo}... | {criado}")
