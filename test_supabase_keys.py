#!/usr/bin/env python3
"""
Script para verificar qual chave do Supabase está funcionando
Testa anon key vs service_role key
"""

from supabase import create_client

# Configurações do projeto NewPost-IA
SUPABASE_URL = "https://hzmtdfojctctvgqjdbex.supabase.co"

# Chaves para testar
CHAVES = {
    "Publishable (Anon)": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6bXRkZm9qY3RjdHZncWpkYmV4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2NDUwMTIsImV4cCI6MjA3OTIyMTAxMn0.bv_6SFc_vNnw_eIyD73xNsRVXtL0guSbMRNuCthIy4Q",
    "Service Role": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh6bXRkZm9qY3RjdHZncWpkYmV4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjY0NTAxMiwiZXhwIjoyMDkyMjIxMDEyfQ.bv_6SFc_vNnw_eIyD73xNsRVXtL0guSbMRNuCthIy4Q"
}

print("="*70)
print("TESTE DE CHAVES SUPABASE - NewPost-IA")
print(f"URL: {SUPABASE_URL}")
print("="*70)

for nome_chave, chave in CHAVES.items():
    print(f"\n{'-'*70}")
    print(f"Testando: {nome_chave}")
    print(f"Chave: {chave[:50]}...")
    
    try:
        # Criar cliente
        supabase = create_client(SUPABASE_URL, chave)
        
        # Teste 1: Ler da tabela newpost_posts
        print("\n1. Testando LEITURA (select)...")
        result = supabase.table('newpost_posts').select('*').limit(1).execute()
        print(f"   ✅ LEITURA OK - Encontrados: {len(result.data)} registros")
        
        # Teste 2: Tentar inserir um registro de teste
        print("\n2. Testando ESCRITA (insert)...")
        test_data = {
            'titulo': 'Teste de Chave - ' + nome_chave,
            'descricao': 'Teste automatizado de verificação de chave',
            'conteudo': 'Este é um post de teste para verificar se a chave tem permissão de escrita.',
            'hashtags': ['#teste', '#verificacao'],
            'autor_id': '3a1a93d0-e451-47a4-a126-f1b7375895eb',
            'status': 'rascunho'
        }
        
        insert_result = supabase.table('newpost_posts').insert(test_data).execute()
        
        if insert_result.data:
            novo_id = insert_result.data[0].get('id')
            print(f"   ✅ ESCRITA OK - Post criado com ID: {novo_id}")
            
            # Limpar - deletar o post de teste
            print("\n3. Limpando teste (delete)...")
            supabase.table('newpost_posts').delete().eq('id', novo_id).execute()
            print(f"   ✅ LIMPEZA OK - Post de teste removido")
            
            print(f"\n🎉 CHAVE '{nome_chave}' FUNCIONA COMPLETAMENTE!")
        else:
            print(f"   ⚠️ ESCRITA retornou vazio")
            
    except Exception as e:
        erro_str = str(e)
        if "Invalid API key" in erro_str:
            print(f"   ❌ CHAVE INVÁLIDA: {erro_str}")
        elif "row-level security" in erro_str.lower() or "rls" in erro_str.lower():
            print(f"   ⚠️ RLS bloqueando: {erro_str[:100]}...")
        else:
            print(f"   ❌ ERRO: {erro_str[:150]}...")

print("\n" + "="*70)
print("RESUMO:")
print("- Service Role Key = Permissão total (leitura + escrita)")
print("- Anon Key = Geralmente só leitura (bloqueada por RLS)")
print("="*70)
