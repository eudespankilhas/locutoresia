from supabase import create_client
from datetime import datetime, timedelta

supabase = create_client(
    'https://ykswhzqdjoshjoaruhqs.supabase.co',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'
)

# Buscar posts das ultimas 2 horas
cutoff = (datetime.now() - timedelta(hours=2)).isoformat()
result = supabase.table('newpost_posts').select('*').gte('criado_em', cutoff).order('criado_em', desc=True).execute()

print('Posts das ultimas 2 horas:', len(result.data))
for p in result.data:
    titulo = p.get('titulo', 'N/A')[:60]
    criado = p.get('criado_em', 'N/A')
    print('- ' + titulo + '... | ' + criado)
