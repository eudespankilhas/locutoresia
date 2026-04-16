"""
Upload Handler para Vercel - Corrige problema de uploads desativados
"""

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

def handle_upload(request):
    """Handler genérico para uploads na Vercel"""
    try:
        # Verificar se o arquivo foi enviado
        if 'file' not in request.files:
            return {'error': 'Nenhum arquivo enviado'}, 400
        
        file = request.files['file']
        if file.filename == '':
            return {'error': 'Nenhum arquivo selecionado'}, 400
        
        # Verificar extensão permitida
        allowed_extensions = ['.wav', '.mp3', '.ogg', '.m4a']
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return {'error': f'Extensão não permitida: {file_ext}'}, 400
        
        # Gerar nome único
        unique_filename = f"{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
        
        # Salvar no diretório temporário da Vercel
        upload_dir = '/tmp/generated_audio'
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, unique_filename)
        file.save(filepath)
        
        # Retornar informações do arquivo
        file_info = {
            'success': True,
            'filename': unique_filename,
            'original_filename': filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath),
            'download_url': f'/api/download/{unique_filename}',
            'message': 'Arquivo enviado com sucesso!'
        }
        
        return file_info, 200
        
    except Exception as e:
        return {'error': f'Erro no upload: {str(e)}'}, 500

def handle_voice_upload(request):
    """Handler específico para upload de voz para clonagem"""
    try:
        # Verificar se o arquivo foi enviado
        if 'voice_file' not in request.files:
            return {'error': 'Nenhum arquivo de voz enviado'}, 400
        
        file = request.files['voice_file']
        if file.filename == '':
            return {'error': 'Nenhum arquivo de voz selecionado'}, 400
        
        # Verificar se é arquivo de áudio
        allowed_extensions = ['.wav', '.mp3', '.m4a']
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return {'error': f'Formato de áudio não suportado: {file_ext}'}, 400
        
        # Gerar nome único para voz
        voice_filename = f"voice_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
        
        # Salvar no diretório temporário
        upload_dir = '/tmp/generated_audio'
        os.makedirs(upload_dir, exist_ok=True)
        
        filepath = os.path.join(upload_dir, voice_filename)
        file.save(filepath)
        
        # Retornar informações para processamento
        voice_info = {
            'success': True,
            'voice_filename': voice_filename,
            'original_filename': filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath),
            'format': file_ext.replace('.', ''),
            'message': 'Voz enviada para processamento!'
        }
        
        return voice_info, 200
        
    except Exception as e:
        return {'error': f'Erro no upload de voz: {str(e)}'}, 500
