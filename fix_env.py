"""
Script para verificar e corrigir o arquivo .env
"""
import os

# Credenciais corretas
ENV_CONTENT = """FLASK_DEBUG=True
FLASK_ENV=development
GEMINI_API_KEY=AIzaSyA9TQ1ZQEmJlhW7ggQczAhbglNvPdF6Sus
SUPABASE_URL=https://ykswhzqdjoshjoaruhqs.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8
"""

# Verificar se .env existe e ler
env_path = '.env'
if os.path.exists(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            current_content = f.read()
        print("Arquivo .env encontrado.")
        print(f"Tamanho: {len(current_content)} caracteres")
        print(f"Linhas: {len(current_content.splitlines())}")
        
        # Verificar se SUPABASE_SERVICE_KEY está presente
        if 'SUPABASE_SERVICE_KEY' in current_content:
            print("\nSUPABASE_SERVICE_KEY encontrado no arquivo.")
        else:
            print("\n✗ SUPABASE_SERVICE_KEY NAO encontrado!")
            
    except Exception as e:
        print(f"Erro ao ler .env: {e}")
        current_content = ""
else:
    print("Arquivo .env NAO existe!")
    current_content = ""

# Perguntar se quer recriar
print("\n" + "="*50)
print("Deseja recriar o arquivo .env com as credenciais corretas?")
print("Isso vai sobrescrever o arquivo atual.")
print("="*50)

# Sempre recriar para garantir
print("\nRecriando .env...")
try:
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(ENV_CONTENT)
    print("✓ Arquivo .env recriado com sucesso!")
    print("\nConteudo:")
    for line in ENV_CONTENT.strip().split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            masked = value[:20] + "..." if len(value) > 20 else value
            print(f"  {key}={masked}")
except Exception as e:
    print(f"✗ Erro ao criar .env: {e}")
