@echo off
echo ====================================
echo    DEPLOY COMPLETO LOCUTORES IA
echo ====================================
echo.

echo [1/5] Verificando ambiente Python...
py --version
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    pause
    exit /b 1
)

echo.
echo [2/5] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERRO: Falha ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [3/5] Verificando integracao LMNT...
py -c "from backend.lmnt_integration import lmnt_integration; print('LMNT Status:', lmnt_integration.get_status())"
if %errorlevel% neq 0 (
    echo AVISO: LMNT integration pode nao estar funcionando
)

echo.
echo [4/5] Fazendo commit das alteracoes...
git add .
git commit -m "feat: Integrar LMNT Voice Cloner ao projeto Locutores IA

- Adicionar endpoints LMNT ao backend
- Integrar clonagem de vozes ao sistema existente
- Atualizar requirements.txt com LMNT SDK
- Criar workflow de deploy automatico
- Adicionar GitHub Actions para deploy na Vercel"
if %errorlevel% neq 0 (
    echo AVISO: Nao foi possivel fazer commit (pode ja estar tudo commitado)
)

echo.
echo [5/5] Enviando para GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ERRO: Falha ao enviar para GitHub!
    pause
    exit /b 1
)

echo.
echo ====================================
echo    DEPLOY CONCLUIDO!
echo ====================================
echo.
echo Acesse sua aplicacao em:
echo https://locutores-ia.vercel.app
echo.
echo Endpoints LMNT disponiveis:
echo - GET  /api/lmnt/status
echo - GET  /api/lmnt/voices  
echo - POST /api/lmnt/generate
echo - POST /api/lmnt/clone
echo - GET  /api/lmnt/voice/{id}
echo.
echo Pressione qualquer tecla para sair...
pause > nul
