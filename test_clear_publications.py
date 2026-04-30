"""
Teste para limpar publicações
Testa o endpoint DELETE /api/publications
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_clear_publications():
    """Testa endpoint DELETE /api/publications"""
    print("=" * 60)
    print("TESTE: DELETE /api/publications")
    print("=" * 60)
    
    try:
        # Primeiro, listar publicações antes
        print("\n1. Listando publicações antes...")
        response = requests.get(f"{BASE_URL}/api/publications", timeout=10)
        data = response.json()
        print(f"   Total antes: {data.get('total', 0)}")
        
        # Confirmar ação
        confirm = input("\n⚠️ Tem certeza que deseja limpar TODAS as publicações? (s/n): ")
        if confirm.lower() != 's':
            print("❌ Cancelado pelo usuário")
            return
        
        # Limpar publicações
        print("\n2. Limpando publicações...")
        response = requests.delete(
            f"{BASE_URL}/api/publications",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code in (200, 204):
            data = response.json()
            if data.get('success'):
                print(f"\n✅ Publicações limpas com sucesso")
            else:
                print(f"\n❌ Erro: {data.get('error')}")
        else:
            print(f"\n❌ Erro ao limpar publicações")
        
        # Listar publicações depois
        print("\n3. Listando publicações depois...")
        response = requests.get(f"{BASE_URL}/api/publications", timeout=10)
        data = response.json()
        print(f"   Total depois: {data.get('total', 0)}")
        
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    print("🧪 Teste de Limpar Publicações")
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    test_clear_publications()
    
    print("\n" + "=" * 60)
    print("✅ Teste concluído")
    print("=" * 60)
