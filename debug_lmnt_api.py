"""
Script para depurar e entender a estrutura da API LMNT oficial
"""

import os
from lmnt import Lmnt

# Configurar API Key
os.environ['LMNT_API_KEY'] = "ak_AbZv3CzqvsHjHxRFj4oL9h"

def debug_api_structure():
    """Depura a estrutura da API para entender os atributos corretos"""
    
    print("=== Depurando Estrutura da API LMNT ===")
    
    try:
        client = Lmnt()
        print("1. Cliente inicializado com sucesso")
        
        # Testar informações da conta
        print("\n2. Testando informações da conta...")
        account = client.accounts.retrieve()
        print(f"   Tipo: {type(account)}")
        print(f"   Atributos disponíveis: {dir(account)}")
        
        # Tentar acessar atributos comuns
        for attr in ['email', 'id', 'account_id', 'name', 'credits_remaining']:
            try:
                value = getattr(account, attr, 'N/A')
                print(f"   {attr}: {value}")
            except Exception as e:
                print(f"   {attr}: Erro - {e}")
        
        # Testar listagem de vozes
        print("\n3. Testando listagem de vozes...")
        voices = client.voices.list()
        print(f"   Tipo: {type(voices)}")
        print(f"   Atributos disponíveis: {dir(voices)}")
        
        # Verificar se tem 'data' ou outro atributo
        if hasattr(voices, 'data'):
            print(f"   voices.data: {len(voices.data)} itens")
        elif hasattr(voices, '__iter__'):
            voices_list = list(voices)
            print(f"   list(voices): {len(voices_list)} itens")
        else:
            print(f"   Estrutura não identificada")
            print(f"   Conteúdo: {voices}")
        
        # Testar geração de áudio se houver vozes
        print("\n4. Testando geração de áudio...")
        
        # Tentar obter primeira voz
        voices_response = client.voices.list()
        first_voice = None
        
        if hasattr(voices_response, 'data') and voices_response.data:
            first_voice = voices_response.data[0]
        elif hasattr(voices_response, '__iter__'):
            voices_list = list(voices_response)
            if voices_list:
                first_voice = voices_list[0]
        
        if first_voice:
            print(f"   Primeira voz: {first_voice}")
            print(f"   Tipo: {type(first_voice)}")
            print(f"   Atributos: {dir(first_voice)}")
            
            # Tentar obter ID
            voice_id = getattr(first_voice, 'id', None)
            if voice_id:
                print(f"   Voice ID: {voice_id}")
                
                # Testar geração
                try:
                    response = client.speech.generate(
                        text="Teste de áudio",
                        voice=voice_id,
                        format="mp3"
                    )
                    print(f"   Áudio gerado: {len(response.content)} bytes")
                except Exception as e:
                    print(f"   Erro na geração: {e}")
            else:
                print("   Não foi possível obter ID da voz")
        else:
            print("   Nenhuma voz encontrada para teste")
            
    except Exception as e:
        print(f"Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_api_structure()
