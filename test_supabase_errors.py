"""
Script automático para identificar os 2 erros do Supabase
"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

class SupabaseErrorTester:
    def __init__(self):
        load_dotenv('.env.local', override=True)
        
        self.base_url = os.getenv("SUPABASE_URL", "").strip()
        self.service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()
        self.anon_key = os.getenv("SUPABASE_ANON_KEY", "").strip()
        
        self.news_log_url = f"{self.base_url.rstrip('/')}/rest/v1/news_log"
        
        print("🔧 CONFIGURAÇÃO:")
        print(f"   Base URL: {self.base_url}")
        print(f"   Service Key: {'✓' if self.service_key else '✗'}")
        print(f"   Anon Key: {'✓' if self.anon_key else '✗'}")
        print(f"   News Log URL: {self.news_log_url}")
    
    def test_connection(self):
        """Testa conexão básica com Supabase"""
        
        print("\n🔌 TESTE 1: CONEXÃO BÁSICA")
        print("-" * 40)
        
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}"
        }
        
        try:
            # Teste simples: contar registros
            response = requests.get(f"{self.news_log_url}?select=id", headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if data else 0
                print(f"   ✅ Conexão OK - Total registros: {count}")
                return True, count
            else:
                print(f"   ❌ Erro: {response.text}")
                return False, 0
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            return False, 0
    
    def get_table_structure(self):
        """Obtém estrutura da tabela news_log"""
        
        print("\n🏗️ TESTE 2: ESTRUTURA DA TABELA")
        print("-" * 40)
        
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Accept": "application/vnd.pgrst.object+json"
        }
        
        try:
            # Tentar obter um registro para ver a estrutura
            response = requests.get(f"{self.news_log_url}?select=*&limit=1", headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    print("   ✅ Campos encontrados:")
                    for campo, valor in data[0].items():
                        tipo = type(valor).__name__
                        print(f"      - {campo} ({tipo})")
                    return list(data[0].keys())
                else:
                    print("   ⚠️ Tabela vazia, mas acessível")
                    return []
            else:
                print(f"   ❌ Erro: {response.text}")
                return []
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            return []
    
    def test_minimal_insert(self):
        """Testa inserção mínima para identificar ERRO 1"""
        
        print("\n📝 TESTE 3: INSERÇÃO MÍNIMA (ERRO 1)")
        print("-" * 40)
        
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json"
        }
        
        # Payload mínimo possível
        minimal_payload = {
            "url": f"https://test-minimal-{datetime.now().timestamp()}.com"
        }
        
        print(f"   Payload mínimo: {json.dumps(minimal_payload, indent=2)}")
        
        try:
            response = requests.post(self.news_log_url, json=minimal_payload, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("   ✅ Inserção mínima bem-sucedida!")
                return True, None
            else:
                error_text = response.text
                print(f"   ❌ ERRO 1 IDENTIFICADO: {error_text}")
                return False, error_text
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            return False, str(e)
    
    def test_full_insert(self, table_structure):
        """Testa inserção completa para identificar ERRO 2"""
        
        print("\n📋 TESTE 4: INSERÇÃO COMPLETA (ERRO 2)")
        print("-" * 40)
        
        headers = {
            "apikey": self.service_key,
            "Authorization": f"Bearer {self.service_key}",
            "Content-Type": "application/json"
        }
        
        # Payload completo baseado na estrutura
        full_payload = {
            "url": f"https://test-full-{datetime.now().timestamp()}.com",
            "titulo": "Notícia de Teste Completa",
            "fonte": "Teste Automático",
            "categoria": "teste",
            "status": "publicada",
            "agente_origem": "error_tester"
        }
        
        # Adicionar campos extras se existirem na tabela
        if 'created_at' in table_structure:
            full_payload['created_at'] = datetime.now().isoformat()
        if 'id' in table_structure:
            pass  # ID é auto-incremento
        
        print(f"   Payload completo: {json.dumps(full_payload, indent=2)}")
        
        try:
            response = requests.post(self.news_log_url, json=full_payload, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print("   ✅ Inserção completa bem-sucedida!")
                return True, None
            else:
                error_text = response.text
                print(f"   ❌ ERRO 2 IDENTIFICADO: {error_text}")
                return False, error_text
                
        except Exception as e:
            print(f"   ❌ Exceção: {e}")
            return False, str(e)
    
    def generate_solutions(self, error1, error2, table_structure):
        """Gera soluções para os erros encontrados"""
        
        print("\n🔧 SOLUÇÕES RECOMENDADAS")
        print("=" * 50)
        
        solutions = []
        
        # Análise do ERRO 1
        if error1:
            print(f"\n🔴 ERRO 1 (Inserção Mínima): {error1}")
            
            if "row-level security policy" in error1.lower():
                print("   💡 SOLUÇÃO 1: Usar SERVICE_ROLE_KEY (já está usando)")
                print("   💡 SOLUÇÃO 2: Verificar políticas RLS no Supabase")
                solutions.append("Verificar políticas RLS na tabela news_log")
            
            if "column" in error1.lower() and "does not exist" in error1.lower():
                print("   💡 SOLUÇÃO: Remover campo que não existe")
                solutions.append("Ajustar payload para campos existentes")
            
            if "null value" in error1.lower() and "not-null" in error1.lower():
                print("   💡 SOLUÇÃO: Adicionar valores obrigatórios")
                solutions.append("Preencher campos obrigatórios")
        
        # Análise do ERRO 2
        if error2:
            print(f"\n🔴 ERRO 2 (Inserção Completa): {error2}")
            
            if "duplicate key" in error2.lower():
                print("   💡 SOLUÇÃO: Verificar constraint unique")
                solutions.append("Ajustar URL para ser único")
        
        # Recomendações gerais
        print(f"\n📋 ESTRUTURA DA TABELA: {len(table_structure)} campos")
        print("   Campos:", ", ".join(table_structure))
        
        print(f"\n🎯 PLANO DE AÇÃO:")
        print("   1. Aplicar soluções identificadas")
        print("   2. Corrigir payload no NewsUtils")
        print("   3. Testar novamente com agente completo")
        
        return solutions
    
    def run_full_test(self):
        """Executa todos os testes e gera relatório"""
        
        print("🧪 INICIANDO DIAGNÓSTICO COMPLETO DO SUPABASE")
        print("=" * 60)
        
        # Teste 1: Conexão
        connection_ok, total_records = self.test_connection()
        if not connection_ok:
            print("\n❌ FALHA CRÍTICA: Sem conexão com Supabase!")
            return
        
        # Teste 2: Estrutura
        table_structure = self.get_table_structure()
        
        # Teste 3: Inserção mínima
        minimal_ok, error1 = self.test_minimal_insert()
        
        # Teste 4: Inserção completa
        full_ok, error2 = self.test_full_insert(table_structure)
        
        # Gerar soluções
        solutions = self.generate_solutions(error1, error2, table_structure)
        
        # Resumo final
        print(f"\n📊 RESUMO FINAL:")
        print(f"   Conexão: {'✅' if connection_ok else '❌'}")
        print(f"   Registros atuais: {total_records}")
        print(f"   Inserção mínima: {'✅' if minimal_ok else '❌'}")
        print(f"   Inserção completa: {'✅' if full_ok else '❌'}")
        print(f"   Soluções geradas: {len(solutions)}")
        
        return {
            "connection_ok": connection_ok,
            "total_records": total_records,
            "table_structure": table_structure,
            "minimal_ok": minimal_ok,
            "full_ok": full_ok,
            "error1": error1,
            "error2": error2,
            "solutions": solutions
        }

if __name__ == "__main__":
    tester = SupabaseErrorTester()
    results = tester.run_full_test()
    
    print(f"\n🎯 PRÓXIMO PASSO:")
    if results["minimal_ok"] and results["full_ok"]:
        print("   ✅ TUDO FUNCIONANDO! Testar com agente completo:")
        print("   python test_collect_news.py")
    else:
        print("   🔧 APLICAR SOLUÇÕES IDENTIFICADAS")
        print("   Depois testar novamente com: python test_collect_news.py")
