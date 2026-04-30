"""
Teste para VoxCraft Callback
Testa o fluxo completo: receive -> complete
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_voxcraft_receive():
    """Testa endpoint /api/voxcraft/receive"""
    print("=" * 60)
    print("TESTE 1: /api/voxcraft/receive")
    print("=" * 60)
    
    payload = {
        "text": "Texto de teste",
        "post_id": "test-post-123",
        "title": "Notícia Teste",
        "category": "tech",
        "return_url": "http://localhost:3000/callback"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voxcraft/receive",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            session_id = data.get('session_id')
            print(f"\n✅ Session ID criado: {session_id}")
            return session_id
        else:
            print(f"\n❌ Erro ao criar sessão")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

def test_voxcraft_complete(session_id):
    """Testa endpoint /api/voxcraft/complete"""
    print("\n" + "=" * 60)
    print("TESTE 2: /api/voxcraft/complete")
    print("=" * 60)
    
    if not session_id:
        print("❌ Session ID não fornecido")
        return
    
    payload = {
        "session_id": session_id,
        "audio_filename": "locution_test.wav"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/voxcraft/complete",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print(f"\n✅ Callback completado com sucesso")
            print(f"   → Session ID: {session_id}")
            print(f"   → Audio Filename: locution_test.wav")
        else:
            print(f"\n❌ Erro no callback")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

def test_voxcraft_metadata(session_id):
    """Testa endpoint /api/voxcraft/metadata"""
    print("\n" + "=" * 60)
    print("TESTE 3: /api/voxcraft/metadata")
    print("=" * 60)
    
    if not session_id:
        print("❌ Session ID não fornecido")
        return
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/voxcraft/metadata/{session_id}",
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Metadados da sessão:")
            print(f"   → Status: {data.get('status')}")
            print(f"   → Audio Filename: {data.get('audio_filename')}")
            print(f"   → Post ID: {data.get('post_id')}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    print("🧪 Iniciando testes VoxCraft Callback")
    print(f"🌐 Base URL: {BASE_URL}")
    print()
    
    # Teste 1: Criar sessão
    session_id = test_voxcraft_receive()
    
    if session_id:
        # Teste 2: Completar callback
        test_voxcraft_complete(session_id)
        
        # Teste 3: Verificar metadados
        test_voxcraft_metadata(session_id)
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos")
    print("=" * 60)
