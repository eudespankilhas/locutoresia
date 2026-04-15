"""
Exemplo de uso do SDK LMNT OFICIAL

Este arquivo demonstra como usar o SDK oficial do LMNT que foi instalado via pip.
A implementação oficial é mais robusta, completa e mantida pelo time LMNT.
"""

import os
from lmnt import Lmnt, AsyncLmnt


def main_sync():
    """Exemplo síncrono usando API oficial LMNT"""
    
    # Inicializar cliente síncrono
    client = Lmnt(
        api_key=os.environ.get("LMNT_API_KEY")  # Busca automaticamente da variável de ambiente
    )
    
    try:
        # 1. Obter informações da conta
        print("=== Informações da Conta ===")
        account = client.accounts.retrieve()
        print(f"Conta ID: {account.id}")
        print(f"Email: {account.email}")
        print(f"Créditos: {account.credits_remaining}")
        
        # 2. Listar vozes disponíveis
        print("\n=== Vozes Disponíveis ===")
        voices = client.voices.list()
        print(f"Total de vozes: {len(voices.data)}")
        
        for voice in voices.data[:5]:  # Mostrar primeiras 5
            print(f"- {voice.name} ({voice.id}) - {voice.gender or 'N/A'}")
        
        # 3. Gerar áudio básico
        if voices.data:
            voice_id = voices.data[0].id
            print(f"\n=== Gerando Áudio com Voz: {voice_id} ===")
            
            response = client.speech.generate(
                text="Olá! Este é um teste com o SDK oficial do LMNT.",
                voice=voice_id,
                format="mp3"
            )
            
            # Salvar áudio
            output_file = "official_speech.mp3"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"Áudio salvo em: {output_file}")
            
            # 4. Gerar áudio detalhado
            print("\n=== Gerando Áudio Detalhado ===")
            detailed_response = client.speech.generate_detailed(
                text="Teste de geração detalhada com metadados.",
                voice=voice_id,
                return_detailed=True
            )
            
            print(f"Duração: {detailed_response.duration} segundos")
            print(f"Formato: {detailed_response.format}")
            
            # Salvar áudio detalhado
            detailed_output = "official_detailed.mp3"
            with open(detailed_output, 'wb') as f:
                f.write(detailed_response.audio)
            print(f"Áudio detalhado salvo em: {detailed_output}")
        
        print("\n=== Exemplos síncronos concluídos! ===")
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()


async def main_async():
    """Exemplo assíncrono usando API oficial LMNT"""
    
    # Inicializar cliente assíncrono
    client = AsyncLmnt(
        api_key=os.environ.get("LMNT_API_KEY")
    )
    
    try:
        # Listar vozes de forma assíncrona
        print("\n=== Listando Vozes (Async) ===")
        voices = await client.voices.list()
        print(f"Total de vozes (async): {len(voices.data)}")
        
        # Gerar áudio de forma assíncrona
        if voices.data:
            voice_id = voices.data[0].id
            response = await client.speech.generate(
                text="Áudio gerado assincronamente!",
                voice=voice_id,
                format="wav"
            )
            
            # Salvar áudio
            with open("async_speech.wav", 'wb') as f:
                f.write(response.content)
            print("Áudio assíncrono salvo em: async_speech.wav")
        
        print("=== Exemplos assíncronos concluídos! ===")
        
    except Exception as e:
        print(f"Erro assíncrono: {e}")
        import traceback
        traceback.print_exc()


def streaming_example():
    """Exemplo de streaming de áudio"""
    
    client = Lmnt(api_key=os.environ.get("LMNT_API_KEY"))
    
    try:
        print("\n=== Exemplo de Streaming ===")
        
        # Usar streaming response para áudio em tempo real
        with client.speech.generate(
            text="Este áudio está sendo gerado em streaming para melhor performance.",
            voice="daniel",  # Voz padrão (substitua se necessário)
            format="mp3"
        ) as response:
            # Processar streaming
            with open("streamed_audio.mp3", 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        
        print("Áudio em streaming salvo em: streamed_audio.mp3")
        
    except Exception as e:
        print(f"Erro no streaming: {e}")


def voice_management_example():
    """Exemplo de gerenciamento de vozes"""
    
    client = Lmnt(api_key=os.environ.get("LMNT_API_KEY"))
    
    try:
        print("\n=== Gerenciamento de Vozes ===")
        
        # Criar uma nova voz (se tiver arquivo de áudio)
        audio_file = "sample_voice.wav"  # Substitua por seu arquivo
        
        if os.path.exists(audio_file):
            print(f"Criando voz a partir de: {audio_file}")
            
            with open(audio_file, 'rb') as f:
                new_voice = client.voices.create(
                    name="Voz Personalizada Oficial",
                    files={"audio": f},
                    description="Voz criada com SDK oficial",
                    enhance=True
                )
            
            print(f"Voz criada: {new_voice.name} ({new_voice.id})")
            
            # Atualizar informações da voz
            updated_voice = client.voices.update(
                new_voice.id,
                description="Voz atualizada via SDK oficial"
            )
            print(f"Voz atualizada: {updated_voice.description}")
            
            # Listar vozes personalizadas
            custom_voices = client.voices.list()
            print(f"Total de vozes após criação: {len(custom_voices.data)}")
            
        else:
            print(f"Arquivo '{audio_file}' não encontrado. Pulando criação de voz.")
        
    except Exception as e:
        print(f"Erro no gerenciamento de vozes: {e}")


if __name__ == "__main__":
    print("=== Exemplos do SDK LMNT OFICIAL ===")
    print("Certifique-se de configurar LMNT_API_KEY no ambiente")
    print()
    
    # Executar exemplos
    main_sync()
    
    # Exemplo assíncrono
    import asyncio
    asyncio.run(main_async())
    
    # Exemplo de streaming
    streaming_example()
    
    # Exemplo de gerenciamento de vozes
    voice_management_example()
