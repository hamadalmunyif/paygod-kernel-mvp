Param()

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
Write-Host "==> RepoRoot : $repoRoot"

# Ensure output dir exists (bind mount target)
New-Item -ItemType Directory -Force -Path (Join-Path $repoRoot "_dev_out") | Out-Null

# Build runner (existing script)
& (Join-Path $repoRoot "tools\docker\build.ps1") -ImageName "paygod/runner:dev"

# Build api (single-line to avoid PS continuation issues)
$dockerfile = Join-Path $repoRoot "deploy\docker\api\Dockerfile"
Write-Host "==> Dockerfile: $dockerfile"
Write-Host "==> Image     : paygod/api:dev"

docker build -f "$dockerfile" -t "paygod/api:dev" "$repoRoot"

Write-Host "==> OK: built paygod/api:dev"
