#!/usr/bin/env python3
"""Verifica onde estão as notícias coletadas"""

import sqlite3
import os
from datetime import datetime

print("=== VERIFICANDO NOTÍCIAS ===\n")

# 1. Verificar cache local (SQLite)
print("1. CACHE LOCAL (news_cache.db):")
print("-" * 40)
if os.path.exists('news_cache.db'):
    conn = sqlite3.connect('news_cache.db')
    cursor = conn.cursor()
    
    # Total de notícias
    cursor.execute("SELECT COUNT(*) FROM news")
    total = cursor.fetchone()[0]
    print(f"Total no cache: {total} notícias")
    
    # Notícias recentes (últimas 2 horas)
    cursor.execute("""
        SELECT title, source, category, collected_at 
        FROM news 
        WHERE collected_at > datetime('now', '-2 hours')
        ORDER BY collected_at DESC
        LIMIT 10
    """)
    recent = cursor.fetchall()
    print(f"\nNotícias recentes (últimas 2h): {len(recent)}")
    for n in recent:
        print(f"  - [{n[1]}] {n[0][:50]}... ({n[3]})")
    conn.close()
else:
    print("Arquivo news_cache.db não encontrado")

print("\n" + "="*60)
print("\n2. SUPABASE (tabela newpost_posts):")
print("-" * 40)

try:
    from supabase import create_client
    
    SUPABASE_URL = 'https://ykswhzqdjoshjoaruhqs.supabase.co'
    SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'
    
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Total de posts
    result = supabase.table('newpost_posts').select('*', count='exact').execute()
    print(f"Total em newpost_posts: {result.count} posts")
    
    # Posts do NewsAgent
    result2 = supabase.table('newpost_posts').select('*').eq('origem', 'NewsAgent Auto-Post').execute()
    print(f"Posts do NewsAgent: {len(result2.data)}")
    
    # Posts recentes (últimas 2 horas)
    from datetime import timedelta
    cutoff = (datetime.now() - timedelta(hours=2)).isoformat()
    result3 = supabase.table('newpost_posts').select('*').gte('criado_em', cutoff).order('criado_em', desc=True).execute()
    print(f"\nPosts recentes (últimas 2h): {len(result3.data)}")
    for post in result3.data[:5]:
        titulo = post.get('titulo', 'N/A')
        status = post.get('status', 'N/A')
        criado = post.get('criado_em', 'N/A')
        print(f"  - [{status}] {titulo[:50]}... ({criado})")
    
    print(f"\n✅ Verifique em: https://plugpost-ai.lovable.app/")
    
except Exception as e:
    print(f"Erro ao verificar Supabase: {e}")

print("\n" + "="*60)
print("\nResumo:")
print("- Cache local: notícias coletadas mas não publicadas")
print("- newpost_posts: posts publicados na NewPost-IA")
