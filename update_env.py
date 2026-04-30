ENV_CONTENT = """FLASK_DEBUG=True
FLASK_ENV=development
GEMINI_API_KEY=AIzaSyA9TQ1ZQEmJlhW7ggQczAhbglNvPdF6Sus
SUPABASE_URL=https://ravpbfkicqkwjxejuzty.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhdnBiZmtpY3Frd2p4ZWp1enR5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNDMwOCwiZXhwIjoyMDkyODkwMzA4fQ.QAHywO5Uu70dmcMQM7t7EslEqZG4y79-kLUIxPR81RM
"""

with open('.env', 'w', encoding='utf-8') as f:
    f.write(ENV_CONTENT)

print("Arquivo .env atualizado com projeto ravpbfkicqkwjxejuzty")
