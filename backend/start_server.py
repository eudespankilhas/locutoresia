#!/usr/bin/env python3
"""
Startup script for News Automation Backend Server
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        import requests
        import feedparser
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Installing requirements...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False

def check_env_vars():
    """Check if environment variables are set"""
    required_vars = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {', '.join(missing_vars)}")
        print("   The server will run but database operations may fail")
        print("   Set these variables in your .env file or environment")
        return False
    
    print("✅ Environment variables are set")
    return True

def main():
    print("🚀 Starting News Automation Backend Server")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    check_env_vars()
    
    print("\n🌐 Starting Flask server...")
    print("   Server will be available at: http://localhost:5000")
    print("   API Documentation:")
    print("     GET  /api/news/status     - Get automation status")
    print("     POST /api/news/start      - Start automation")
    print("     POST /api/news/stop       - Stop automation") 
    print("     POST /api/news/execute    - Execute news cycle")
    print("     POST /api/newpost/publish - Publish to NewPost-IA")
    print("     GET  /api/health          - Health check")
    print("\n   Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the server
        from news_api_server import app
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
