@echo off
echo ==========================================
echo 🚀 DEPLOY LOCUTORES IA - VERCEL
echo ==========================================
echo.

echo 📦 Adicionando arquivos ao Git...
git add vercel.json
git add backend/app.py
git add static/script.js
git add templates/index.html
git add deploy.bat

echo.
echo 💾 Fazendo commit...
git commit -m "Implementa Web Speech API fallback quando Edge TTS falha (403)"

echo.
echo 📤 Enviando para GitHub...
git push

echo.
echo 🚀 Fazendo deploy no Vercel...
vercel --prod --yes

echo.
echo ==========================================
echo ✅ Deploy concluido!
echo ==========================================
pause
