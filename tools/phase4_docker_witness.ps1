Param(
  [ValidateSet("strict","canonical")]
  [string]$Mode = "strict",
  [string]$ImageName = "paygod/runner:dev",
  [string]$PackPath  = "packs/core/secrets-in-repo-guard",
  [string]$Clock     = "2026-02-15T00:00:00Z"
)

$ErrorActionPreference = "Stop"

# ============================================================
# Utility Helpers
# ============================================================

function New-CleanDir([string]$Path) {
  if (Test-Path $Path) { Remove-Item -Recurse -Force $Path }
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
}

function Get-RelativePath([string]$Base, [string]$Full) {
  $baseFull = (Resolve-Path $Base).Path
  $fullPath = (Resolve-Path $Full).Path
  $baseNorm = $baseFull.Replace('\','/').TrimEnd('/')
  $fullNorm = $fullPath.Replace('\','/')
  if (-not $fullNorm.StartsWith($baseNorm, [System.StringComparison]::OrdinalIgnoreCase)) { return $Full }
  return $fullNorm.Substring($baseNorm.Length).TrimStart('/')
}

function Should-IgnorePath([string]$RelPath) {
  $p = $RelPath.Replace('\','/').ToLowerInvariant()
  if ($p -match '(^|/)_meta(/|$)') { return $true }
  if ($p -match '(^|/)run-metadata(/|$)') { return $true }
  if ($p.EndsWith(".log")) { return $true }
  if ($p.EndsWith(".tmp")) { return $true }
  if ($p.EndsWith(".bak")) { return $true }
  return $false
}

# ============================================================
# Canonical JSON Helpers (Single Definition Only)
# ============================================================

function Canonicalize-JsonValue($value) {
  if ($null -eq $value) { return $null }

  if ($value -is [System.Collections.IEnumerable] -and
      -not ($value -is [string]) -and
      -not ($value -is [System.Collections.IDictionary])) {
    $arr = @()
    foreach ($item in $value) { $arr += (Canonicalize-JsonValue $item) }
    return ,$arr
  }

  if ($value -is [System.Collections.IDictionary]) {
    $out = [ordered]@{}
    $keys = @($value.Keys) | ForEach-Object { "$_" } | Sort-Object
    foreach ($k in $keys) { $out[$k] = Canonicalize-JsonValue $value[$k] }
    return $out
  }

  if ($value -is [psobject] -and -not ($value -is [string])) {
    $out = [ordered]@{}
    $props = @($value.PSObject.Properties.Name) | Sort-Object
    foreach ($name in $props) { $out[$name] = Canonicalize-JsonValue $value.$name }
    return $out
  }

  return $value
}

function Normalize-JsonObject($obj) {
  if ($null -eq $obj) { return $null }

  if ($obj -is [System.Collections.IDictionary]) {
    foreach ($k in @("generated_at","timestamp","record_hash")) {
      if ($obj.ContainsKey($k)) { $obj.Remove($k) }
    }
    foreach ($k in @($obj.Keys)) { $obj[$k] = Normalize-JsonObject $obj[$k] }
    return $obj
  }

  if ($obj -is [psobject] -and -not ($obj -is [string])) {
    foreach ($k in @("generated_at","timestamp","record_hash")) {
      $p = $obj.PSObject.Properties[$k]
      if ($null -ne $p) { $obj.PSObject.Properties.Remove($k) }
    }
    foreach ($p in @($obj.PSObject.Properties)) {
      $obj.($p.Name) = Normalize-JsonObject $p.Value
    }
    return $obj
  }

  if ($obj -is [System.Collections.IEnumerable] -and -not ($obj -is [string])) {
    for ($i=0; $i -lt $obj.Count; $i++) {
      $obj[$i] = Normalize-JsonObject $obj[$i]
    }
    return $obj
  }

  return $obj
}

function ConvertTo-CanonicalJson([string]$RawJson) {
  try { $obj = $RawJson | ConvertFrom-Json -AsHashtable }
  catch { $obj = $RawJson | ConvertFrom-Json }
  $obj = Normalize-JsonObject $obj
  $canon = Canonicalize-JsonValue $obj
  return ($canon | ConvertTo-Json -Compress -Depth 100)
}

function Get-TextSha256([string]$Text) {
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  return (($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join "")
}

function Get-NormalizedFileText([string]$FilePath, [string]$RelPath) {
  $rp = $RelPath.Replace('\','/').ToLowerInvariant()

  if ($rp.EndsWith(".json")) {
    $raw = Get-Content -Raw -Path $FilePath -Encoding UTF8
    return (ConvertTo-CanonicalJson $raw)
  }

  if ($rp.EndsWith(".jsonl")) {
    $lines = Get-Content -Path $FilePath -Encoding UTF8
    $outLines = foreach ($line in $lines) {
      if ([string]::IsNullOrWhiteSpace($line)) { continue }
      (ConvertTo-CanonicalJson $line)
    }
    return ($outLines -join "`n")
  }

  return (Get-Content -Raw -Path $FilePath -Encoding UTF8)
}

# ============================================================
# Digest Logic
# ============================================================

function Get-OutDigest([string]$OutDir) {
  $files = Get-ChildItem -Path $OutDir -Recurse -File | Sort-Object FullName
  $pairs = New-Object System.Collections.Generic.List[string]
  $map = @{}

  foreach ($f in $files) {
    $rel = Get-RelativePath $OutDir $f.FullName
    if (Should-IgnorePath $rel) { continue }

    $text = Get-NormalizedFileText $f.FullName $rel
    $h = Get-TextSha256 $text

    $pairs.Add("$rel=$h")
    $map[$rel] = @{
      hash  = $h
      text  = $text
      bytes = ([System.Text.Encoding]::UTF8.GetByteCount($text))
    }
  }

  $joined = ($pairs.ToArray() -join "`n")
  $digest = Get-TextSha256 $joined

  return @{
    digest = $digest
    count  = $pairs.Count
    map    = $map
  }
}

function Get-CanonicalWitness([string]$OutDir) {

  $files = Get-ChildItem -Path $OutDir -Recurse -File | Sort-Object FullName
  $map = @{}

  foreach ($f in $files) {
    $rel = Get-RelativePath $OutDir $f.FullName
    if (Should-IgnorePath $rel) { continue }
    if ($rel.ToLowerInvariant() -eq "manifest.json") { continue }

    $text = Get-NormalizedFileText $f.FullName $rel
    $h = Get-TextSha256 $text

    $map[$rel] = @{
      hash  = $h
      text  = $text
      bytes = ([System.Text.Encoding]::UTF8.GetByteCount($text))
    }
  }

  if (-not $map.ContainsKey("plan.json")) { throw "Missing plan.json" }

  $plan = $map["plan.json"].text | ConvertFrom-Json
  $pack = $plan.pack
  $inputCanon = $plan.input.canonical_hash

  $expected = @("findings.json","ledger.jsonl","plan.json")
  foreach ($e in $expected) {
    if (-not $map.ContainsKey($e)) { throw "Missing expected file: $e" }
  }

  $fileEntries = foreach ($name in $expected) {
    [ordered]@{
      name   = $name
      bytes  = $map[$name].bytes
      sha256 = $map[$name].hash
    }
  }

  $sorted = $fileEntries | Sort-Object name
  $lines = $sorted | ForEach-Object { "$($_.name)=$($_.sha256)" }
  $bundleDigest = Get-TextSha256 ($lines -join "`n")

  $canonManifest = [ordered]@{
    api_version = "paygod/v1"
    kind = "Manifest"
    input = @{ canonical_hash = $inputCanon }
    pack  = @{
      name = $pack.name
      version = $pack.version
      path = $pack.path
      digest_sha256 = $pack.digest_sha256
    }
    files = $sorted
    bundle = @{
      algorithm = "sha256"
      file_count = $sorted.Count
      bundle_digest = $bundleDigest
    }
  }

  $canonJson = ($canonManifest | ConvertTo-Json -Compress -Depth 100)
  $canonHash = Get-TextSha256 $canonJson

  return @{
    canon_manifest_hash = $canonHash
    canon_manifest_json = $canonJson
  }
}

# ============================================================
# Main Execution
# ============================================================

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
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
  "metadata": { "id": "witness", "tenant": "dev" },
  "spec": { "target": { "type": "repo", "path": "/work" } }
}
'@ | Set-Content -Encoding UTF8 $inputJsonPath

$workHost  = (Resolve-Path $repoRoot).Path
$packHost  = (Resolve-Path (Join-Path $repoRoot $PackPath)).Path
$inputHost = (Resolve-Path $inputJsonPath).Path

$userArgs = @()
if ($IsLinux) {
  $uid = (& /usr/bin/id -u).Trim()
  $gid = (& /usr/bin/id -g).Trim()
  $userArgs = @("--user","${uid}:${gid}")
}

function Invoke-Run([string]$OutDir) {

  $outHostPath = (Resolve-Path $OutDir).Path
  $help = docker run --rm $ImageName run --help 2>&1 | Out-String
  $supportsClock = ($help -match "--clock")

  $cmd = @("run","--rm","--network","none") + $userArgs + @(
    "-e","PAYGOD_CLOCK=$Clock",
    "-e","PAYGOD_STRICT=1",
    "-e","SOURCE_DATE_EPOCH=0",
    "-v","${workHost}:/work:ro",
    "-v","${packHost}:/pack:ro",
    "-v","${inputHost}:/input/input.json:ro",
    "-v","${outHostPath}:/out:rw",
    $ImageName,
    "run","--pack","/pack","--input","/input/input.json","--out","/out"
  )

  if ($supportsClock) {
    $cmd += @("--clock",$Clock)
  }

  docker @cmd
  if ($LASTEXITCODE -ne 0) { throw "Runner failed" }
}

Invoke-Run $out1Dir
Invoke-Run $out2Dir

if ($Mode -eq "canonical") {
  $d1 = Get-CanonicalWitness $out1Dir
  $d2 = Get-CanonicalWitness $out2Dir
  if ($d1.canon_manifest_hash -ne $d2.canon_manifest_hash) {
    throw "WITNESS FAIL (canonical)"
  }
  Write-Host "PASS (canonical)"
  exit 0
}

$d1 = Get-OutDigest $out1Dir
$d2 = Get-OutDigest $out2Dir

if ($d1.digest -ne $d2.digest) {
  throw "WITNESS FAIL (strict)"
}

Write-Host "PASS (strict)"