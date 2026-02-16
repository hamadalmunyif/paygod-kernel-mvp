Param(
  [switch]$PruneOut
)

$ErrorActionPreference = "Stop"
$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$compose = Join-Path $repoRoot "deploy\compose\docker-compose.yml"

docker compose -f $compose down

if ($PruneOut) {
  $out = Join-Path $repoRoot "_dev_out"
  if (Test-Path $out) { Remove-Item -Recurse -Force $out }
  New-Item -ItemType Directory -Force -Path $out | Out-Null
  Write-Host "==> pruned: _dev_out"
}

Write-Host "==> DOWN"
