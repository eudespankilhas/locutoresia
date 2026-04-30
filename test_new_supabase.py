#!/usr/bin/env python3
"""Testar conexão com novo Supabase"""

from supabase import create_client

SUPABASE_URL = "https://ravpbfkicqkwjxejuzty.supabase.co"
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM"

print("="*60)
print("TESTANDO NOVO SUPABASE")
print(f"URL: {SUPABASE_URL}")
print("="*60)

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    
    # Testar leitura
    print("\n1. Testando leitura...")
    result = supabase.table('posts').select('*').limit(1).execute()
    print(f"   ✅ OK - Tabela existe!")
    
    # Testar inserção
    print("\n2. Testando escrita...")
    test_post = {
        'title': 'Teste de Conexão',
        'content': 'Post de teste para verificar se tudo funciona!',
        'hashtags': ['#teste', '#locutoresia'],
        'status': 'draft'
    }
    insert = supabase.table('posts').insert(test_post).execute()
    
    if insert.data:
        new_id = insert.data[0]['id']
        print(f"   ✅ OK - Post criado: {new_id}")
        
        # Limpar
        supabase.table('posts').delete().eq('id', new_id).execute()
        print(f"   ✅ OK - Post removido (limpeza)")
    
    print("\n" + "="*60)
    print("🎉 SUPABASE CONFIGURADO COM SUCESSO!")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    print("\n💡 Dica: Execute o SQL no Editor SQL do Supabase primeiro!")
