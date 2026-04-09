# Script para configurar Git e enviar para GitHub
# Execute: .\setup-github.ps1

Write-Host "🚀 Configurando Locutores IA para GitHub" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Verificar se Git está instalado
try {
    $gitVersion = git --version
    Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git não encontrado. Por favor, instale o Git:" -ForegroundColor Red
    Write-Host "   https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Perguntar nome do usuário GitHub
$githubUser = Read-Host "Digite seu nome de usuário do GitHub"
if ([string]::IsNullOrWhiteSpace($githubUser)) {
    Write-Host "❌ Nome de usuário é obrigatório" -ForegroundColor Red
    exit 1
}

# Perguntar email
$gitEmail = Read-Host "Digite seu email para configuração do Git"
if ([string]::IsNullOrWhiteSpace($gitEmail)) {
    $gitEmail = "$githubUser@users.noreply.github.com"
    Write-Host "⚠️  Usando email padrão: $gitEmail" -ForegroundColor Yellow
}

# Configurar Git
git config --global user.name "$githubUser"
git config --global user.email "$gitEmail"

Write-Host "✅ Git configurado com:" -ForegroundColor Green
Write-Host "   Usuário: $githubUser" -ForegroundColor Cyan
Write-Host "   Email: $gitEmail" -ForegroundColor Cyan

# Verificar se já é um repositório Git
if (Test-Path .git) {
    Write-Host "⚠️  Repositório Git já existe" -ForegroundColor Yellow
    $reset = Read-Host "Deseja resetar o repositório? (s/N)"
    if ($reset -eq 's' -or $reset -eq 'S') {
        Remove-Item -Recurse -Force .git
        Write-Host "🗑️  Repositório antigo removido" -ForegroundColor Green
    }
}

# Inicializar Git
if (-not (Test-Path .git)) {
    git init
    Write-Host "✅ Repositório Git inicializado" -ForegroundColor Green
}

# Adicionar todos os arquivos
git add .
Write-Host "✅ Arquivos adicionados" -ForegroundColor Green

# Commit inicial
git commit -m "🎉 Initial commit - Locutores IA v1.0

- Sistema de geração de voz com IA
- MiniDAW para mixagem profissional
- Multi-track com efeitos
- Auto Fade 1.05s
- Exportação WAV/MP3
- Interface responsiva"

Write-Host "✅ Commit realizado" -ForegroundColor Green

# Configurar remote origin
$repoUrl = "https://github.com/$githubUser/locutores-ia.git"
Write-Host "🔗 Configurando remote origin: $repoUrl" -ForegroundColor Cyan

# Remover remote antigo se existir
git remote remove origin 2>$null

# Adicionar novo remote
git remote add origin $repoUrl

Write-Host "" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "🎉 Repositório configurado localmente!" -ForegroundColor Green
Write-Host "" -ForegroundColor White
Write-Host "Próximos passos:" -ForegroundColor Yellow
Write-Host "1. Crie o repositório no GitHub:" -ForegroundColor Cyan
Write-Host "   https://github.com/new" -ForegroundColor White
Write-Host "   Nome: locutores-ia" -ForegroundColor White
Write-Host "" -ForegroundColor Cyan
Write-Host "2. Execute o push:" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host "" -ForegroundColor Cyan
Write-Host "3. Configure no Vercel:" -ForegroundColor Cyan
Write-Host "   https://vercel.com/new" -ForegroundColor White
Write-Host "   Importe o repositório locutores-ia" -ForegroundColor White
Write-Host "" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Perguntar se deseja fazer push agora
$pushNow = Read-Host "Deseja fazer push agora? (s/N)"
if ($pushNow -eq 's' -or $pushNow -eq 'S') {
    Write-Host "⬆️  Fazendo push para GitHub..." -ForegroundColor Cyan
    git push -u origin main
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Código enviado para GitHub com sucesso!" -ForegroundColor Green
        Write-Host "" -ForegroundColor Green
        Write-Host "🚀 Agora configure no Vercel:" -ForegroundColor Green
        Write-Host "   https://vercel.com/new" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Erro ao fazer push. Verifique se o repositório existe no GitHub." -ForegroundColor Red
    }
}

Write-Host "" -ForegroundColor Green
Write-Host "Para mais informações, consulte DEPLOY_VERCEL.md" -ForegroundColor Cyan
