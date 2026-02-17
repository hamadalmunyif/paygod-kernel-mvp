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
  # Cross-platform relative path (Windows/Linux)
  $baseFull = (Resolve-Path $Base).Path
  $fullPath = (Resolve-Path $Full).Path

  # Normalize separators for comparison
  $baseNorm = $baseFull.Replace('\','/').TrimEnd('/')
  $fullNorm = $fullPath.Replace('\','/')

  if (-not $fullNorm.StartsWith($baseNorm, [System.StringComparison]::OrdinalIgnoreCase)) { return $Full }
  $rel = $fullNorm.Substring($baseNorm.Length).TrimStart('/')
  return $rel
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

# ---- Canonical JSON helpers (stable key ordering) ----

function Canonicalize-JsonValue($value) {
  if ($null -eq $value) { return $null }

  # Arrays / lists
  if ($value -is [System.Collections.IEnumerable] -and -not ($value -is [string]) -and -not ($value -is [System.Collections.IDictionary])) {
    $arr = @()
    foreach ($item in $value) {
      $arr += (Canonicalize-JsonValue $item)
    }
    return ,$arr
  }

  # Hashtable / dictionary
  if ($value -is [System.Collections.IDictionary]) {
    $out = [ordered]@{}
    $keys = @($value.Keys) | ForEach-Object { "$_" } | Sort-Object
    foreach ($k in $keys) {
      $out[$k] = Canonicalize-JsonValue $value[$k]
    }
    return $out
  }

  # PSCustomObject / PSObject
  if ($value -is [psobject] -and -not ($value -is [string])) {
    $out = [ordered]@{}
    $props = @($value.PSObject.Properties.Name) | Sort-Object
    foreach ($name in $props) {
      $out[$name] = Canonicalize-JsonValue $value.$name
    }
    return $out
  }

  # Scalars
  return $value
}

function Normalize-JsonObject($obj) {
  if ($null -eq $obj) { return $null }

  # remove volatile fields anywhere they appear (objects only)
  if ($obj -is [System.Collections.IDictionary]) {
    foreach ($k in @("generated_at","timestamp","record_hash")) {
      if ($obj.ContainsKey($k)) { $obj.Remove($k) }
    }
    foreach ($k in @($obj.Keys)) {
      $obj[$k] = Normalize-JsonObject $obj[$k]
    }
    return $obj
  }

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

  if ($obj -is [System.Collections.IEnumerable] -and -not ($obj -is [string])) {
    for ($i=0; $i -lt $obj.Count; $i++) {
      $obj[$i] = Normalize-JsonObject $obj[$i]
    }
    return $obj
  }

  return $obj
}

function ConvertTo-CanonicalJson([string]$RawJson) {
  # Use -AsHashtable when available (pwsh 7+) to avoid PSObject quirks.
  try {
    $obj = $RawJson | ConvertFrom-Json -AsHashtable
  } catch {
    $obj = $RawJson | ConvertFrom-Json
  }

  $obj = Normalize-JsonObject $obj
  $canon = Canonicalize-JsonValue $obj
  return ($canon | ConvertTo-Json -Compress -Depth 100)
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

function Get-TextSha256([string]$Text) {
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  return (($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join "")
}

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
    joined = $joined
  }
}

function Show-WitnessDiff($d1, $d2) {
  $keys = @($d1.map.Keys + $d2.map.Keys) | Sort-Object -Unique

  foreach ($k in $keys) {
    $h1 = $null; $h2 = $null
    if ($d1.map.ContainsKey($k)) { $h1 = $d1.map[$k].hash }
    if ($d2.map.ContainsKey($k)) { $h2 = $d2.map[$k].hash }

    if ($h1 -ne $h2) {
      Write-Host "!! DIFF FILE: $k"
      Write-Host "   out1 hash : $h1"
      Write-Host "   out2 hash : $h2"
      if ($d1.map.ContainsKey($k)) { Write-Host ("   out1 bytes: {0}" -f $d1.map[$k].bytes) }
      if ($d2.map.ContainsKey($k)) { Write-Host ("   out2 bytes: {0}" -f $d2.map[$k].bytes) }

      # Print bounded preview to avoid log explosion
      $max = 4000

      Write-Host "----- out1 normalized (preview) -----"
      if ($d1.map.ContainsKey($k)) {
        $t = $d1.map[$k].text
        if ($t.Length -gt $max) { $t = $t.Substring(0,$max) + "`n...<truncated>..." }
        Write-Host $t
      } else {
        Write-Host "<missing>"
      }

      Write-Host "----- out2 normalized (preview) -----"
      if ($d2.map.ContainsKey($k)) {
        $t = $d2.map[$k].text
        if ($t.Length -gt $max) { $t = $t.Substring(0,$max) + "`n...<truncated>..." }
        Write-Host $t
      } else {
        Write-Host "<missing>"
      }

      return
    }
  }

  Write-Host "!! Digests differ but no per-file diffs found (unexpected)."
}

# ---- Main ----

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

# IMPORTANT: Docker mount strings must avoid PS parsing ambiguity with ":" after variables.
$workHost  = (Resolve-Path $repoRoot).Path
$packHost  = (Resolve-Path (Join-Path $repoRoot $PackPath)).Path
$inputHost = (Resolve-Path $inputJsonPath).Path

$workMount  = "${workHost}:/work:ro"
$packMount  = "${packHost}:/pack:ro"
$inputMount = "${inputHost}:/input/input.json:ro"

# Linux CI: run container as host runner user so it can write mounted /out
$userArgs = @()
if ($IsLinux) {
  $uid = (& /usr/bin/id -u).Trim()
  $gid = (& /usr/bin/id -g).Trim()
  $userArgs = @("--user", "${uid}:${gid}")
  Write-Host "==> Linux runner detected; using container user: ${uid}:${gid}"
}

function Invoke-Run([string]$OutDir) {
  $outHostPath = (Resolve-Path $OutDir).Path

  if ($IsLinux) {
    & /bin/chmod -R 777 $outHostPath 2>$null | Out-Null
  }

  $outMount = "${outHostPath}:/out:rw"

  # Detect whether runner supports --clock (backward compatible)
  $help = docker run --rm $ImageName run --help 2>&1 | Out-String
  $supportsClock = ($help -match "--clock")

  $cmd = @("run","--rm","--network","none") + $userArgs + @(
    "-v",$workMount,
    "-v",$packMount,
    "-v",$inputMount,
    "-v",$outMount,
    $ImageName,
    "run","--pack","/pack","--input","/input/input.json","--out","/out"
  )

  if ($supportsClock) { $cmd += @("--clock",$Clock) }

  Write-Host "==> docker $($cmd -join ' ')"
  docker @cmd
  if ($LASTEXITCODE -ne 0) { throw "Runner failed (exit $LASTEXITCODE)" }
}

Write-Host "==> Run #1"
Invoke-Run $out1Dir

Write-Host "==> Run #2"
Invoke-Run $out2Dir

Write-Host "==> Hashing outputs (with exclusions + canonical JSON)"
$d1 = Get-OutDigest $out1Dir
$d2 = Get-OutDigest $out2Dir

Write-Host ("==> out1 files counted: {0}" -f $d1.count)
Write-Host ("==> out2 files counted: {0}" -f $d2.count)
Write-Host ("==> out1 digest: {0}" -f $d1.digest)
Write-Host ("==> out2 digest: {0}" -f $d2.digest)

if ($d1.digest -ne $d2.digest) {
  Write-Host "==> WITNESS FAIL: digests differ. Showing first differing file (normalized):"
  Show-WitnessDiff $d1 $d2
  throw "WITNESS FAIL"
}

Write-Host "==> PASS: deterministic outputs match"
