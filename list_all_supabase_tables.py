#!/usr/bin/env python3
"""Lista todas as tabelas do Supabase para identificar a tabela correta da NewPost-IA"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== LISTANDO TODAS AS TABELAS DO SUPABASE ===\n")

# Lista de possíveis tabelas
all_possible_tables = [
    'posts', 'newpost_posts', 'social_posts', 'publications',
    'profiles', 'newpost_profiles', 'user_profiles', 'users',
    'user_roles', 'sources', 'automation_config', 'news_cycles',
    'scheduled_posts', 'voxcraft_posts', 'voxcraft_status', 'voxcraft_logs',
    'feed', 'timeline', 'home_posts', 'user_posts', 'all_posts',
    'comments', 'likes', 'shares', 'notifications',
    'media', 'images', 'videos', 'audio',
    'categories', 'tags', 'hashtags',
    'settings', 'config', 'preferences'
]

for table in all_possible_tables:
    try:
        result = supabase.table(table).select('*').limit(1).execute()
        if result.data:
            print(f"[OK] {table}: {len(result.data)} registros")
            print(f"  Colunas: {list(result.data[0].keys())}")
            
            # Se tiver dados, mostrar um exemplo
            if result.data:
                print(f"  Exemplo de dados:")
                for key, value in result.data[0].items():
                    if isinstance(value, str) and len(value) > 50:
                        print(f"    {key}: {value[:50]}...")
                    else:
                        print(f"    {key}: {value}")
        else:
            print(f"[OK] {table}: vazia")
    except Exception as e:
        print(f"[ERRO] {table}: {str(e)[:50]}")
    print()

print("\n" + "="*60)
print("=== VERIFICANDO O POST DE TESTE CRIADO ===\n")

# Buscar o post de teste específico
result = supabase.table('posts').select('*').eq('title', 'Teste NewsAgent - 09:45:35 - Nova Tecnologia Brasileira').execute()

if result.data:
    print("Post de teste encontrado:")
    post = result.data[0]
    for key, value in post.items():
        print(f"  {key}: {value}")
else:
    print("Post de teste NÃO encontrado na tabela posts")

# Verificar em newpost_posts também
result_newpost = supabase.table('newpost_posts').select('*').eq('titulo', 'Teste NewsAgent - 09:45:35 - Nova Tecnologia Brasileira').execute()

if result_newpost.data:
    print("\nPost de teste encontrado em newpost_posts:")
    post = result_newpost.data[0]
    for key, value in post.items():
        print(f"  {key}: {value}")
else:
    print("Post de teste NÃO encontrado na tabela newpost_posts")
