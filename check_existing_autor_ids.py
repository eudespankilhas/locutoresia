#!/usr/bin/env python3
"""Verifica os autor_ids existentes em newpost_posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== VERIFICANDO AUTOR_IDS EXISTENTES ===\n")

try:
    result = supabase.table('newpost_posts').select('autor_id').execute()
    
    if result.data:
        autor_ids = set([post['autor_id'] for post in result.data])
        print(f"Total de posts: {len(result.data)}")
        print(f"Total de autor_ids unicos: {len(autor_ids)}")
        print(f"\nAutor IDs encontrados:")
        for autor_id in autor_ids:
            print(f"  {autor_id}")
            
        # Contar posts por autor
        from collections import Counter
        autor_count = Counter([post['autor_id'] for post in result.data])
        print(f"\nPosts por autor:")
        for autor_id, count in autor_count.items():
            print(f"  {autor_id}: {count} posts")
            
        # Usar o autor_id mais comum para o NewsAgent
        most_common = autor_count.most_common(1)[0]
        print(f"\nAutor ID mais comum: {most_common[0]} ({most_common[1]} posts)")
        
        # Salvar para uso futuro
        with open('newsagent_autor_id.txt', 'w') as f:
            f.write(most_common[0])
        print(f"ID salvo em newsagent_autor_id.txt")
        
    else:
        print("Nenhum post encontrado")
        
except Exception as e:
    print(f"Erro: {e}")
