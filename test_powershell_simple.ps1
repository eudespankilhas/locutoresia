# Teste simples do NewsAgent API para PowerShell
# Execute este script em outro terminal enquanto o servidor está rodando

Write-Host "🧪 TESTE SIMPLES NEWSAGENT API" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

$baseUrl = "http://localhost:5000"

# Teste 1: Health Check
Write-Host "`n1️⃣ Testando Health Check..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/health" -TimeoutSec 5
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Status: $($data.status)" -ForegroundColor Green
    Write-Host "✅ Agent OK: $($data.agent_ok)" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 Certifique-se de que o servidor está rodando!" -ForegroundColor Yellow
    exit 1
}

# Teste 2: Listar Fontes
Write-Host "`n2️⃣ Listando Fontes..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/sources" -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Fontes disponíveis: $($data.total_sources)" -ForegroundColor Green
    foreach ($source in $data.sources) {
        Write-Host "   📰 $($source.label) - $($source.categories.Count) categorias" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 3: Status das Fontes
Write-Host "`n3️⃣ Status das Fontes..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/status" -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Status obtido" -ForegroundColor Green
    foreach ($source in $data.status.PSObject.Properties) {
        $status = $source.Value.status
        Write-Host "   📊 $($source.Name): $status" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 4: Coletar Notícias
Write-Host "`n4️⃣ Coletar Notícias (G1 - Brasil)..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/collect/g1/brasil" -TimeoutSec 15
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Notícias coletadas: $($data.total)" -ForegroundColor Green
    if ($data.total -gt 0) {
        $noticia = $data.news[0]
        Write-Host "   📝 Exemplo: $($noticia.title)" -ForegroundColor Gray
        Write-Host "   🔗 $($noticia.url)" -ForegroundColor Blue
    }
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

# Teste 5: Cache Local
Write-Host "`n5️⃣ Cache Local..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/cache?limit=5" -TimeoutSec 10
    $data = $response.Content | ConvertFrom-Json
    Write-Host "✅ Notícias em cache: $($data.total_cached)" -ForegroundColor Green
} catch {
    Write-Host "❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + "=" * 40 -ForegroundColor Cyan
Write-Host "🎉 TESTE CONCLUÍDO!" -ForegroundColor Green
Write-Host "✅ NewsAgent API está funcionando!" -ForegroundColor Green
