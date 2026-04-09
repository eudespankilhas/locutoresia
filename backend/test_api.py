import requests
import json

base_url = "http://localhost:5000"

print("=== TESTE COMPLETO DA API ===")

# Testar endpoint principal
print("\n1. Testando endpoint principal...")
try:
    response = requests.get(f"{base_url}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("OK: Página principal carregando")
    else:
        print(f"ERRO: {response.text[:200]}")
except Exception as e:
    print(f"ERRO DE CONEXÃO: {e}")

# Testar endpoint de vozes
print("\n2. Testando /api/voices...")
try:
    response = requests.get(f"{base_url}/api/voices")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        voices = data.get('voices', [])
        print(f"OK: {len(voices)} vozes encontradas")
        for voice in voices[:3]:
            print(f"  - {voice.get('name', 'N/A')} ({voice.get('model', 'N/A')})")
    else:
        print(f"ERRO: {response.text[:200]}")
except Exception as e:
    print(f"ERRO DE CONEXÃO: {e}")

# Testar endpoint de stats
print("\n3. Testando /api/stats...")
try:
    response = requests.get(f"{base_url}/api/stats")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"OK: Stats carregados")
        print(f"  - Vozes: {data.get('voices_count', 0)}")
        print(f"  - Áudios gerados: {data.get('audios_generated', 0)}")
    else:
        print(f"ERRO: {response.text[:200]}")
except Exception as e:
    print(f"ERRO DE CONEXÃO: {e}")

# Testar geração de áudio
print("\n4. Testando /api/generate-audio...")
try:
    test_data = {
        "text": "Olá, este é um teste de geração de áudio.",
        "voice": "Charon",
        "style": "normal",
        "language": "pt-BR"
    }
    response = requests.post(f"{base_url}/api/generate-audio", json=test_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"OK: Áudio gerado com sucesso")
        print(f"  - Filename: {data.get('filename', 'N/A')}")
        print(f"  - Download URL: {data.get('download_url', 'N/A')}")
    else:
        print(f"ERRO: {response.text[:200]}")
except Exception as e:
    print(f"ERRO DE CONEXÃO: {e}")

# Testar listagem de vozes ElevenLabs
print("\n5. Testando /api/list-elevenlabs-voices...")
try:
    response = requests.get(f"{base_url}/api/list-elevenlabs-voices")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        voices = data.get('voices', [])
        print(f"OK: {len(voices)} vozes ElevenLabs encontradas")
        for voice in voices[:3]:
            print(f"  - {voice.get('name', 'N/A')} ({voice.get('provider', 'N/A')})")
    else:
        print(f"ERRO: {response.text[:200]}")
except Exception as e:
    print(f"ERRO DE CONEXÃO: {e}")

print("\n=== FIM DOS TESTES ===")
