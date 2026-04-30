import os
os.environ['SUPABASE_URL'] = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
os.environ['SUPABASE_SERVICE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'

from supabase import create_client
supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_SERVICE_KEY'])

# Buscar posts mais recentes (qualquer status)
print("=== Posts mais recentes (todos os status) ===")
response = supabase.table('posts').select('*').order('created_at', desc=True).limit(10).execute()

for i, post in enumerate(response.data):
    meta = post.get('metadata', {}) or {}
    print(f"{i+1}. {post['created_at'][:16]} | Status: {post['status']:<8} | Voxcraft: {meta.get('voxcraft', False):<5} | {post['title'][:40]}")

print()
print("=== Posts DRAFT com voxcraft=True ===")
drafts = [p for p in response.data if p['status'] == 'draft' and p.get('metadata', {}).get('voxcraft')]
print(f"Encontrados: {len(drafts)}")
for post in drafts:
    print(f"  - {post['created_at'][:16]} | {post['title'][:40]}")

print()
print("=== Analise de status dos posts ===")
status_counts = {}
for post in response.data:
    status = post['status']
    status_counts[status] = status_counts.get(status, 0) + 1
for status, count in status_counts.items():
    print(f"  {status}: {count}")
