import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

print("=== Verificando newpost_profiles ===")
try:
    profiles = supabase.table('newpost_profiles').select('*').limit(5).execute()
    print(f"Perfis encontrados: {len(profiles.data)}")
    for profile in profiles.data:
        print(f"\n  ID: {profile.get('id', 'N/A')}")
        print(f"  Nome: {profile.get('nome', profile.get('name', profile.get('full_name', 'N/A')))}")
        print(f"  Email: {profile.get('email', 'N/A')}")
        print(f"  Role: {profile.get('role', profile.get('tipo', 'N/A'))}")
        
    # Verificar se nosso autor_id existe
    target_author = '3a1a93d0-e451-47a4-a126-f1b7375895eb'
    print(f"\n\n=== Verificando se autor {target_author} existe ===")
    author_check = supabase.table('newpost_profiles').select('*').eq('id', target_author).execute()
    if author_check.data:
        print("✓ Autor encontrado!")
        print(f"  Nome: {author_check.data[0].get('nome', 'N/A')}")
    else:
        print("✗ Autor NAO encontrado!")
        print("Isso pode ser o problema - posts com autor_id inexistente")
        
except Exception as e:
    print(f"Erro: {e}")
