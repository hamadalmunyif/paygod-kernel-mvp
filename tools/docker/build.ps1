Param(
  [string]$ImageName = "paygod/runner:dev"
)

$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$dockerfile = Join-Path $repoRoot "deploy\docker\runner\Dockerfile"

Write-Host "==> RepoRoot : $repoRoot"
Write-Host "==> Dockerfile: $dockerfile"
Write-Host "==> Image     : $ImageName"

docker version | Out-Null

docker build `
  -f $dockerfile `
  -t $ImageName `
  $repoRoot

if ($LASTEXITCODE -ne 0) { throw "docker build failed (exit $LASTEXITCODE)" }

Write-Host "==> OK: built $ImageName"
