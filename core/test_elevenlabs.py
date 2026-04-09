import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')

api_key = os.environ.get('ELEVENLABS_API_KEY')
print('Testando conexão com ElevenLabs...')
print(f'API Key: {api_key[:10]}...' if api_key else 'API Key NOT FOUND')

headers = {
    'xi-api-key': api_key,
    'Accept': 'application/json'
}

try:
    response = requests.get('https://api.elevenlabs.io/v1/voices', headers=headers, timeout=10)
    print(f'Status Code: {response.status_code}')
    if response.status_code == 200:
        print('Conexão bem-sucedida!')
        data = response.json()
        print(f'Vozes encontradas: {len(data.get("voices", []))}')
    else:
        print(f'Erro: {response.status_code}')
        print(f'Resposta: {response.text[:200]}')
except Exception as e:
    print(f'Erro de conexão: {e}')
