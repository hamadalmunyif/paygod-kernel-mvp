Param()

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Write-Host "==> RepoRoot : $repoRoot"

# Build images
& (Join-Path $repoRoot "tools\docker\build_all.ps1")

# Compose up
$compose = Join-Path $repoRoot "deploy\compose\docker-compose.yml"
Write-Host "==> compose: $compose"

docker compose -f $compose up -d
Write-Host "==> UP: http://localhost:8080  (POST /api/run)"
