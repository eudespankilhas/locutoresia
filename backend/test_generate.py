import requests
import json

def test_generate_audio():
    print("Testando geração de áudio via API...")
    
    url = "http://localhost:5000/api/generate-audio"
    data = {
        "text": "Este é um teste de geração de áudio com voz real.",
        "voice": "Puck",
        "style": "fast",
        "language": "pt-BR"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resultado: {result}")
            
            filename = result.get('filename')
            if filename:
                download_url = f"http://localhost:5000/api/download/{filename}"
                print(f"URL de download: {download_url}")
                
                # Testar download
                download_response = requests.get(download_url)
                print(f"Download Status: {download_response.status_code}")
                print(f"Download Size: {len(download_response.content)} bytes")
                
                if len(download_response.content) > 0:
                    # Salvar para teste
                    with open(f"test_{filename}", "wb") as f:
                        f.write(download_response.content)
                    print(f"Arquivo salvo: test_{filename}")
                    return True
                else:
                    print("ERRO: Download retornou arquivo vazio")
                    return False
            else:
                print("ERRO: Nenhum filename retornado")
                return False
        else:
            print(f"ERRO: {response.text}")
            return False
            
    except Exception as e:
        print(f"ERRO: {e}")
        return False

if __name__ == "__main__":
    success = test_generate_audio()
    if success:
        print("\nSUCESSO: API está funcionando corretamente!")
    else:
        print("\nERRO: Problema na API!")
