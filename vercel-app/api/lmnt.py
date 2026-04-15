"""
API Backend para LMNT Voice Cloner - Vercel Serverless Function
"""

import os
import json
import base64
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

# Importar nosso clonador LMNT
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from core.lmnt_voice_cloner_final import LMNTVoiceClonerFinal

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        path = urlparse(self.path).path
        
        if path == '/api/lmnt/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "ok", "message": "LMNT API is ready"}
            self.wfile.write(json.dumps(response).encode())
            return
        
        elif path == '/api/lmnt/voices':
            self.handle_list_voices()
            return
        
        elif path.startswith('/api/lmnt/voice/'):
            voice_id = path.split('/')[-1]
            self.handle_get_voice(voice_id)
            return
        
        elif path == '/api/lmnt/account':
            self.handle_account_info()
            return
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        path = urlparse(self.path).path
        
        if path == '/api/lmnt/generate':
            self.handle_generate_speech()
            return
        
        elif path == '/api/lmnt/clone':
            self.handle_clone_voice()
            return
        
        elif path.startswith('/api/lmnt/voice/'):
            parts = path.split('/')
            if len(parts) >= 5 and parts[4] == 'update':
                voice_id = parts[3]
                self.handle_update_voice(voice_id)
                return
            elif len(parts) >= 5 and parts[4] == 'delete':
                voice_id = parts[3]
                self.handle_delete_voice(voice_id)
                return
        
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode())
    
    def handle_list_voices(self):
        """Listar todas as vozes disponíveis"""
        try:
            cloner = LMNTVoiceClonerFinal()
            voices = cloner.list_voices()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(voices).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_get_voice(self, voice_id):
        """Obter informações de uma voz específica"""
        try:
            cloner = LMNTVoiceClonerFinal()
            voice = cloner.get_voice(voice_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(voice).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_account_info(self):
        """Obter informações da conta"""
        try:
            cloner = LMNTVoiceClonerFinal()
            account = cloner.get_account_info()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(account).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_generate_speech(self):
        """Gerar áudio a partir de texto"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            voice_id = data.get('voice_id')
            text = data.get('text')
            format_type = data.get('format', 'mp3')
            
            if not voice_id or not text:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "voice_id and text are required"}).encode())
                return
            
            cloner = LMNTVoiceClonerFinal()
            audio_bytes = cloner.synthesize_with_cloned_voice(voice_id, text, format_type)
            
            # Retornar áudio como base64
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            response = {
                "success": True,
                "audio_base64": audio_base64,
                "format": format_type,
                "voice_id": voice_id,
                "text": text
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_clone_voice(self):
        """Criar uma nova voz clonada"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            name = data.get('name')
            audio_base64 = data.get('audio_base64')
            description = data.get('description', '')
            enhance = data.get('enhance', True)
            
            if not name or not audio_base64:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "name and audio_base64 are required"}).encode())
                return
            
            cloner = LMNTVoiceClonerFinal()
            audio_bytes = cloner.base64_to_bytes(audio_base64)
            voice = cloner.clone_voice(name, audio_bytes, description, enhance)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(voice).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_update_voice(self, voice_id):
        """Atualizar informações de uma voz"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            cloner = LMNTVoiceClonerFinal()
            updated_voice = cloner.update_voice(voice_id, **data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(updated_voice).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_delete_voice(self, voice_id):
        """Excluir uma voz"""
        try:
            cloner = LMNTVoiceClonerFinal()
            result = cloner.delete_voice(voice_id)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def send_error_response(self, error_message, status_code=500):
        """Enviar resposta de erro"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error": error_message}).encode())
