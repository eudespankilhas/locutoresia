from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
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
            from tts_generator_mock import get_tts_generator
            tts = get_tts_generator()
            print(f"Usando gerador TTS: {type(tts).__name__}")
        except ImportError:
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

def handler(request, response):
    """Handler para Vercel serverless functions"""
    with app.request_context(request.environ):
        return app(request.environ, response)

# Para desenvolvimento local
if __name__ == '__main__':
    print("Iniciando Locutores IA Server...")
    print("Acesse: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)