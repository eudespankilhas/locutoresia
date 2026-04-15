#!/usr/bin/env python3
import os
import sys

# Adicionar o diretório core ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def test_pyttsx3():
    print("Testando pyttsx3 - sistema TTS offline com múltiplas vozes...")
    
    try:
        import pyttsx3
        
        # Inicializar o engine
        engine = pyttsx3.init()
        
        # Listar todas as vozes disponíveis
        voices = engine.getProperty('voices')
        
        print(f"Vozes disponíveis: {len(voices)}")
        for i, voice in enumerate(voices):
            print(f"  {i}: {voice.name} - {voice.languages[0] if voice.languages else 'Unknown'} - {'Male' if voice.gender == 1 else 'Female' if voice.gender == 2 else 'Unknown'}")
        
        # Testar diferentes vozes
        test_voices = []
        
        # Encontrar vozes masculinas e femininas em português
        for voice in voices:
            if any('pt' in lang.lower() or 'brazil' in lang.lower() for lang in voice.languages):
                test_voices.append(voice)
                if len(test_voices) >= 4:  # Limitar a 4 vozes para teste
                    break
        
        if not test_voices:
            # Se não encontrar vozes em português, usar as primeiras disponíveis
            test_voices = voices[:4]
        
        text = "Este é um teste de voz diferente"
        
        print(f"\nTestando com: '{text}'")
        print("=" * 50)
        
        for i, voice in enumerate(test_voices):
            print(f"\n--- Voz {i+1}: {voice.name} ---")
            
            try:
                # Configurar a voz
                engine.setProperty('voice', voice.id)
                
                # Salvar em arquivo
                filename = f"test_pyttsx3_voz_{i+1}.mp3"
                engine.save_to_file(text, filename)
                engine.runAndWait()
                
                # Verificar o arquivo
                if os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    print(f"  Arquivo: {filename}")
                    print(f"  Tamanho: {file_size} bytes")
                    print(f"  Gênero: {'Male' if voice.gender == 1 else 'Female' if voice.gender == 2 else 'Unknown'}")
                else:
                    print(f"  ERRO: Arquivo não foi criado")
                    
            except Exception as e:
                print(f"  ERRO: {e}")
        
        print("\n" + "=" * 50)
        print("Teste concluído! Verifique os arquivos para ouvir as diferenças.")
        return True
        
    except ImportError:
        print("pyttsx3 não está instalado. Instalando...")
        os.system("pip install pyttsx3")
        return test_pyttsx3()
    except Exception as e:
        print(f"Erro ao testar pyttsx3: {e}")
        return False

if __name__ == "__main__":
    test_pyttsx3()
