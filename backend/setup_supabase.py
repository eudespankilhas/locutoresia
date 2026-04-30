#!/usr/bin/env python3
"""
Script para configurar o Supabase com as tabelas do News Auto Post
Execute este script uma vez para criar todas as tabelas necessárias
"""

import os
import sys
from supabase_config import get_supabase_client, CREATE_TABLES_SQL

def setup_database():
    """Configura o banco de dados Supabase"""
    print("Configurando banco de dados Supabase...")
    
    try:
        # Conectar ao Supabase
        supabase = get_supabase_client()
        print("Conectado ao Supabase com sucesso!")
        
        # Executar SQL para criar tabelas
        print("Criando tabelas...")
        
        # Dividir o SQL em comandos individuais
        sql_commands = CREATE_TABLES_SQL.split(';')
        
        for command in sql_commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    # Tentar executar o comando SQL
                    result = supabase.rpc('exec_sql', {'sql': command}).execute()
                    print(f"Executado: {command[:50]}...")
                except Exception as e:
                    # Se falhar, tentar método alternativo
                    print(f"Aviso: {e}")
                    continue
        
        print("Banco de dados configurado com sucesso!")
        
        # Verificar se as tabelas foram criadas
        print("Verificando tabelas criadas...")
        
        tables_to_check = ['publications', 'logs', 'sources', 'analytics']
        
        for table in tables_to_check:
            try:
                result = supabase.table(table).select('*').limit(1).execute()
                print(f" Tabela '{table}': OK")
            except Exception as e:
                print(f" Tabela '{table}': Erro - {e}")
        
        # Testar inserção de dados
        print("\nTestando inserção de dados...")
        
        test_log = {
            'message': 'Teste de configuração do sistema',
            'type': 'info'
        }
        
        try:
            result = supabase.table('logs').insert(test_log).execute()
            print(" Teste de inserção: OK")
            
            # Remover teste
            supabase.table('logs').delete().eq('message', 'Teste de configuração do sistema').execute()
            print(" Limpeza de teste: OK")
            
        except Exception as e:
            print(f" Teste de inserção: Erro - {e}")
        
        print("\nConfiguração concluída!")
        return True
        
    except Exception as e:
        print(f"Erro na configuração: {e}")
        return False

def check_environment():
    """Verifica se as variáveis de ambiente estão configuradas"""
    print("Verificando configuração de ambiente...")
    
    required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f" {var}: Configurada")
        else:
            print(f" {var}: NÃO CONFIGURADA")
            print(f"  Defina a variável: export {var}='seu_valor'")
            return False
    
    return True

if __name__ == "__main__":
    print("=== SETUP DO SUPABASE - NEWS AUTO POST ===\n")
    
    # Verificar ambiente
    if not check_environment():
        print("\nConfigure as variáveis de ambiente antes de continuar.")
        sys.exit(1)
    
    # Configurar banco
    if setup_database():
        print("\nSetup concluído com sucesso!")
        print("O sistema agora usará o Supabase para persistência de dados.")
    else:
        print("\nO setup falhou. Verifique os logs acima.")
        sys.exit(1)
