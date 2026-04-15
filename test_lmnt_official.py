"""
Teste de integração com API oficial LMNT

Este arquivo testa se a integração com o SDK oficial está funcionando corretamente.
"""

import os
from lmnt import Lmnt


def test_basic_connection():
    """Testa conexão básica com a API LMNT"""
    
    print("🔧 Testando conexão com API LMNT oficial...")
    
    try:
        # Inicializar cliente
        client = Lmnt(api_key=os.environ.get("LMNT_API_KEY"))
        print("✅ Cliente LMNT inicializado com sucesso")
        
        # Testar obter informações da conta
        print("\n📊 Testando informações da conta...")
        account = client.accounts.retrieve()
        print(f"✅ Conectado à conta: {account.email}")
        print(f"   Créditos restantes: {account.credits_remaining}")
        print(f"   Plano: {account.plan}")
        
        # Testar listar vozes
        print("\n🎤 Testando listagem de vozes...")
        voices = client.voices.list()
        print(f"✅ Encontradas {len(voices.data)} vozes disponíveis")
        
        # Mostrar algumas vozes
        if voices.data:
            print("   Vozes disponíveis:")
            for i, voice in enumerate(voices.data[:3]):
                print(f"   {i+1}. {voice.name} ({voice.id}) - {voice.gender or 'N/A'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False


def test_speech_generation():
    """Testa geração de áudio"""
    
    print("\n🎵 Testando geração de áudio...")
    
    try:
        client = Lmnt(api_key=os.environ.get("LMNT_API_KEY"))
        
        # Obter primeira voz disponível
        voices = client.voices.list()
        if not voices.data:
            print("❌ Nenhuma voz disponível para teste")
            return False
        
        voice_id = voices.data[0].id
        print(f"   Usando voz: {voices.data[0].name}")
        
        # Gerar áudio simples
        response = client.speech.generate(
            text="Olá! Este é um teste do SDK oficial LMNT.",
            voice=voice_id,
            format="mp3"
        )
        
        # Salvar áudio
        output_file = "test_speech.mp3"
        with open(output_file, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Áudio gerado e salvo em: {output_file}")
        print(f"   Tamanho do arquivo: {len(response.content)} bytes")
        
        # Testar geração detalhada
        detailed_response = client.speech.generate_detailed(
            text="Teste de geração detalhada com metadados.",
            voice=voice_id,
            return_detailed=True
        )
        
        print(f"✅ Áudio detalhado gerado:")
        print(f"   Duração: {detailed_response.duration} segundos")
        print(f"   Formato: {detailed_response.format}")
        
        # Salvar áudio detalhado
        detailed_output = "test_detailed.mp3"
        with open(detailed_output, 'wb') as f:
            f.write(detailed_response.audio)
        
        print(f"   Salvo em: {detailed_output}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na geração de áudio: {e}")
        return False


def test_voice_management():
    """Testa gerenciamento de vozes (se houver arquivo de áudio)"""
    
    print("\n🎭 Testando gerenciamento de vozes...")
    
    try:
        client = Lmnt(api_key=os.environ.get("LMNT_API_KEY"))
        
        # Listar vozes existentes
        voices_before = client.voices.list()
        print(f"   Vozes antes do teste: {len(voices_before.data)}")
        
        # Verificar se temos um arquivo de áudio para teste
        test_audio_file = "test_voice_sample.wav"
        if not os.path.exists(test_audio_file):
            print(f"⚠️  Arquivo '{test_audio_file}' não encontrado. Pulando teste de criação de voz.")
            print("   Para testar criação de voz, adicione um arquivo WAV com este nome.")
            return True
        
        # Criar nova voz
        with open(test_audio_file, 'rb') as f:
            new_voice = client.voices.create(
                name="Voz de Teste Oficial",
                files={"audio": f},
                description="Voz criada durante teste do SDK oficial",
                enhance=True
            )
        
        print(f"✅ Voz criada: {new_voice.name} ({new_voice.id})")
        
        # Atualizar voz
        updated_voice = client.voices.update(
            new_voice.id,
            description="Voz atualizada durante teste"
        )
        print(f"✅ Voz atualizada: {updated_voice.voice.description}")
        
        # Listar vozes após criação
        voices_after = client.voices.list()
        print(f"   Vozes após criação: {len(voices_after.data)}")
        
        # Excluir voz de teste
        delete_response = client.voices.delete(new_voice.id)
        if delete_response.success:
            print(f"✅ Voz de teste excluída com sucesso")
        
        # Verificar contagem final
        voices_final = client.voices.list()
        print(f"   Vozes finais: {len(voices_final.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no gerenciamento de vozes: {e}")
        return False


def main():
    """Função principal de testes"""
    
    print("🚀 Iniciando testes do SDK LMNT Oficial")
    print("=" * 50)
    
    # Verificar variável de ambiente
    if not os.environ.get("LMNT_API_KEY"):
        print("❌ LMNT_API_KEY não encontrada no ambiente!")
        print("   Configure a variável de ambiente antes de executar os testes.")
        return
    
    print(f"🔑 API Key encontrada: {os.environ.get('LMNT_API_KEY')[:10]}...")
    print()
    
    # Executar testes
    tests = [
        ("Conexão Básica", test_basic_connection),
        ("Geração de Áudio", test_speech_generation),
        ("Gerenciamento de Vozes", test_voice_management),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Falha inesperada no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo dos testes
    print("\n" + "="*60)
    print("📋 RESUMO DOS TESTES")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\n🏆 Resultado: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("🎉 Todos os testes passaram! SDK LMNT Oficial está funcionando perfeitamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    print("\n💡 Dica: Use o arquivo 'lmnt_official_example.py' para ver exemplos completos de uso.")


if __name__ == "__main__":
    main()
