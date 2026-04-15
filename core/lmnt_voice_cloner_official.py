import os
import base64
from typing import Optional, Dict, Any
import io
from dotenv import load_dotenv
from lmnt import Lmnt

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))


class LMNTVoiceClonerOfficial:
    """Classe para clonagem de vozes usando API LMNT OFICIAL"""
    
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
            
            # Converter para dicionário para compatibilidade com código existente
            result = {
                'id': voice.id,
                'name': voice.name,
                'description': voice.description,
                'gender': voice.gender,
                'age': voice.age,
                'accent': voice.accent,
                'language': voice.language,
                'is_custom': voice.is_custom,
                'is_public': voice.is_public,
                'created_at': voice.created_at.isoformat() if voice.created_at else None,
                'metadata': voice.metadata,
                'sample_audio_url': voice.sample_audio_url
            }
            
            print(f"Voz clonada com sucesso: {voice.id}")
            return result
            
        except Exception as e:
            print(f"Erro ao clonar voz: {e}")
            raise
    
    def list_voices(self) -> Dict[str, Any]:
        """Lista todas as vozes disponíveis na conta LMNT usando API oficial"""
        try:
            voices_response = self.client.voices.list()
            
            # Converter para formato compatível
            voices_list = []
            for voice in voices_response.data:
                voice_dict = {
                    'id': voice.id,
                    'name': voice.name,
                    'description': voice.description,
                    'gender': voice.gender,
                    'age': voice.age,
                    'accent': voice.accent,
                    'language': voice.language,
                    'is_custom': voice.is_custom,
                    'is_public': voice.is_public,
                    'created_at': voice.created_at.isoformat() if voice.created_at else None,
                    'metadata': voice.metadata,
                    'sample_audio_url': voice.sample_audio_url
                }
                voices_list.append(voice_dict)
            
            return {
                'voices': voices_list,
                'total_count': len(voices_list)
            }
            
        except Exception as e:
            print(f"Erro ao listar vozes: {e}")
            raise
    
    def get_voice(self, voice_id: str) -> Dict[str, Any]:
        """Obtém informações de uma voz específica usando API oficial"""
        try:
            voice = self.client.voices.retrieve(voice_id)
            
            # Converter para formato compatível
            return {
                'id': voice.id,
                'name': voice.name,
                'description': voice.description,
                'gender': voice.gender,
                'age': voice.age,
                'accent': voice.accent,
                'language': voice.language,
                'is_custom': voice.is_custom,
                'is_public': voice.is_public,
                'created_at': voice.created_at.isoformat() if voice.created_at else None,
                'updated_at': voice.updated_at.isoformat() if voice.updated_at else None,
                'metadata': voice.metadata,
                'sample_audio_url': voice.sample_audio_url
            }
            
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
            
            return response.content
            
        except Exception as e:
            print(f"Erro na síntese: {e}")
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
            response = self.client.speech.generate_detailed(
                text=text,
                voice=voice_id,
                format=format,
                return_detailed=True
            )
            
            return {
                'audio': response.audio,
                'duration': response.duration,
                'format': response.format,
                'voice_id': response.voice_id,
                'text': response.text,
                'created_at': response.created_at.isoformat() if response.created_at else None,
                'metadata': response.metadata
            }
            
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
            
            return {
                'success': True,
                'voice': {
                    'id': updated_voice.voice.id,
                    'name': updated_voice.voice.name,
                    'description': updated_voice.voice.description,
                    'updated_at': updated_voice.updated_at.isoformat() if updated_voice.updated_at else None
                },
                'message': updated_voice.message
            }
            
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
            
            return {
                'success': response.success,
                'voice_id': response.voice_id,
                'message': response.message,
                'deleted_at': response.deleted_at.isoformat() if response.deleted_at else None
            }
            
        except Exception as e:
            print(f"Erro ao excluir voz: {e}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """Obtém informações da conta usando API oficial"""
        try:
            account = self.client.accounts.retrieve()
            
            return {
                'account_id': account.id,
                'email': account.email,
                'name': account.name,
                'plan': account.plan,
                'credits_remaining': account.credits_remaining,
                'credits_used': account.credits_used,
                'api_calls_made': account.api_calls_made,
                'voices_created': account.voices_created,
                'created_at': account.created_at.isoformat() if account.created_at else None,
                'updated_at': account.updated_at.isoformat() if account.updated_at else None,
                'metadata': account.metadata
            }
            
        except Exception as e:
            print(f"Erro ao obter informações da conta: {e}")
            raise
    
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
def create_voice_clone_official(name: str, audio_base64: str, description: str = "", enhance: bool = True) -> Dict[str, Any]:
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
    cloner = LMNTVoiceClonerOfficial()
    audio_bytes = cloner.base64_to_bytes(audio_base64)
    return cloner.clone_voice(name, audio_bytes, description, enhance)


if __name__ == "__main__":
    # Teste da classe com API oficial
    print("Testando LMNT Voice Cloner Oficial...")
    
    # Verificar se a API key está configurada
    api_key = os.environ.get("LMNT_API_KEY")
    if not api_key:
        print("Configure LMNT_API_KEY no arquivo .env para testar")
    else:
        print(f"API Key encontrada: {api_key[:10]}...")
        
        # Listar vozes existentes
        try:
            cloner = LMNTVoiceClonerOfficial()
            voices = cloner.list_voices()
            print(f"Vozes encontradas: {len(voices.get('voices', []))}")
            
            # Obter informações da conta
            account_info = cloner.get_account_info()
            print(f"Créditos restantes: {account_info.get('credits_remaining', 'N/A')}")
            
        except Exception as e:
            print(f"Erro ao testar: {e}")
