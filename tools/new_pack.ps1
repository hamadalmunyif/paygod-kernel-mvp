param(
  [Parameter(Mandatory=$true)]
  [string]$Name,

  [ValidateSet("core","providers","drafts")]
  [string]$Category = "core"
)

$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path ".").Path
$template = Join-Path $repoRoot "packs\_template\pack"

if (!(Test-Path $template)) {
  Write-Error "Template not found: $template"
}

switch ($Category) {
  "core"      { $destRoot = Join-Path $repoRoot "packs\core" }
  "providers" { $destRoot = Join-Path $repoRoot "packs\providers" }
  "drafts"    { $destRoot = Join-Path $repoRoot "packs\_drafts" }
}

$dest = Join-Path $destRoot $Name

if (Test-Path $dest) {
  Write-Error "Destination already exists: $dest"
}

Copy-Item -Recurse -Force $template $dest

# Replace template name in pack.yaml
$packPath = Join-Path $dest "pack.yaml"
$content = Get-Content $packPath -Raw -Encoding UTF8
$content = $content -replace "name:\s*pack-name-here", ("name: " + $Name)
Set-Content -Path $packPath -Value $content -Encoding UTF8

Write-Host "Created pack: $dest"
Write-Host "Next:"
Write-Host "  python tools/pack_validate.py"
