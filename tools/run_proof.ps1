# tools/run_proof.ps1
# Phase 2 - STEP 3: Deterministic proof_run runner (no new contracts).
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Fail([string]$msg) { Write-Error $msg; exit 1 }

if (-not (Test-Path ".git")) { Fail "Run from repository root." }

$base   = "docs/examples/proof_run"
$okIn   = Join-Path $base "input.envelope.json"
$badIn  = Join-Path $base "failures/fail.raw_payload.json"
$outDir = Join-Path $base "outputs"

if (-not (Test-Path $okIn))  { Fail "Missing: $okIn" }
if (-not (Test-Path $badIn)) { Fail "Missing: $badIn" }
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

# --- Load JSON ---
try { $ok  = Get-Content $okIn  -Raw | ConvertFrom-Json } catch { Fail "Invalid JSON: $okIn" }
try { $bad = Get-Content $badIn -Raw | ConvertFrom-Json } catch { Fail "Invalid JSON: $badIn" }

# --- Policy: refs-only (StrictMode-safe) ---
function Has-Prop([object]$o, [string]$name) {
  return ($null -ne $o.PSObject.Properties[$name])
}
function Get-Prop([object]$o, [string]$name) {
  $p = $o.PSObject.Properties[$name]
  if ($null -eq $p) { return $null }
  return $p.Value
}

# Negative case MUST have raw_payload
if (Has-Prop $bad "raw_payload" -and $null -ne (Get-Prop $bad "raw_payload")) {
  Write-Host "OK: negative case has raw_payload (expected)."
} else {
  Fail "Negative case missing raw_payload (expected to violate)."
}

# Positive case MUST NOT have raw_payload
if (Has-Prop $ok "raw_payload" -and $null -ne (Get-Prop $ok "raw_payload")) {
  Fail "Positive input contains raw_payload (forbidden)."
}

# Positive case MUST have evidence_refs with at least 1 item
if (-not (Has-Prop $ok "evidence_refs")) { Fail "Positive input missing evidence_refs." }
$e = Get-Prop $ok "evidence_refs"
if ($null -eq $e -or $e.Count -lt 1) { Fail "Positive input missing evidence_refs." }

# --- Deterministic timestamp (UTC, invariant) ---
# --- Reproducible proof time (bit-for-bit) ---
# Priority:
# 1) input.timestamp
# 2) env:PAYGOD_PROOF_TIME
# 3) fixed default (1970-01-01)
function Get-ProofTime([object]$okObj) {
  if ($null -ne $okObj.PSObject.Properties["timestamp"]) {
    $t = $okObj.PSObject.Properties["timestamp"].Value
    if (-not [string]::IsNullOrWhiteSpace($t)) { return $t }
  }
  if (-not [string]::IsNullOrWhiteSpace($env:PAYGOD_PROOF_TIME)) {
    return $env:PAYGOD_PROOF_TIME
  }
  return "1970-01-01T00:00:00Z"
}

$utc = Get-ProofTime $ok

# --- Build outputs (Phase 2 placeholders -> deterministic) ---
$decisionObj = [ordered]@{
  decision  = "ALLOW"
  reason    = "deterministic proof_run: refs-only input accepted"
  pack      = "packs/core/bap-output-validator-guard"
  timestamp = $utc
}

$evidenceObj = [ordered]@{
  evidence = @(
    [ordered]@{
      ref      = $ok.evidence_refs[0].ref
      hash_alg = "sha256"
      note     = "refs-only; no raw payload; no PII"
    }
  )
}

$ledgerObj = [ordered]@{
  entry_index   = 0
  timestamp     = $utc
  previous_hash = ("0" * 64)
  record_hash   = ("0" * 64)
  data_ref      = "outputs/decision.json"
}

# --- Write UTF-8 no BOM ---
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
function Write-Utf8NoBom([string]$p, [object]$o) {
  $json = ($o | ConvertTo-Json -Depth 10)
  [System.IO.File]::WriteAllText($p, $json + "`n", $utf8NoBom)
}

$decisionPath = Join-Path $outDir "decision.json"
$evidencePath = Join-Path $outDir "evidence.json"
$ledgerPath   = Join-Path $outDir "ledger_entry.json"

Write-Utf8NoBom $decisionPath $decisionObj
Write-Utf8NoBom $evidencePath $evidenceObj
Write-Utf8NoBom $ledgerPath   $ledgerObj

# --- Verify writes ---
foreach ($p in @($decisionPath,$evidencePath,$ledgerPath)) {
  if (-not (Test-Path $p)) { Fail "Write failed (missing): $p" }
  if ((Get-Item $p).Length -lt 10) { Fail "Write failed (too small): $p" }
}

Write-Host "OK: Step 3 proof_run generated outputs in $outDir"
exit 0