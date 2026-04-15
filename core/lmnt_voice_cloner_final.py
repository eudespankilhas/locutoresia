import os
import base64
from typing import Optional, Dict, Any, List
import io
from dotenv import load_dotenv
from lmnt import Lmnt

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class LMNTVoiceClonerFinal:
    """
    Versão FINAL corrigida do clonador de vozes LMNT usando API oficial
    
    Esta versão usa a estrutura correta da API oficial LMNT baseado nos testes.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa o clonador de vozes LMNT
        
        Args:
            api_key: Chave da API LMNT. Se não fornecida, busca do ambiente
        """
        self.api_key = api_key or os.environ.get("LMNT_API_KEY")
        
        if not self.api_key:
            raise ValueError("LMNT_API_KEY não configurada. Defina a variável de ambiente ou forneça a chave.")
        
        # Inicializar cliente oficial LMNT
        self.client = Lmnt(api_key=self.api_key)
    
    def clone_voice(self, name: str, audio_data: bytes, description: str = "", enhance: bool = True) -> Dict[str, Any]:
        """
        Cria um clone de voz a partir de dados de áudio usando API oficial
        
        Args:
            name: Nome da voz a ser criada
            audio_data: Dados binários do áudio (bytes)
            description: Descrição opcional da voz
            enhance: Se deve usar enhancement de áudio
            
        Returns:
            Dicionário com informações da voz criada
        """
        try:
            # Criar arquivo temporário em memória para upload
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            # Usar API oficial para criar voz
            voice = self.client.voices.create(
                name=name,
                files={"audio": audio_file},
                description=description,
                enhance=enhance
            )
            
            # Converter para dicionário usando model_dump()
            result = voice.model_dump()
            
            print(f"Voz clonada com sucesso: {voice.id}")
            return result
            
        except Exception as e:
            print(f"Erro ao clonar voz: {e}")
            raise
    
    def list_voices(self) -> Dict[str, Any]:
        """Lista todas as vozes disponíveis na conta LMNT usando API oficial"""
        try:
            # API oficial retorna lista diretamente
            voices_list = self.client.voices.list()
            
            # Converter cada voz para dicionário
            voices_dict_list = []
            for voice in voices_list:
                voice_dict = voice.model_dump()
                voices_dict_list.append(voice_dict)
            
            return {
                'voices': voices_dict_list,
                'total_count': len(voices_dict_list)
            }
            
        except Exception as e:
            print(f"Erro ao listar vozes: {e}")
            raise
    
    def get_voice(self, voice_id: str) -> Dict[str, Any]:
        """Obtém informações de uma voz específica usando API oficial"""
        try:
            voice = self.client.voices.retrieve(voice_id)
            
            # Usar model_dump() para converter para dicionário
            return voice.model_dump()
            
        except Exception as e:
            print(f"Erro ao obter voz: {e}")
            raise
    
    def synthesize_with_cloned_voice(self, voice_id: str, text: str, format: str = "mp3") -> bytes:
        """
        Gera áudio usando uma voz clonada com API oficial
        
        Args:
            voice_id: ID da voz clonada
            text: Texto para sintetizar
            format: Formato do áudio (mp3, wav, etc.)
            
        Returns:
            Dados binários do áudio gerado
        """
        try:
            response = self.client.speech.generate(
                text=text,
                voice=voice_id,
                format=format
            )
            
            # BinaryAPIResponse tem método read()
            return response.read()
            
        except Exception as e:
            print(f"Erro na síntese: {e}")
            raise
    
    def synthesize_to_file(self, voice_id: str, text: str, filepath: str, format: str = "mp3") -> str:
        """
        Gera áudio e salva diretamente em arquivo
        
        Args:
            voice_id: ID da voz clonada
            text: Texto para sintetizar
            filepath: Caminho do arquivo de saída
            format: Formato do áudio
            
        Returns:
            Caminho do arquivo salvo
        """
        try:
            response = self.client.speech.generate(
                text=text,
                voice=voice_id,
                format=format
            )
            
            # Usar método write_to_file do BinaryAPIResponse
            response.write_to_file(filepath)
            
            print(f"Áudio salvo em: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Erro na síntese para arquivo: {e}")
            raise
    
    def synthesize_detailed(self, voice_id: str, text: str, format: str = "mp3") -> Dict[str, Any]:
        """
        Gera áudio com detalhes adicionais usando API oficial
        
        Args:
            voice_id: ID da voz clonada
            text: Texto para sintetizar
            format: Formato do áudio
            
        Returns:
            Dicionário com áudio e metadados
        """
        try:
            # API oficial não tem parâmetro return_detailed
            response = self.client.speech.generate_detailed(
                text=text,
                voice=voice_id,
                format=format
            )
            
            # Usar model_dump() para obter dados
            return response.model_dump()
            
        except Exception as e:
            print(f"Erro na síntese detalhada: {e}")
            raise
    
    def update_voice(self, voice_id: str, **kwargs) -> Dict[str, Any]:
        """
        Atualiza informações de uma voz usando API oficial
        
        Args:
            voice_id: ID da voz
            **kwargs: Parâmetros para atualizar (name, description, etc.)
            
        Returns:
            Dicionário com resultado da atualização
        """
        try:
            updated_voice = self.client.voices.update(voice_id, **kwargs)
            
            return updated_voice.model_dump()
            
        except Exception as e:
            print(f"Erro ao atualizar voz: {e}")
            raise
    
    def delete_voice(self, voice_id: str) -> Dict[str, Any]:
        """
        Exclui uma voz usando API oficial
        
        Args:
            voice_id: ID da voz a ser excluída
            
        Returns:
            Dicionário com resultado da exclusão
        """
        try:
            response = self.client.voices.delete(voice_id)
            
            return response.model_dump()
            
        except Exception as e:
            print(f"Erro ao excluir voz: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Obtém informações da conta usando API oficial"""
        try:
            account = self.client.accounts.retrieve()
            
            # Usar model_dump() para obter dados
            return account.model_dump()
            
        except Exception as e:
            print(f"Erro ao obter informações da conta: {e}")
            raise
    
    def get_available_voices_summary(self) -> List[Dict[str, str]]:
        """Obtém resumo das vozes disponíveis para fácil seleção"""
        try:
            voices = self.client.voices.list()
            
            summary = []
            for voice in voices[:10]:  # Primeiras 10 vozes
                summary.append({
                    'id': voice.id,
                    'name': voice.name,
                    'gender': voice.gender or 'N/A',
                    'description': voice.description or 'N/A'
                })
            
            return summary
            
        except Exception as e:
            print(f"Erro ao obter resumo de vozes: {e}")
            return []
    
    @staticmethod
    def base64_to_bytes(base64_string: str) -> bytes:
        """Converte string base64 para bytes"""
        try:
            # Remover prefixo data URL se presente
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            return base64.b64decode(base64_string)
        except Exception as e:
            print(f"Erro ao converter base64: {e}")
            raise
    
    @staticmethod
    def bytes_to_base64(audio_data: bytes) -> str:
        """Converte bytes para string base64"""
        return base64.b64encode(audio_data).decode('utf-8')


# Função de conveniência para uso rápido
def create_voice_clone_final(name: str, audio_base64: str, description: str = "", enhance: bool = True) -> Dict[str, Any]:
    """
    Função de conveniência para criar clone de voz usando API oficial
    
    Args:
        name: Nome da voz
        audio_base64: Áudio em base64
        description: Descrição opcional
        enhance: Se deve usar enhancement
        
    Returns:
        Informações da voz criada
    """
    cloner = LMNTVoiceClonerFinal()
    audio_bytes = cloner.base64_to_bytes(audio_base64)
    return cloner.clone_voice(name, audio_bytes, description, enhance)


if __name__ == "__main__":
    # Teste da classe final com API oficial
    print("Testando LMNT Voice Cloner FINAL...")
    
    try:
        cloner = LMNTVoiceClonerFinal()
        
        # Testar informações da conta
        print("\n1. Informações da Conta:")
        account_info = cloner.get_account_info()
        print(f"   Plano: {account_info.get('plan', {}).get('type', 'N/A')}")
        print(f"   Limite de caracteres: {account_info.get('plan', {}).get('character_limit', 'N/A')}")
        
        # Testar listagem de vozes
        print("\n2. Vozes Disponíveis:")
        voices = cloner.list_voices()
        print(f"   Total: {len(voices.get('voices', []))}")
        
        # Mostrar resumo
        summary = cloner.get_available_voices_summary()
        for voice in summary[:5]:
            print(f"   - {voice['name']} ({voice['id']}) - {voice['gender']}")
        
        # Testar geração de áudio
        if voices.get('voices'):
            first_voice = voices['voices'][0]
            voice_id = first_voice['id']
            
            print(f"\n3. Testando Geração de Áudio com voz: {first_voice['name']}")
            
            # Gerar áudio para arquivo
            output_file = "test_final_speech.mp3"
            cloner.synthesize_to_file(
                voice_id=voice_id,
                text="Este é um teste do LMNT Voice Cloner Final corrigido!",
                filepath=output_file
            )
            
            print(f"   Áudio gerado: {output_file}")
        
        print("\n4. Teste concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro no teste: {e}")
        import traceback
        traceback.print_exc()
