"""
Teste corrigido para API oficial LMNT

Este arquivo usa a estrutura correta da API oficial baseado na depuração.
"""

import os
from lmnt import Lmnt

# Configurar API Key
os.environ['LMNT_API_KEY'] = "ak_AbZv3CzqvsHjHxRFj4oL9h"


def test_basic_connection():
    """Testa conexão básica com a API LMNT oficial"""
    
    print("=== Testando Conexão com API LMNT Oficial ===")
    
    try:
        # Inicializar cliente
        client = Lmnt()
        print("1. Cliente LMNT inicializado com sucesso")
        
        # Testar obter informações da conta
        print("\n2. Testando informações da conta...")
        account = client.accounts.retrieve()
        
        # Usar model_dump() para obter dados corretos
        account_data = account.model_dump()
        print(f"   Tipo da conta: {type(account)}")
        print(f"   Dados da conta: {list(account_data.keys())}")
        
        # Mostrar informações disponíveis
        for key, value in account_data.items():
            if key in ['email', 'id', 'account_id', 'name', 'credits_remaining', 'plan']:
                print(f"   {key}: {value}")
        
        print("   Conexão bem-sucedida!")
        return True
        
    except Exception as e:
        print(f"   Erro na conexão: {e}")
        return False


def test_voices_list():
    """Testa listagem de vozes com estrutura correta"""
    
    print("\n=== Testando Listagem de Vozes ===")
    
    try:
        client = Lmnt()
        
        # Listar vozes - retorna uma lista diretamente
        voices = client.voices.list()
        print(f"   Tipo de retorno: {type(voices)}")
        print(f"   Total de vozes: {len(voices)}")
        
        # Mostrar algumas vozes
        if voices:
            print("   Primeiras vozes:")
            for i, voice in enumerate(voices[:5]):
                print(f"   {i+1}. {voice.name} ({voice.id}) - {voice.gender} - {voice.description}")
        
        return True, voices
        
    except Exception as e:
        print(f"   Erro na listagem: {e}")
        return False, []


def test_speech_generation(voices):
    """Testa geração de áudio com estrutura correta"""
    
    print("\n=== Testando Geração de Áudio ===")
    
    try:
        client = Lmnt()
        
        # Obter primeira voz disponível
        if not voices:
            print("   Nenhuma voz disponível para teste")
            return False
        
        first_voice = voices[0]
        voice_id = first_voice.id
        print(f"   Usando voz: {first_voice.name} ({voice_id})")
        
        # Gerar áudio
        response = client.speech.generate(
            text="Olá! Este é um teste do SDK oficial LMNT corrigido.",
            voice=voice_id,
            format="mp3"
        )
        
        print(f"   Tipo de resposta: {type(response)}")
        print(f"   Atributos: {dir(response)}")
        
        # Salvar áudio - BinaryAPIResponse tem método diferente
        output_file = "test_speech_fixed.mp3"
        
        # Tentar diferentes métodos para acessar o conteúdo
        if hasattr(response, 'content'):
            with open(output_file, 'wb') as f:
                f.write(response.content)
        elif hasattr(response, 'read'):
            with open(output_file, 'wb') as f:
                f.write(response.read())
        elif hasattr(response, '__iter__'):
            with open(output_file, 'wb') as f:
                for chunk in response:
                    f.write(chunk)
        else:
            print(f"   Estrutura de resposta não identificada: {response}")
            return False
        
        print(f"   Áudio gerado e salvo em: {output_file}")
        return True
        
    except Exception as e:
        print(f"   Erro na geração de áudio: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_detailed_speech(voices):
    """Testa geração detalhada de áudio"""
    
    print("\n=== Testando Geração Detalhada ===")
    
    try:
        client = Lmnt()
        
        if not voices:
            print("   Nenhuma voz disponível")
            return False
        
        voice_id = voices[0].id
        
        # Gerar áudio detalhado
        detailed_response = client.speech.generate_detailed(
            text="Teste de geração detalhada corrigida.",
            voice=voice_id,
            return_detailed=True
        )
        
        print(f"   Tipo da resposta detalhada: {type(detailed_response)}")
        
        # Obter dados usando model_dump()
        response_data = detailed_response.model_dump()
        print(f"   Campos disponíveis: {list(response_data.keys())}")
        
        # Mostrar informações
        for key in ['duration', 'format', 'voice_id', 'text']:
            if key in response_data:
                print(f"   {key}: {response_data[key]}")
        
        # Salvar áudio detalhado
        if 'audio' in response_data:
            detailed_output = "test_detailed_fixed.mp3"
            with open(detailed_output, 'wb') as f:
                f.write(response_data['audio'])
            print(f"   Áudio detalhado salvo em: {detailed_output}")
        
        return True
        
    except Exception as e:
        print(f"   Erro na geração detalhada: {e}")
        return False


def test_voice_management():
    """Testa gerenciamento básico de vozes"""
    
    print("\n=== Testando Informações de Voz ===")
    
    try:
        client = Lmnt()
        
        # Obter primeira voz
        voices = client.voices.list()
        if voices:
            first_voice = voices[0]
            voice_id = first_voice.id
            
            print(f"   Voz selecionada: {first_voice.name} ({voice_id})")
            
            # Obter informações detalhadas da voz
            voice_info = client.voices.retrieve(voice_id)
            voice_data = voice_info.model_dump()
            
            print(f"   Informações detalhadas:")
            for key, value in voice_data.items():
                if key in ['name', 'id', 'gender', 'description', 'type', 'state']:
                    print(f"     {key}: {value}")
            
            return True
        
        print("   Nenhuma voz disponível para teste")
        return False
        
    except Exception as e:
        print(f"   Erro no gerenciamento: {e}")
        return False


def main():
    """Função principal com testes corrigidos"""
    
    print("=== Testes Corrigidos do SDK LMNT Oficial ===")
    print("=" * 60)
    
    results = []
    
    # Testar conexão básica
    connection_ok = test_basic_connection()
    results.append(("Conexão Básica", connection_ok))
    
    if connection_ok:
        # Testar listagem de vozes
        voices_ok, voices = test_voices_list()
        results.append(("Listagem de Vozes", voices_ok))
        
        # Testar geração de áudio
        speech_ok = test_speech_generation(voices)
        results.append(("Geração de Áudio", speech_ok))
        
        # Testar geração detalhada
        detailed_ok = test_detailed_speech(voices)
        results.append(("Geração Detalhada", detailed_ok))
        
        # Testar gerenciamento de vozes
        management_ok = test_voice_management()
        results.append(("Gerenciamento de Vozes", management_ok))
    
    # Resumo final
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES CORRIGIDOS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASSOU" if result else "FALHOU"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("Todos os testes passaram! SDK LMNT Oficial está funcionando perfeitamente.")
    else:
        print("Alguns testes falharam, mas a conexão básica está funcionando.")
    
    print("\nDicas para usar no seu projeto:")
    print("- client.voices.list() retorna lista diretamente (não tem .data)")
    print("- Use .model_dump() para acessar dados dos objetos")
    print("- BinaryAPIResponse precisa ser tratado especificamente para salvar")


if __name__ == "__main__":
    main()
