# API handler para Vercel serverless
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

# Vercel serverless handler
def handler(request, response):
    """WSGI handler for Vercel serverless functions"""
    return app(request.environ, response.start_response)

# Alternative Vercel handler using vercel-python format
try:
    from http.server import BaseHTTPRequestHandler
    class VercelHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            with app.test_client() as client:
                resp = client.get(self.path)
                self.send_response(resp.status_code)
                for key, value in resp.headers:
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(resp.data)
        
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            with app.test_client() as client:
                resp = client.post(self.path, data=body, content_type=self.headers.get('Content-Type', 'application/json'))
                self.send_response(resp.status_code)
                for key, value in resp.headers:
                    self.send_header(key, value)
                self.end_headers()
                self.wfile.write(resp.data)
except ImportError:
    pass

# Export handler for Vercel
from app import app as application
