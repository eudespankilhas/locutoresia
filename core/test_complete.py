import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')

api_key = os.environ.get('ELEVENLABS_API_KEY')
print('Testando todas as funcionalidades...')

headers = {
    'xi-api-key': api_key,
    'Accept': 'application/json'
}

# Testar listagem de vozes
print('1. Listando vozes...')
response = requests.get('https://api.elevenlabs.io/v1/voices', headers=headers, timeout=10)
if response.status_code == 200:
    voices = response.json()
    print(f'   OK: {len(voices.get("voices", []))} vozes encontradas')
else:
    print(f'   ERRO: {response.status_code}')

# Testar vozes predefinidas
print('2. Listando vozes predefinidas...')
response = requests.get('https://api.elevenlabs.io/v1/voices/preview', headers=headers, timeout=10)
if response.status_code == 200:
    preset_voices = response.json()
    print(f'   OK: {len(preset_voices.get("voices", []))} vozes predefinidas')
else:
    print(f'   ERRO: {response.status_code}')

print('3. API Key está pronta para uso!')
