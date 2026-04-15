"""
Exemplo de uso do SDK LMNT

Este arquivo demonstra como usar as diferentes funcionalidades da API LMNT
através do cliente Python que foi implementado.
"""

import os
import base64
from lmnt import LMNTClient, create_client


def main():
    """Função principal com exemplos de uso"""
    
    # Inicializar o cliente (a API key pode ser configurada via variável de ambiente)
    try:
        client = LMNTClient()
        print("Cliente LMNT inicializado com sucesso!")
    except ValueError as e:
        print(f"Erro ao inicializar cliente: {e}")
        print("Configure a variável de ambiente LMNT_API_KEY ou forneça a chave diretamente.")
        return
    
    try:
        # 1. Obter informações da conta
        print("\n=== Informações da Conta ===")
        account_info = client.get_account_info()
        print(f"ID da Conta: {account_info.account_id}")
        print(f"Email: {account_info.email}")
        print(f"Plano: {account_info.plan}")
        print(f"Créditos Restantes: {account_info.credits_remaining}")
        
        # 2. Listar vozes disponíveis
        print("\n=== Vozes Disponíveis ===")
        voices_response = client.list_voices(limit=10)
        print(f"Total de vozes: {len(voices_response.voices)}")
        
        for voice in voices_response.voices[:5]:  # Mostrar apenas as 5 primeiras
            print(f"- {voice.name} ({voice.id}) - {voice.gender or 'N/A'} - {voice.language or 'N/A'}")
        
        # 3. Gerar áudio usando uma voz existente
        if voices_response.voices:
            voice_id = voices_response.voices[0].id
            print(f"\n=== Gerando Áudio com Voz: {voice_id} ===")
            
            # Gerar áudio simples
            response = client.generate_speech(
                text="Olá! Este é um teste de geração de áudio usando a API LMNT.",
                voice=voice_id,
                format="mp3"
            )
            
            # Salvar áudio gerado
            output_file = "generated_speech.mp3"
            response.save_to_file(output_file)
            print(f"Áudio salvo em: {output_file}")
            
            # Gerar áudio com detalhes
            print("\n=== Gerando Áudio Detalhado ===")
            detailed_response = client.generate_detailed_speech(
                text="Este é um teste de geração detalhada de áudio.",
                voice=voice_id,
                speed=1.0,
                return_detailed=True
            )
            
            print(f"Duração: {detailed_response.duration} segundos")
            print(f"Formato: {detailed_response.format}")
            print(f"ID da Voz: {detailed_response.voice_id}")
            
            # Salvar áudio detalhado
            detailed_output = "detailed_speech.mp3"
            detailed_response.save_audio(detailed_output)
            print(f"Áudio detalhado salvo em: {detailed_output}")
        
        # 4. Criar uma voz personalizada (exemplo)
        print("\n=== Criando Voz Personalizada ===")
        
        # Exemplo de como criar uma voz (você precisar fornecer dados de áudio reais)
        # Aqui está um exemplo com dados simulados:
        
        # Ler arquivo de áudio para clonagem
        audio_file_path = "sample_voice.wav"  # Substitua pelo seu arquivo
        
        if os.path.exists(audio_file_path):
            with open(audio_file_path, 'rb') as f:
                audio_data = f.read()
            
            new_voice = client.create_voice(
                name="Minha Voz Personalizada",
                audio_data=audio_data,
                description="Voz criada para testes",
                enhance=True,
                language="pt-BR"
            )
            
            print(f"Voz criada com sucesso!")
            print(f"ID: {new_voice.id}")
            print(f"Nome: {new_voice.name}")
            print(f"Idioma: {new_voice.language}")
            
            # Atualizar informações da voz
            print("\n=== Atualizando Voz ===")
            update_response = client.update_voice(
                new_voice.id,
                description="Voz atualizada com nova descrição",
                is_public=False
            )
            
            print(f"Voz atualizada: {update_response.success}")
            if update_response.message:
                print(f"Mensagem: {update_response.message}")
        else:
            print(f"Arquivo de áudio '{audio_file_path}' não encontrado. Pulando criação de voz.")
        
        # 5. Exemplo de conversão de áudio
        print("\n=== Convertendo Áudio ===")
        
        # Exemplo de conversão (você precisar fornecer dados de áudio reais)
        if os.path.exists("input_audio.wav"):
            with open("input_audio.wav", 'rb') as f:
                input_audio = f.read()
            
            converted_response = client.convert_speech(
                input_format="wav",
                output_format="mp3",
                data=input_audio,
                voice=voice_id if voices_response.voices else None
            )
            
            converted_response.save_to_file("converted_audio.mp3")
            print("Áudio convertido salvo em: converted_audio.mp3")
        else:
            print("Arquivo 'input_audio.wav' não encontrado. Pulando conversão.")
        
        print("\n=== Exemplos concluídos com sucesso! ===")
        
    except Exception as e:
        print(f"Erro durante a execução: {e}")
        import traceback
        traceback.print_exc()


def exemplo_simples():
    """Exemplo mais simples e direto"""
    
    # Usar função de conveniência
    client = create_client()  # Irá buscar LMNT_API_KEY do ambiente
    
    # Gerar áudio rapidamente
    response = client.generate_speech(
        text="Teste rápido de geração de áudio",
        voice="daniel",  # Voz padrão (substitua por uma voz válida)
        format="wav"
    )
    
    response.save_to_file("quick_test.wav")
    print("Áudio gerado com sucesso!")


if __name__ == "__main__":
    print("=== Exemplo de Uso do SDK LMNT ===")
    print("Certifique-se de configurar a variável de ambiente LMNT_API_KEY")
    print()
    
    # Executar exemplo completo
    main()
    
    # Ou executar exemplo simples
    # exemplo_simples()
