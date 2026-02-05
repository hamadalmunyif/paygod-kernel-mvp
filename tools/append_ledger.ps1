# tools/append_ledger.ps1
# Append-only runtime ledger entry (JSONL) - refs-only - OUTSIDE git.

param(
  [Parameter(Mandatory=$true)][string]$DecisionPath,
  [Parameter(Mandatory=$true)][string]$EvidencePath,
  [Parameter(Mandatory=$true)][string]$LedgerEntryPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"


$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Fail([string]$msg) { Write-Error $msg; exit 1 }

$ledgerPath = $env:PAYGOD_LEDGER_PATH
if ([string]::IsNullOrWhiteSpace($ledgerPath)) {
  Fail "PAYGOD_LEDGER_PATH is not set. Refusing to write runtime ledger."
}

function NormPath([string]$p) {
  return ($p -replace '\\','/')
}

function Sha256File([string]$p) {
  if (-not (Test-Path $p)) { Fail "Missing file: $p" }
  return (Get-FileHash -Algorithm SHA256 -Path $p).Hash.ToLowerInvariant()
}

$decisionHash = Sha256File $DecisionPath
$evidenceHash = Sha256File $EvidencePath
$entryHash    = Sha256File $LedgerEntryPath

$dir = Split-Path -Parent $ledgerPath
if (-not [string]::IsNullOrWhiteSpace($dir)) {
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

$rec = [ordered]@{
  v = 1
  at_utc = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ", [System.Globalization.CultureInfo]::InvariantCulture)
  repo = (git config --get remote.origin.url)
  head = (git rev-parse HEAD)
  decision     = [ordered]@{ path = (NormPath $DecisionPath);     sha256 = $decisionHash }
  evidence     = [ordered]@{ path = (NormPath $EvidencePath);     sha256 = $evidenceHash }
  ledger_entry = [ordered]@{ path = (NormPath $LedgerEntryPath);  sha256 = $entryHash }
}

$line = ($rec | ConvertTo-Json -Depth 10 -Compress)
[System.IO.File]::AppendAllText($ledgerPath, $line + "`n", $utf8NoBom)

Write-Host "OK: appended runtime ledger entry -> $ledgerPath"
exit 0