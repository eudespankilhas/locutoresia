import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Estrutura da tabela 'posts' ===")
result = supabase.table('posts').select('*').limit(1).execute()
if result.data:
    post = result.data[0]
    print("Todos os campos:")
    for key, value in sorted(post.items()):
        value_type = type(value).__name__
        value_preview = str(value)[:40] if value is not None else "None"
        print(f"  {key}: {value_type}")
        print(f"    Valor: {value_preview}")
        print()
