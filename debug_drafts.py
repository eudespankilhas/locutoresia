import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Buscar TODOS os posts draft
print("=== TODOS os posts DRAFT (ultimos 20) ===")
response = supabase.table('posts').select('*').eq('status', 'draft').order('created_at', desc=True).limit(20).execute()

print(f"Total de drafts encontrados na query: {len(response.data)}")
print()

# Mostrar todos
for i, post in enumerate(response.data):
    meta = post.get('metadata', {}) or {}
    voxcraft = meta.get('voxcraft', False)
    title = post['title'][:45] if post['title'] else 'Sem titulo'
    print(f"{i+1:2d}. {post['created_at'][:16]} | Voxcraft: {voxcraft} | {title}")

print()
print("=== Filtrando apenas voxcraft=True ===")
voxcraft_drafts = [p for p in response.data if p.get('metadata', {}).get('voxcraft') == True]
print(f"Drafts com voxcraft=True: {len(voxcraft_drafts)}")

for post in voxcraft_drafts[:5]:
    title = post['title'][:50] if post['title'] else 'Sem titulo'
    print(f"  - {post['created_at'][:16]} | {title}")
