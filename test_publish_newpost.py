#!/usr/bin/env python3
"""Testa publicação direta na tabela newpost_posts via Supabase"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.supabase_config import get_supabase_client
from datetime import datetime
import uuid
import os

# Usar SERVICE KEY para contornar RLS
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

from supabase import create_client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== TESTANDO PUBLICACAO DIRETA EM newpost_posts ===\n")

# Ler o autor_id existente
try:
    with open('newsagent_autor_id.txt', 'r') as f:
        autor_id = f.read().strip()
except:
    autor_id = "3a1a93d0-e451-47a4-a126-f1b7375895eb"  # ID padrão

# Criar um post de teste
test_post = {
    "autor_id": autor_id,  # Usar autor_id existente
    "titulo": "Teste de Publicação - NewsAgent",
    "descricao": "Este é um post de teste do NewsAgent para verificar a publicação automática",
    "conteudo": "Conteúdo completo do post de teste do NewsAgent. Este post foi gerado automaticamente pelo agente de notícias do Locutores IA.",
    "hashtags": ["teste", "newsagent", "locutoresia", "newpost"],
    "audio_url": None
}

print("Post de teste:")
print(f"  Título: {test_post['titulo']}")
print(f"  Autor: {test_post['autor_id']}")
print(f"  Hashtags: {test_post['hashtags']}")
print()

try:
    print("Inserindo no Supabase...")
    result = supabase.table('newpost_posts').insert(test_post).execute()
    
    if result.data:
        print("✅ SUCESSO! Post inserido com ID:", result.data[0]['id'])
        print(f"  Criado em: {result.data[0]['criado_em']}")
    else:
        print("❌ Erro: Nenhum dado retornado")
        
except Exception as e:
    print(f"❌ Erro ao inserir: {e}")

# Verificar se o post foi inserido
print("\n=== VERIFICANDO SE O POST FOI INSERIDO ===\n")

try:
    result = supabase.table('newpost_posts').select('*').eq('titulo', 'Teste de Publicação - NewsAgent').execute()
    
    if result.data:
        print(f"✅ Post encontrado! Total: {len(result.data)}")
        for post in result.data:
            print(f"  ID: {post['id']}")
            print(f"  Título: {post['titulo']}")
            print(f"  Criado em: {post['criado_em']}")
    else:
        print("❌ Post não encontrado")
        
except Exception as e:
    print(f"❌ Erro ao verificar: {e}")
