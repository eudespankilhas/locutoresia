import os
from supabase import create_client
import json

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

print('Testando salvamento direto no Supabase...')

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Teste de inserção manual
    test_data = {
        "title": "TESTE - Notícia do NewsAgent",
        "source_url": "https://test.com/news123",
        "content": "Conteúdo de teste da notícia",
        "image_url": "https://image.com/test.jpg",
        "category": "teste",
        "status": "draft",
        "published_at": "2026-04-24T16:00:00",
        "metadata": {
            "author": "newsagent",
            "source": "Teste",
            "is_ia_generated": True,
            "voxcraft": True
        }
    }
    
    result = supabase.table('posts').insert(test_data).execute()
    
    if result.data:
        print('✅ SUCESSO: Notícia inserida!')
        print(f'ID: {result.data[0]["id"]}')
        print(f'Título: {result.data[0]["title"]}')
        print(f'Voxcraft: {result.data[0]["metadata"]["voxcraft"]}')
    else:
        print('❌ ERRO: Falha ao inserir')
        print(f'Erro: {result.get("error", "Desconhecido")}')
        
except Exception as e:
    print(f'❌ ERRO: {e}')
    print(f'Tipo: {type(e).__name__}')
