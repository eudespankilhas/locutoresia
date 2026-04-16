from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import uuid
from datetime import datetime

# No Vercel, as variáveis de ambiente são configuradas diretamente no painel
# Não precisamos carregar de arquivo .env em produção
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

app = Flask(__name__, 
           template_folder='../templates',
           static_folder='../static')

app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'generated_audio')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/minidaw')
def minidaw():
    return render_template('minidaw.html')

@app.route('/minidaw-react')
def minidaw_react():
    return render_template('minidaw-react.html')

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Texto não fornecido'}), 400
        text = data['text']
        voice_model = data.get('voice', 'pt-BR-AntonioNeural')
        style = data.get('style', 'normal')
        language = data.get('language', 'pt-BR')
        if len(text.strip()) == 0:
            return jsonify({'error': 'Texto não pode estar vazio'}), 400
        if len(text) > 5000:
            return jsonify({'error': 'Texto muito longo (máximo 5000 caracteres)'}), 400
        try:
            # Importar TTSGenerator do core (Google Gemini)
            from core.tts_generator import TTSGenerator
            tts = TTSGenerator()
            print(f"Usando gerador TTS: {type(tts).__name__}")
        except ImportError as e:
            print(f"Erro ao importar TTS: {e}")
            return jsonify({'error': 'Módulo TTS não disponível'}), 500
        try:
            audio_data = tts.generate_speech(text=text, voice_model=voice_model, style=style, language=language)
            filename = f"locution_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            with open(filepath, 'wb') as f:
                f.write(audio_data)
            return jsonify({'success': True, 'filename': filename, 'download_url': f'/api/download/{filename}', 'message': 'Áudio gerado com sucesso!'})
        except Exception as e:
            return jsonify({'error': f'Erro ao gerar áudio: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'Arquivo não encontrado'}), 404
        mimetype = 'audio/mpeg' if filename.endswith('.mp3') else 'audio/wav'
        return send_file(filepath, as_attachment=False, download_name=filename, mimetype=mimetype)
    except Exception as e:
        return jsonify({'error': f'Erro ao baixar arquivo: {str(e)}'}), 500

@app.route('/api/voices')
def get_voices():
    return jsonify({'voices': []})

@app.route('/api/stats')
def get_stats():
    return jsonify({'voices_count': 50, 'audios_generated': 1247, 'active_projects': 89, 'users_count': 342})

@app.route('/api/debug/env')
def debug_env():
    """Endpoint para debug de variáveis de ambiente"""
    return jsonify({
        'gemini_key_exists': bool(os.getenv('GEMINI_API_KEY')),
        'gemini_key_length': len(os.getenv('GEMINI_API_KEY', '')),
        'google_ai_studio_key_exists': bool(os.getenv('GOOGLE_AI_STUDIO_API_KEY')),
        'google_ai_studio_key_length': len(os.getenv('GOOGLE_AI_STUDIO_API_KEY', '')),
        'elevenlabs_key_exists': bool(os.getenv('ELEVENLABS_API_KEY')),
        'elevenlabs_key_length': len(os.getenv('ELEVENLABS_API_KEY', '')),
        'environment': os.getenv('FLASK_ENV', 'not_set'),
        'vercel_env': os.getenv('VERCEL', 'not_set')
    })

@app.route('/api/synthesize-cloned-voice', methods=['POST'])
def synthesize_cloned_voice():
    try:
        data = request.get_json()
        if not data or 'voice_id' not in data or 'text' not in data:
            return jsonify({'error': 'ID da voz e texto são obrigatórios'}), 400
        voice_id = data['voice_id']
        text = data['text']
        if len(text.strip()) == 0:
            return jsonify({'error': 'Texto não pode estar vazio'}), 400
        if len(text) > 5000:
            return jsonify({'error': 'Texto muito longo (máximo 5000 caracteres)'}), 400
        try:
            from elevenlabs_voice_cloner import ElevenLabsVoiceCloner
            cloner = ElevenLabsVoiceCloner()
            audio_data = cloner.synthesize_with_cloned_voice(voice_id, text)
        except ImportError:
            return jsonify({'error': 'Módulo ElevenLabs não disponível'}), 500
        filename = f"elevenlabs_{uuid.uuid4().hex[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        return jsonify({'success': True, 'filename': filename, 'download_url': f'/api/download/{filename}', 'message': 'Áudio gerado com sucesso!'})
    except Exception as e:
        return jsonify({'error': f'Erro ao sintetizar áudio: {str(e)}'}), 500

@app.route('/api/list-elevenlabs-voices', methods=['GET'])
def list_elevenlabs_voices():
    try:
        from elevenlabs_voice_cloner import ElevenLabsVoiceCloner
        cloner = ElevenLabsVoiceCloner()
        voices_data = cloner.list_voices()
        voices = voices_data.get('voices', [])
        formatted_voices = []
        for voice in voices:
            formatted_voices.append({
                'id': voice.get('voice_id'),
                'name': voice.get('name'),
                'description': voice.get('description', 'Voz ElevenLabs'),
                'gender': 'neutral',
                'language': 'pt-BR',
                'style': 'professional',
                'avatar': f'https://picsum.photos/seed/{voice.get("name")}/80/80',
                'model': voice.get('voice_id'),
                'sampleText': f'Olá! Esta é uma amostra da voz {voice.get("name")} gerada com ElevenLabs.',
                'provider': 'elevenlabs',
            })
        return jsonify({'success': True, 'voices': formatted_voices})
    except ImportError:
        return jsonify({'error': 'Módulo ElevenLabs não disponível'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro ao listar vozes: {str(e)}'}), 500

@app.route('/api/clone-voice-elevenlabs', methods=['POST'])
def clone_voice_elevenlabs():
    return jsonify({'error': 'Clonagem requer plano pago no ElevenLabs. Acesse elevenlabs.io para upgrade.'}), 400

@app.route('/api/clone-voice', methods=['POST'])
def clone_voice():
    return jsonify({'error': 'Clonagem requer plano pago no ElevenLabs. Acesse elevenlabs.io para upgrade.'}), 400

@app.route('/api/list-cloned-voices', methods=['GET'])
def list_cloned_voices():
    return jsonify({'success': True, 'voices': []})

@app.route('/api/recent-audio', methods=['GET'])
def recent_audio():
    """Lista áudios recentes para importação na MiniDAW"""
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        files = []
        
        if os.path.exists(upload_folder):
            # List files sorted by modification time (most recent first)
            file_list = []
            for filename in os.listdir(upload_folder):
                if filename.endswith('.wav'):
                    filepath = os.path.join(upload_folder, filename)
                    stat = os.stat(filepath)
                    file_list.append({
                        'filename': filename,
                        'modified': stat.st_mtime,
                        'size': stat.st_size
                    })
            
            # Sort by modification time (most recent first) and take last 10
            file_list.sort(key=lambda x: x['modified'], reverse=True)
            files = file_list[:10]
            
            # Convert timestamps to readable format
            for file in files:
                file['modified'] = datetime.fromtimestamp(file['modified']).strftime('%Y-%m-%d %H:%M:%S')
                file['size_mb'] = round(file['size'] / (1024 * 1024), 2)
        
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        return jsonify({'error': f'Erro ao listar áudios: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Página não encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500


# ============================================================
# ENDPOINTS VOXCRAFT INTEGRATION
# ============================================================

from flask import make_response

# Sessões temporárias em memória (em produção usar Redis/DB)
voxcraft_sessions = {}

@app.route('/api/voxcraft/health', methods=['GET'])
def voxcraft_health():
    """Health check para integração VoxCraft"""
    return jsonify({
        'status': 'ok',
        'integration': 'voxcraft',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/voxcraft/receive', methods=['POST', 'OPTIONS'])
def voxcraft_receive():
    """Recebe notícia do VoxCraft e retorna URL para redirecionamento"""
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Campos obrigatórios
        text = data.get('text', '').strip()
        post_id = data.get('post_id', '').strip()
        
        if not text:
            return jsonify({'error': 'Texto não fornecido'}), 400
        if not post_id:
            return jsonify({'error': 'post_id não fornecido'}), 400
        
        # Campos opcionais
        title = data.get('title', 'Notícia VoxCraft').strip()
        category = data.get('category', 'geral').strip()
        image_url = data.get('image_url', '').strip()
        return_url = data.get('return_url', '').strip()
        
        # Sanitiza post_id (apenas alphanumeric e hífen)
        import re
        post_id = re.sub(r'[^a-zA-Z0-9\-_]', '', post_id)[:50]
        
        # Cria sessão temporária
        session_id = f"voxcraft_{post_id}_{uuid.uuid4().hex[:8]}"
        voxcraft_sessions[session_id] = {
            'post_id': post_id,
            'text': text,
            'title': title,
            'category': category,
            'image_url': image_url,
            'return_url': return_url,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'audio_filename': None
        }
        
        # Limpa sessões antigas (mais de 1 hora)
        current_time = datetime.now()
        expired = []
        for sid, session in voxcraft_sessions.items():
            created = datetime.fromisoformat(session['created_at'])
            if (current_time - created).total_seconds() > 3600:
                expired.append(sid)
        for sid in expired:
            del voxcraft_sessions[sid]
        
        # Constrói URL de redirecionamento
        from urllib.parse import quote
        base_url = request.host_url.rstrip('/')
        redirect_url = (
            f"{base_url}/?"
            f"voxcraft=true&"
            f"session_id={session_id}&"
            f"text={quote(text[:500])}&"  # Limita texto na URL
            f"post_id={post_id}&"
            f"title={quote(title[:100])}"
        )
        
        if category:
            redirect_url += f"&category={quote(category[:50])}"
        if image_url:
            redirect_url += f"&image_url={quote(image_url[:500])}"
        if return_url:
            redirect_url += f"&return_url={quote(return_url[:500])}"
        
        response = jsonify({
            'success': True,
            'session_id': session_id,
            'redirect_url': redirect_url,
            'message': 'Sessão criada. Redirecione usuário para a URL fornecida.'
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        print(f"Erro em voxcraft_receive: {str(e)}")
        response = jsonify({'error': f'Erro interno: {str(e)}'}), 500
        if isinstance(response, tuple):
            response[0].headers.add('Access-Control-Allow-Origin', '*')
        else:
            response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/api/voxcraft/metadata/<session_id>', methods=['GET'])
def voxcraft_metadata(session_id):
    """Retorna metadados da sessão VoxCraft"""
    try:
        if session_id not in voxcraft_sessions:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        session = voxcraft_sessions[session_id]
        return jsonify({
            'success': True,
            'session_id': session_id,
            'post_id': session['post_id'],
            'title': session['title'],
            'category': session['category'],
            'image_url': session['image_url'],
            'return_url': session['return_url'],
            'status': session['status'],
            'audio_filename': session['audio_filename'],
            'created_at': session['created_at']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voxcraft/complete', methods=['POST', 'OPTIONS'])
def voxcraft_complete():
    """Notifica conclusão da geração de áudio"""
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        return response
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        session_id = data.get('session_id', '').strip()
        audio_filename = data.get('audio_filename', '').strip()
        
        if not session_id:
            return jsonify({'error': 'session_id não fornecido'}), 400
        if session_id not in voxcraft_sessions:
            return jsonify({'error': 'Sessão não encontrada'}), 404
        
        # Atualiza sessão
        session = voxcraft_sessions[session_id]
        session['status'] = 'completed'
        session['audio_filename'] = audio_filename
        session['completed_at'] = datetime.now().isoformat()
        
        # Constrói URL de retorno
        return_url = session.get('return_url', '')
        if return_url:
            separator = '&' if '?' in return_url else '?'
            return_url += f"{separator}audio_filename={audio_filename}&session_id={session_id}"
        
        response = jsonify({
            'success': True,
            'message': 'Áudio gerado com sucesso',
            'return_url': return_url,
            'audio_filename': audio_filename,
            'session_id': session_id
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
        
    except Exception as e:
        print(f"Erro em voxcraft_complete: {str(e)}")
        response = jsonify({'error': str(e)}), 500
        if isinstance(response, tuple):
            response[0].headers.add('Access-Control-Allow-Origin', '*')
        else:
            response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/api/voxcraft/logs', methods=['GET'])
def voxcraft_logs():
    """Retorna logs das sessões (para debug)"""
    try:
        logs = []
        for sid, session in voxcraft_sessions.items():
            logs.append({
                'session_id': sid,
                'post_id': session['post_id'],
                'title': session['title'][:50],
                'status': session['status'],
                'created_at': session['created_at'],
                'has_audio': bool(session['audio_filename'])
            })
        
        # Ordena por data (mais recente primeiro)
        logs.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'total_sessions': len(logs),
            'sessions': logs[:20]  # Últimas 20
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Importar handlers de upload
from upload_handler import handle_upload, handle_voice_upload

# Importar integração LMNT
from lmnt_integration import lmnt_integration

# Endpoints LMNT Integration
@app.route('/api/lmnt/status', methods=['GET'])
def lmnt_status():
    """Verifica status da integração LMNT"""
    return jsonify(lmnt_integration.get_status())

@app.route('/api/lmnt/voices', methods=['GET'])
def lmnt_voices():
    """Lista vozes disponíveis no LMNT"""
    return jsonify(lmnt_integration.get_available_voices())

@app.route('/api/lmnt/generate', methods=['POST'])
def lmnt_generate():
    """Gera áudio usando LMNT"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Texto não fornecido'}), 400
        
        text = data['text'].strip()
        voice_id = data.get('voice_id')
        format_type = data.get('format', 'mp3')
        
        if len(text) == 0:
            return jsonify({'error': 'Texto não pode estar vazio'}), 400
        
        if len(text) > 1000:  # Limite do LMNT
            return jsonify({'error': 'Texto muito longo (máximo 1000 caracteres)'}), 400
        
        result = lmnt_integration.generate_speech(text, voice_id, format_type)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lmnt/clone', methods=['POST'])
def lmnt_clone():
    """Clona uma nova voz no LMNT"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'Arquivo de áudio não fornecido'}), 400
        
        audio_file = request.files['audio']
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        enhance = request.form.get('enhance', 'true').lower() == 'true'
        
        if not name:
            return jsonify({'error': 'Nome da voz não fornecido'}), 400
        
        if not audio_file.filename:
            return jsonify({'error': 'Arquivo de áudio inválido'}), 400
        
        # Ler arquivo de áudio
        audio_data = audio_file.read()
        
        result = lmnt_integration.clone_voice(name, audio_data, description, enhance)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lmnt/voice/<voice_id>', methods=['GET'])
def lmnt_voice_info(voice_id):
    """Obtém informações de uma voz específica"""
    return jsonify(lmnt_integration.get_voice_info(voice_id))

@app.route('/api/test-env', methods=['GET'])
def test_environment():
    """Testa variáveis de ambiente configuradas"""
    env_vars = {
        'LMNT_API_KEY': bool(os.environ.get('LMNT_API_KEY')),
        'GEMINI_API_KEY': bool(os.environ.get('GEMINI_API_KEY')),
        'GOOGLE_AI_STUDIO_API_KEY': bool(os.environ.get('GOOGLE_AI_STUDIO_API_KEY')),
        'ELEVENLABS_API_KEY': bool(os.environ.get('ELEVENLABS_API_KEY')),
        'VERCEL_ENV': os.environ.get('VERCEL_ENV', 'unknown'),
        'NODE_ENV': os.environ.get('NODE_ENV', 'unknown')
    }
    
    # Testar importação LMNT
    lmnt_import_test = False
    lmnt_error = None
    try:
        import lmnt
        lmnt_import_test = True
    except Exception as e:
        lmnt_error = str(e)
    
    return jsonify({
        'environment_variables': env_vars,
        'lmnt_import_success': lmnt_import_test,
        'lmnt_import_error': lmnt_error,
        'python_version': os.sys.version,
        'working_directory': os.getcwd()
    })

# Handler para Vercel serverless
from flask import Flask

# Garantir que os paths estão corretos para Vercel
if os.environ.get('VERCEL'):
    # Em produção no Vercel, ajustar paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    app.template_folder = os.path.join(base_dir, 'templates')
    app.static_folder = os.path.join(base_dir, 'static')
    app.config['UPLOAD_FOLDER'] = '/tmp/generated_audio'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Configurações adicionais para Vercel
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    app.config['UPLOAD_EXTENSIONS'] = ['.wav', '.mp3', '.ogg', '.m4a']

# Endpoints de Upload
@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint genérico para upload de arquivos"""
    try:
        result, status = handle_upload(request)
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/upload/voice', methods=['POST'])
def upload_voice():
    """Endpoint específico para upload de voz para clonagem"""
    try:
        result, status = handle_voice_upload(request)
        return jsonify(result), status
    except Exception as e:
        return jsonify({'error': f'Erro no upload de voz: {str(e)}'}), 500

def handler(request, response):
    """Handler para Vercel serverless functions"""
    with app.request_context(request.environ):
        return app(request.environ, response)

# Para desenvolvimento local
if __name__ == '__main__':
    print("Iniciando Locutores IA Server...")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)