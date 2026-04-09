import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')

api_key = os.environ.get('ELEVENLABS_API_KEY')
headers = {
    'xi-api-key': api_key,
    'Accept': 'application/json'
}

# Voice IDs fornecidos pelo usuário
voice_ids = [
    'PIGsltMj3gFMR34aFDI3',
    'UgBBYS2sOqTuMpoF3BR0', 
    'ljX1ZrXuDIIRVcmiVSyR'
]

print('Testando os Voice IDs fornecidos...')

for voice_id in voice_ids:
    print(f'\nTestando voice_id: {voice_id}')
    
    # Verificar se a voz existe
    try:
        response = requests.get(f'https://api.elevenlabs.io/v1/voices/{voice_id}', headers=headers, timeout=10)
        if response.status_code == 200:
            voice_data = response.json()
            print(f'  OK: {voice_data.get("name", "Nome não encontrado")}')
            print(f'  Descrição: {voice_data.get("description", "Sem descrição")}')
        else:
            print(f'  ERRO: {response.status_code} - {response.text[:100]}')
    except Exception as e:
        print(f'  ERRO DE CONEXÃO: {e}')

# Listar todas as vozes disponíveis para comparação
print('\n\n=== VOZES DISPONÍVEIS NA SUA CONTA ===')
try:
    response = requests.get('https://api.elevenlabs.io/v1/voices', headers=headers, timeout=10)
    if response.status_code == 200:
        voices_data = response.json()
        voices = voices_data.get('voices', [])
        for voice in voices[:10]:  # Mostrar apenas as 10 primeiras
            print(f'ID: {voice.get("voice_id", "N/A")} - Nome: {voice.get("name", "N/A")}')
        if len(voices) > 10:
            print(f'... e mais {len(voices) - 10} vozes')
    else:
        print(f'ERRO ao listar vozes: {response.status_code}')
except Exception as e:
    print(f'ERRO: {e}')
