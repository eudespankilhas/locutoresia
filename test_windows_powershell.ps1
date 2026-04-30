# Teste do NewsAgent API usando PowerShell do Windows

Write-Host "🚀 TESTANDO NEWSAGENT API COM POWERSHELL" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

# Base URL
$baseUrl = "http://localhost:5000"

# Testar se servidor está rodando
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/" -TimeoutSec 5
    Write-Host "✅ Servidor Flask está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Servidor não está rodando. Inicie com: python backend/app.py" -ForegroundColor Red
    exit 1
}

# Testar endpoints
$endpoints = @(
    @{Method="GET"; Url="/api/news/sources"; Desc="Listar fontes disponíveis"},
    @{Method="GET"; Url="/api/news/status"; Desc="Verificar status das fontes"},
    @{Method="GET"; Url="/api/news/health"; Desc="Health check do serviço"},
    @{Method="GET"; Url="/api/news/cache?limit=5"; Desc="Obter notícias em cache"},
    @{Method="GET"; Url="/api/news/collect/g1/brasil"; Desc="Coletar notícias do G1 - Brasil"}
)

foreach ($endpoint in $endpoints) {
    try {
        Write-Host "`n🔍 Testando: $($endpoint.Desc)" -ForegroundColor Yellow
        Write-Host "   $($endpoint.Method) $($endpoint.Url)" -ForegroundColor Gray
        
        if ($endpoint.Method -eq "GET") {
            $response = Invoke-WebRequest -Uri "$baseUrl$($endpoint.Url)" -TimeoutSec 10
            $data = $response.Content | ConvertFrom-Json
            
            Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
            Write-Host "   ✅ Sucesso: $($data.success)" -ForegroundColor Green
            
            # Mostrar informações específicas
            if ($endpoint.Url -match "sources") {
                Write-Host "   📰 Fontes: $($data.sources.Count)" -ForegroundColor Blue
                for ($i = 0; $i -lt [Math]::Min(2, $data.sources.Count); $i++) {
                    $source = $data.sources[$i]
                    Write-Host "      - $($source.label): $($source.categories.Count) categorias" -ForegroundColor Gray
                }
            }
            elseif ($endpoint.Url -match "cache") {
                Write-Host "   💾 Notícias em cache: $($data.total_cached)" -ForegroundColor Blue
            }
            elseif ($endpoint.Url -match "collect") {
                Write-Host "   📰 Notícias coletadas: $($data.total)" -ForegroundColor Blue
            }
            elseif ($endpoint.Url -match "health") {
                Write-Host "   🏥 Status: $($data.status)" -ForegroundColor Blue
            }
        }
    } catch {
        Write-Host "   ❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Testar POST endpoint
try {
    Write-Host "`n🔍 Testando: Coleta com filtros" -ForegroundColor Yellow
    Write-Host "   POST /api/news/execute" -ForegroundColor Gray
    
    $payload = @{
        enabled_sources = @{
            g1 = $true
            folha = $true
        }
        categories = @("brasil")
        limit = 10
    } | ConvertTo-Json
    
    $response = Invoke-WebRequest -Uri "$baseUrl/api/news/execute" -Method POST -ContentType "application/json" -Body $payload -TimeoutSec 15
    $data = $response.Content | ConvertFrom-Json
    
    Write-Host "   Status: $($response.StatusCode)" -ForegroundColor Gray
    Write-Host "   ✅ Sucesso: $($data.success)" -ForegroundColor Green
    Write-Host "   📰 Notícias coletadas: $($data.total_news)" -ForegroundColor Blue
    
    # Mostrar estatísticas
    if ($data.collection_stats) {
        foreach ($source in $data.collection_stats.PSObject.Properties) {
            $collected = $source.Value.collected
            Write-Host "      - $($source.Name): $collected notícias" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "   ❌ Erro: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n" + "=" * 50 -ForegroundColor Green
Write-Host "🎉 TESTE CONCLUÍDO!" -ForegroundColor Green
Write-Host "✅ NewsAgent API testada com PowerShell!" -ForegroundColor Green
