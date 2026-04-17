"""
Script para configurar variáveis de ambiente do Supabase no Vercel via CLI
"""

import subprocess
import sys

def check_vercel_cli():
    """Verifica se Vercel CLI está instalado"""
    try:
        result = subprocess.run(['vercel', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Vercel CLI instalado: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Vercel CLI não encontrado.")
    print("  Instale com: npm install -g vercel")
    return False

def setup_supabase_env():
    """Configura as variáveis do Supabase no Vercel"""
    
    print("=" * 60)
    print("CONFIGURAÇÃO DE VARIÁVEIS SUPABASE NO VERCEL")
    print("=" * 60)
    
    # Verificar CLI
    if not check_vercel_cli():
        return False
    
    # Credenciais do Supabase
    env_vars = {
        'SUPABASE_URL': 'https://ykswhzqdjoshjoaruhqs.supabase.co',
        'SUPABASE_ANON_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo',
        'SUPABASE_SERVICE_KEY': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8'
    }
    
    print("\nAs seguintes variáveis serão configuradas:")
    for name in env_vars.keys():
        print(f"  - {name}")
    
    print("\nAmbiente: Production, Preview, Development")
    print("\n" + "-" * 60)
    
    # Configurar cada variável
    for name, value in env_vars.items():
        print(f"\nConfigurando {name}...")
        
        # Comando para adicionar variável no Vercel
        cmd = [
            'vercel', 'env', 'add', name,
            'production',  # Também pode ser 'preview' ou 'development'
            '--yes'
        ]
        
        try:
            # Usar stdin para passar o valor
            result = subprocess.run(
                cmd,
                input=value,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"  ✓ {name} configurado com sucesso!")
            else:
                print(f"  ✗ Erro ao configurar {name}:")
                print(f"    {result.stderr}")
                
        except Exception as e:
            print(f"  ✗ Erro: {str(e)}")
    
    print("\n" + "=" * 60)
    print("CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("1. Faça deploy na Vercel:")
    print("   vercel --prod")
    print("\n2. Teste a conexão:")
    print("   python test_supabase_connection.py")
    
    return True

def print_manual_instructions():
    """Mostra instruções manuais"""
    print("\n" + "=" * 60)
    print("INSTRUÇÕES MANUAIS PARA CONFIGURAÇÃO")
    print("=" * 60)
    print("\n1. Acesse: https://vercel.com/dashboard")
    print("2. Selecione o projeto 'locutores-ia'")
    print("3. Clique em 'Settings' → 'Environment Variables'")
    print("4. Adicione as seguintes variáveis:\n")
    
    print("SUPABASE_URL:")
    print("  Value: https://ykswhzqdjoshjoaruhqs.supabase.co")
    print("  Environment: Production, Preview, Development\n")
    
    print("SUPABASE_ANON_KEY:")
    print("  Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo")
    print("  Environment: Production, Preview, Development\n")
    
    print("SUPABASE_SERVICE_KEY (opcional):")
    print("  Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8")
    print("  Environment: Production, Preview, Development\n")
    
    print("5. Clique em 'Save' para cada variável")
    print("6. Aguarde o redeploy automático")

if __name__ == "__main__":
    print("\nEscolha uma opção:")
    print("1. Configurar automaticamente via Vercel CLI")
    print("2. Ver instruções manuais")
    print("3. Sair")
    
    choice = input("\nOpção (1/2/3): ").strip()
    
    if choice == '1':
        setup_supabase_env()
    elif choice == '2':
        print_manual_instructions()
    else:
        print("Saindo...")
        sys.exit(0)
