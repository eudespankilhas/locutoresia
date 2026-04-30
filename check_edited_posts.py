from supabase import create_client
import os

SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Buscar todos os posts recentes
response = supabase.table('posts').select('*').order('created_at', desc=True).limit(10).execute()

print("=== Últimos 10 posts na tabela 'posts' ===\n")

for post in response.data:
    print(f"ID: {post['id']}")
    print(f"Título: {post.get('title', 'N/A')[:50]}...")
    print(f"Status: {post.get('status', 'N/A')}")
    print(f"Metadata: {post.get('metadata', {})}")
    print(f"É editado? {post.get('metadata', {}).get('edited', False)}")
    print("-" * 50)
