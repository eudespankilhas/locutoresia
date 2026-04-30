#!/usr/bin/env python3
"""Teste simples de coleta e salvamento no Supabase"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from news_agent import NewsAgent

agent = NewsAgent()

# Coletar notícias de uma fonte
print("Coletando notícias de G1 - Brasil...")
news = agent.collect_from_source("g1", "brasil")

print(f"Coletadas {len(news)} notícias")

# Salvar no banco
saved, duplicates = agent.db.save_news(news)
print(f"Salvas: {saved}, Duplicadas: {duplicates}")

# Verificar no Supabase
try:
    from backend.supabase_config import get_supabase_client
    supabase = get_supabase_client()
    result = supabase.table('publications').select('*').execute()
    print(f"Total no Supabase: {len(result.data)}")
except Exception as e:
    print(f"Erro ao verificar Supabase: {e}")
