"""
Teste interativo do LMNT Voice Cloner Final
"""

import os
from core.lmnt_voice_cloner_final import LMNTVoiceClonerFinal

def menu_interativo():
    """Menu interativo para testar funcionalidades"""
    
    print("=== Teste Interativo LMNT Voice Cloner ===")
    print("API Key configurada:", os.environ.get("LMNT_API_KEY", "N/A")[:10] + "...")
    
    try:
        cloner = LMNTVoiceClonerFinal()
        
        while True:
            print("\n" + "="*50)
            print("MENU DE TESTES:")
            print("1. Ver informações da conta")
            print("2. Listar vozes disponíveis")
            print("3. Gerar áudio com voz existente")
            print("4. Obter informações de voz específica")
            print("5. Sair")
            
            opcao = input("\nEscolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                print("\n--- INFORMAÇÕES DA CONTA ---")
                account = cloner.get_account_info()
                plano = account.get('plan', {})
                print(f"Plano: {plano.get('type', 'N/A')}")
                print(f"Limite de caracteres: {plano.get('character_limit', 'N/A')}")
                print(f"Uso comercial: {plano.get('commercial_use_allowed', 'N/A')}")
                
            elif opcao == "2":
                print("\n--- VOZES DISPONÍVEIS ---")
                voices = cloner.list_voices()
                summary = cloner.get_available_voices_summary()
                
                print(f"Total de vozes: {len(voices['voices'])}")
                print("\nPrimeiras 10 vozes:")
                for i, voice in enumerate(summary, 1):
                    print(f"{i:2d}. {voice['name']:<10} ({voice['id']:<8}) - {voice['gender']} - {voice['description'][:30]}...")
                
            elif opcao == "3":
                print("\n--- GERAR ÁUDIO ---")
                voices = cloner.get_available_voices_summary()
                
                print("Vozes disponíveis:")
                for i, voice in enumerate(voices[:10], 1):
                    print(f"{i}. {voice['name']} ({voice['id']})")
                
                try:
                    voz_num = int(input(f"Escolha uma voz (1-{min(10, len(voices))}): ")) - 1
                    if 0 <= voz_num < len(voices):
                        voz_escolhida = voices[voz_num]
                        texto = input("Digite o texto para gerar áudio: ").strip()
                        
                        if texto:
                            filename = f"test_{voz_escolhida['id']}_interativo.mp3"
                            cloner.synthesize_to_file(
                                voice_id=voz_escolhida['id'],
                                text=texto,
                                filepath=filename
                            )
                            print(f"Áudio gerado: {filename}")
                        else:
                            print("Texto não pode ser vazio!")
                    else:
                        print("Opção inválida!")
                except ValueError:
                    print("Digite um número válido!")
                
            elif opcao == "4":
                print("\n--- INFORMAÇÕES DE VOZ ESPECÍFICA ---")
                voice_id = input("Digite o ID da voz: ").strip()
                
                if voice_id:
                    try:
                        voice_info = cloner.get_voice(voice_id)
                        print(f"\nInformações da voz '{voice_id}':")
                        print(f"Nome: {voice_info.get('name', 'N/A')}")
                        print(f"Gênero: {voice_info.get('gender', 'N/A')}")
                        print(f"Descrição: {voice_info.get('description', 'N/A')}")
                        print(f"Tipo: {voice_info.get('type', 'N/A')}")
                        print(f"Estado: {voice_info.get('state', 'N/A')}")
                    except Exception as e:
                        print(f"Erro ao obter voz: {e}")
                else:
                    print("ID não pode ser vazio!")
                
            elif opcao == "5":
                print("Saindo...")
                break
                
            else:
                print("Opção inválida! Tente novamente.")
                
    except Exception as e:
        print(f"Erro ao inicializar: {e}")

if __name__ == "__main__":
    menu_interativo()
