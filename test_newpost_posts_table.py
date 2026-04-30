#!/usr/bin/env python3
"""Testa publicação na tabela newpost_posts"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
from datetime import datetime

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== TESTANDO PUBLICACAO EM newpost_posts ===\n")

# Author ID válido
autor_id = "3a1a93d0-e451-47a4-a126-f1b7375895eb"

# Criar timestamp único
timestamp = datetime.now().strftime("%H:%M:%S")
titulo = f"Teste NewsAgent newpost_posts - {timestamp} - Tecnologia Brasileira"
descricao = "Esta é uma notícia de teste do NewsAgent publicada na tabela newpost_posts."
conteudo = f"Conteúdo completo da notícia de teste gerada às {timestamp}. O sistema de publicação automática está funcionando."
hashtags = ["#tecnologia", "#NewsAgent", "#LocutoresIA", "#Brasil", "#NewPostIA"]

print(f"Título: {titulo}")
print(f"Autor ID: {autor_id}")
print(f"Hashtags: {hashtags}")
print()

try:
    result = supabase.table('newpost_posts').insert({
        'autor_id': autor_id,
        'titulo': titulo,
        'descricao': descricao,
        'conteudo': conteudo,
        'hashtags': hashtags,
        'audio_url': None
    }).execute()
    
    print("✅ Post criado em newpost_posts com sucesso!")
    print(f"  ID: {result.data[0]['id']}")
    print(f"  Título: {result.data[0]['titulo']}")
    print(f"  Criado em: {result.data[0]['criado_em']}")
    
    print("\n🔍 Verifique agora em: https://plugpost-ai.lovable.app")
    print("O post deve aparecer pois foi publicado na tabela newpost_posts")
    
except Exception as e:
    print(f"❌ Erro: {e}")
