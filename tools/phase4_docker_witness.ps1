Param(
  [string]$ImageName = "paygod/runner:dev",
  [string]$PackPath  = "packs/core/secrets-in-repo-guard",
  [string]$Clock     = "2026-02-15T00:00:00Z"
)

$ErrorActionPreference = "Stop"

function New-CleanDir([string]$Path) {
  if (Test-Path $Path) { Remove-Item -Recurse -Force $Path }
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function Get-RelativePath([string]$Base, [string]$Full) {
  $baseFull = (Resolve-Path $Base).Path.TrimEnd('\')
  $fullPath = (Resolve-Path $Full).Path
  if (-not $fullPath.StartsWith($baseFull, [System.StringComparison]::OrdinalIgnoreCase)) { return $Full }
  $rel = $fullPath.Substring($baseFull.Length).TrimStart('\')
  return $rel -replace '\\','/'
}

function Should-IgnorePath([string]$RelPath) {
  $p = $RelPath.ToLowerInvariant()
  if ($p -match '(^|/)_meta(/|$)') { return $true }
  if ($p -match '(^|/)run-metadata(/|$)') { return $true }
  if ($p.EndsWith(".log")) { return $true }
  if ($p.EndsWith(".tmp")) { return $true }
  if ($p.EndsWith(".bak")) { return $true }
  return $false
}

# PS5.1: ConvertFrom-Json returns PSCustomObject => must handle [psobject]
function Normalize-JsonObject($obj) {
  if ($null -eq $obj) { return $null }

  # Arrays / lists
  if ($obj -is [System.Collections.IList]) {
    for ($i=0; $i -lt $obj.Count; $i++) {
      $obj[$i] = Normalize-JsonObject $obj[$i]
    }
    return $obj
  }

  # Hashtable / Dictionary
  if ($obj -is [System.Collections.IDictionary]) {
    foreach ($k in @("generated_at","timestamp","record_hash")) {
      if ($obj.Contains($k)) { $obj.Remove($k) }
    }
    foreach ($k in @($obj.Keys)) {
      $obj[$k] = Normalize-JsonObject $obj[$k]
    }
    return $obj
  }

  # PSCustomObject / PSObject
  if ($obj -is [psobject]) {
    foreach ($k in @("generated_at","timestamp","record_hash")) {
      $p = $obj.PSObject.Properties[$k]
      if ($null -ne $p) { $obj.PSObject.Properties.Remove($k) }
    }

    foreach ($p in @($obj.PSObject.Properties)) {
      $obj.$($p.Name) = Normalize-JsonObject $p.Value
    }
    return $obj
  }

  return $obj
}

function Get-NormalizedFileText([string]$FilePath, [string]$RelPath) {
  $rp = $RelPath.ToLowerInvariant()

  if ($rp.EndsWith(".json")) {
    $raw = Get-Content -Raw -Path $FilePath
    $obj = $raw | ConvertFrom-Json
    $obj = Normalize-JsonObject $obj
    return ($obj | ConvertTo-Json -Compress)
  }

  if ($rp.EndsWith(".jsonl")) {
    $lines = Get-Content -Path $FilePath
    $outLines = foreach ($line in $lines) {
      if ([string]::IsNullOrWhiteSpace($line)) { continue }
      $obj = $line | ConvertFrom-Json
      $obj = Normalize-JsonObject $obj
      ($obj | ConvertTo-Json -Compress)
    }
    return ($outLines -join "`n")
  }

  return (Get-Content -Raw -Path $FilePath)
}

function Get-TextSha256([string]$Text) {
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  return (($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join "")
}

function Get-OutDigest([string]$OutDir) {
  $files = Get-ChildItem -Path $OutDir -Recurse -File | Sort-Object FullName
  $pairs = New-Object System.Collections.Generic.List[string]

  foreach ($f in $files) {
    $rel = Get-RelativePath $OutDir $f.FullName
    if (Should-IgnorePath $rel) { continue }

    $text = Get-NormalizedFileText $f.FullName $rel
    $h = Get-TextSha256 $text
    $pairs.Add("$rel=$h")
  }

  $joined = ($pairs.ToArray() -join "`n")
  $digest = Get-TextSha256 $joined
  return @{ digest=$digest; count=$pairs.Count }
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Write-Host "==> RepoRoot : $repoRoot"
Write-Host "==> Image    : $ImageName"
Write-Host "==> PackPath : $PackPath"
Write-Host "==> Clock    : $Clock"

docker image inspect $ImageName | Out-Null

$tmp = Join-Path $repoRoot "_witness_tmp"
New-CleanDir $tmp
$inputDir = Join-Path $tmp "input"
$out1Dir  = Join-Path $tmp "out1"
$out2Dir  = Join-Path $tmp "out2"
New-Item -ItemType Directory -Force -Path $inputDir,$out1Dir,$out2Dir | Out-Null

$inputJsonPath = Join-Path $inputDir "input.json"
@'
{
  "apiVersion": "belloop.io/v1",
  "kind": "Input",
  "metadata": { "id": "witness-secrets-in-repo-guard", "tenant": "dev", "source": "witness" },
  "spec": { "target": { "type": "repo", "path": "/work" } }
}
'@ | Set-Content -Encoding UTF8 $inputJsonPath

$workMount  = "$($repoRoot.Path):/work:ro"
$packMount  = "$((Resolve-Path (Join-Path $repoRoot $PackPath)).Path):/pack:ro"
$inputMount = "$((Resolve-Path $inputJsonPath).Path):/input/input.json:ro"

function Invoke-Run([string]$OutDir) {
  $outMount = "$((Resolve-Path $OutDir).Path):/out"

  $help = docker run --rm $ImageName run --help 2>&1 | Out-String
  $supportsClock = ($help -match "--clock")

  $cmd = @(
    "run","--rm","--network","none",
    "-v",$workMount,
    "-v",$packMount,
    "-v",$inputMount,
    "-v",$outMount,
    $ImageName,
    "run","--pack","/pack","--input","/input/input.json","--out","/out"
  )

  if ($supportsClock) {
    $cmd += @("--clock",$Clock)
  }

  Write-Host "==> docker $($cmd -join ' ')"
  docker @cmd
  if ($LASTEXITCODE -ne 0) { throw "Runner failed (exit $LASTEXITCODE)" }
}

Write-Host "==> Run #1"
Invoke-Run $out1Dir
Write-Host "==> Run #2"
Invoke-Run $out2Dir

Write-Host "==> Hashing outputs (with exclusions + normalized time fields)"
$d1 = Get-OutDigest $out1Dir
$d2 = Get-OutDigest $out2Dir

Write-Host ("==> out1 files counted: {0}" -f $d1.count)
Write-Host ("==> out2 files counted: {0}" -f $d2.count)
Write-Host ("==> out1 digest: {0}" -f $d1.digest)
Write-Host ("==> out2 digest: {0}" -f $d2.digest)

if ($d1.digest -ne $d2.digest) { throw "WITNESS FAIL" }
Write-Host "==> PASS: deterministic outputs match"

