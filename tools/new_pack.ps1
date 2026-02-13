param(
  [Parameter(Mandatory=$true)]
  [ValidateNotNullOrEmpty()]
  [string]$Name,

  [ValidateSet("core","providers","drafts")]
  [string]$Category = "core"
)

$ErrorActionPreference = "Stop"

$repoRoot  = (Resolve-Path ".").Path
$template  = Join-Path $repoRoot "packs\_template\pack"

if (!(Test-Path $template)) {
  Write-Error "Template not found: $template"
}

switch ($Category) {
  "core"      { $destRoot = Join-Path $repoRoot "packs\core" }
  "providers" { $destRoot = Join-Path $repoRoot "packs\providers" }
  "drafts"    { $destRoot = Join-Path $repoRoot "packs\_drafts" }
}

New-Item -ItemType Directory -Force $destRoot | Out-Null

$dest = Join-Path $destRoot $Name
if (Test-Path $dest) {
  Write-Error "Destination already exists: $dest"
}

New-Item -ItemType Directory -Force $dest | Out-Null

Copy-Item -Path (Join-Path $template "*") -Destination $dest -Recurse -Force

$packPath = Join-Path $dest "pack.yaml"
if (!(Test-Path $packPath)) {
  Write-Error "pack.yaml not found after copy: $packPath"
}

$content = Get-Content $packPath -Raw -Encoding UTF8
$content = $content -replace "name:\s*pack-name-here", ("name: " + $Name)
Set-Content -Path $packPath -Value $content -Encoding UTF8

Write-Host "Created pack: $dest"
Write-Host "Next:"
Write-Host "  python tools/pack_validate.py"
