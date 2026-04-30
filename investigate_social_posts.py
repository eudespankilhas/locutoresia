#!/usr/bin/env python3
"""Investiga a tabela social_posts detalhadamente"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.supabase_config import get_supabase_client

supabase = get_supabase_client()

print("=== INVESTIGANDO TABELA social_posts ===\n")

# Buscar todos os social_posts
result = supabase.table('social_posts').select('*').order('created_at', desc=True).limit(20).execute()
posts = result.data if result.data else []

print(f"Total de social_posts: {len(posts)}\n")

if posts:
    print(f"Colunas: {list(posts[0].keys())}\n")
    
    print("--- REGISTROS ---")
    for i, post in enumerate(posts[:10], 1):
        print(f"\nRegistro {i}:")
        print(f"  ID: {post.get('id')}")
        print(f"  Título: {post.get('title', 'N/A')}")
        print(f"  Status: {post.get('status')}")
        print(f"  Approval Status: {post.get('approval_status')}")
        print(f"  Scheduled At: {post.get('scheduled_at')}")
        print(f"  Published At: {post.get('published_at')}")
        print(f"  Platforms: {post.get('platforms')}")
        print(f"  Hashtags: {post.get('hashtags')}")
        print(f"  Created At: {post.get('created_at')}")

# Verificar status distribution
print("\n" + "="*60)
print("=== DISTRIBUICAO DE STATUS ===\n")

status_count = {}
approval_count = {}

for post in posts:
    status = post.get('status', 'unknown')
    approval = post.get('approval_status', 'unknown')
    
    status_count[status] = status_count.get(status, 0) + 1
    approval_count[approval] = approval_count.get(approval, 0) + 1

print("Status:")
for status, count in status_count.items():
    print(f"  {status}: {count}")

print("\nApproval Status:")
for approval, count in approval_count.items():
    print(f"  {approval}: {count}")

# Verificar agendamentos futuros
print("\n" + "="*60)
print("=== AGENDAMENTOS FUTUROS ===\n")

from datetime import datetime

scheduled_future = []
for post in posts:
    scheduled_at = post.get('scheduled_at')
    if scheduled_at:
        scheduled_time = datetime.fromisoformat(scheduled_at.replace('Z', '+00:00'))
        if scheduled_time > datetime.now(scheduled_time.tzinfo):
            scheduled_future.append(post)

print(f"Agendamentos futuros: {len(scheduled_future)}")
for post in scheduled_future[:5]:
    print(f"  {post.get('title', 'N/A')} - {post.get('scheduled_at')}")
