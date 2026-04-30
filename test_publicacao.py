#!/usr/bin/env python3
"""Testa a publicação de uma notícia"""

import sys
sys.path.insert(0, 'backend')

from news_agent import NewsAgent

agent = NewsAgent()

# Testar publicação com uma notícia de exemplo
teste_news = {
    'title': 'Teste de Publicacao NewsAgent - ' + __import__('datetime').datetime.now().strftime('%H:%M:%S'),
    'snippet': 'Esta é uma notícia de teste para verificar se a publicação na NewPost-IA está funcionando corretamente.',
    'url': 'https://exame.com/teste-newsagent',
    'source': 'Teste',
    'category': 'tecnologia'
}

print("=== TESTANDO PUBLICACAO ===")
print(f"Titulo: {teste_news['title']}")
print(f"Source: {teste_news['source']}")
print()

# Tentar publicar (via DatabaseManager)
resultado = agent.db.save_to_supabase(teste_news)
print(f"\nResultado: {resultado}")
print("\nVerifique em: https://plugpost-ai.lovable.app/")
