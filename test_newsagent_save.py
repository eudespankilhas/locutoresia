import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.news_utils import NewsUtils

# Testar salvamento usando NewsUtils
news_utils = NewsUtils()

# Dados de teste
test_news = {
    "title": "Notícia de Teste NewsAgent",
    "source_url": "https://exame.com/noticia-teste-123",
    "content": "Conteúdo da notícia de teste",
    "image_url": "https://example.com/image.jpg",
    "category": "tecnologia",
    "published_at": "2026-04-24T16:00:00",
    "source": "Exame"
}

print("Testando salvamento com NewsUtils...")
success, message = news_utils.save_to_supabase(test_news)

print(f"Resultado: {success}")
print(f"Mensagem: {message}")

if success:
    print("\n✅ Notícia salva com sucesso!")
else:
    print("\n❌ Falha ao salvar notícia")
