@echo off
echo ====================================
echo    DEPLOY FINAL - LOCUTORES IA
echo ====================================
echo.

echo [1/6] Configurando GitHub Token...
git config --global credential.helper store
git config --global user.name "Locutores IA Deploy"
git config --global user.email "deploy@locutores-ia.com"

echo.
echo [2/6] Configurando remote com token...
git remote set-url origin https://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@github.com/usuario/repo.git

echo.
echo [3/6] Verificando status do repositório...
git status

echo.
echo [4/6] Adicionando arquivos alterados...
git add .
git add -A

echo.
echo [5/6] Fazendo commit...
git commit -m "feat: Deploy completo com LMNT Voice Cloner

- Integrar LMNT Voice Cloner ao projeto existente
- Adicionar endpoints de clonagem de vozes
- Configurar GitHub Actions para deploy automático
- Atualizar dependências com LMNT SDK
- Testar integração completa

GitHub Token: ghp_***"
if %errorlevel% neq 0 (
    echo AVISO: Nada para commit (pode ja estar tudo atualizado)
)

echo.
echo [6/6] Enviando para GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ERRO: Falha ao enviar para GitHub!
    echo Verifique o token e as permissões do repositório
    pause
    exit /b 1
)

echo.
echo ====================================
echo    ✅ DEPLOY CONCLUIDO!
echo ====================================
echo.
echo 🚀 Aplicação sera deployada automaticamente na Vercel
echo 📦 GitHub Actions ira processar o deploy
echo 🌐 URL: https://locutores-ia.vercel.app
echo.
echo 🔗 Endpoints LMNT disponiveis:
echo    - GET  /api/lmnt/status
echo    - GET  /api/lmnt/voices
echo    - POST /api/lmnt/generate
echo    - POST /api/lmnt/clone
echo    - GET  /api/lmnt/voice/{id}
echo.
echo ⏱️  Aguarde 2-3 minutos para o deploy completar...
echo 📊 Acompanhe em: https://vercel.com/dashboard
echo.
echo Pressione qualquer tecla para sair...
pause > nul
