#!/usr/bin/env python3
import asyncio
import edge_tts

async def test_edge_tts():
    print("Testando Edge TTS diretamente...")
    
    try:
        # Teste simples com voz em português
        communicate = edge_tts.Communicate("Olá, este é um teste da voz Edge TTS em português.", "pt-BR-AntonioNeural")
        
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        if audio_data:
            filename = "test_edge_tts_output.mp3"
            with open(filename, "wb") as f:
                f.write(audio_data)
            print(f"Áudio Edge TTS gerado com sucesso! Salvo como: {filename}")
            print(f"Tamanho do arquivo: {len(audio_data)} bytes")
            return True
        else:
            print("Erro: Nenhum dado de áudio retornado pelo Edge TTS")
            return False
            
    except Exception as e:
        print(f"Erro ao testar Edge TTS: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_edge_tts())
