#!/usr/bin/env python3
"""Testa publicação de uma notícia nova com status 'ready' e voxcraft: True"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from supabase import create_client
import random
from datetime import datetime

SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ykswhzqdjoshjoaruhqs.supabase.co')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

print("=== TESTANDO PUBLICACAO COM STATUS 'ready' E VOXCRAFT ===\n")

# Criar uma notícia nova com timestamp único
timestamp = datetime.now().strftime("%H:%M:%S")
title = f"Teste NewsAgent - {timestamp} - Nova Tecnologia Brasileira"
category = "tecnologia"
hashtags = ["#tecnologia", "#NewsAgent", "#LocutoresIA", "#Brasil"]
content = f"Esta é uma notícia de teste do NewsAgent gerada às {timestamp}. O sistema de publicação automática está funcionando corretamente.\n\n{' '.join(hashtags)}"

# Gerar imagem URL
seed = random.randint(1, 999999)
image_prompt = f"Brazilian technology innovation, digital transformation, modern Brazil, high quality"
image_url = f"https://image.pollinations.ai/prompt/{image_prompt.replace(' ', '%20')}?width=1024&height=1024&nologo=true&seed={seed}&model=flux-realism"

print(f"Título: {title}")
print(f"Status: ready")
print(f"Voxcraft: True")
print()

try:
    result = supabase.table('posts').insert({
        'title': title,
        'content': content,
        'source_url': 'https://locutoresia.com/test',
        'image_url': image_url,
        'category': category,
        'status': 'ready',  # Status 'ready'
        'metadata': {
            'author': 'newsagent',
            'source': 'NewsAgent',
            'is_ia_generated': True,
            'voxcraft': True  # Voxcraft: True
        }
    }).execute()
    
    print("✅ Post criado com sucesso!")
    print(f"  ID: {result.data[0]['id']}")
    print(f"  Status: {result.data[0]['status']}")
    print(f"  Metadata: {result.data[0]['metadata']}")
    print(f"  Criado: {result.data[0]['created_at']}")
    
    print("\n🔍 Verifique agora em: https://plugpost-ai.lovable.app")
    print("O post deve aparecer com status 'ready' e voxcraft: True")
    
except Exception as e:
    print(f"❌ Erro: {e}")
