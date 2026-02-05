# tools/new_handover.ps1
# Phase 2 - STEP 1: Generate docs/HANDOVER.md (UTF-8 no BOM), locked to baseline commit.
# Run from repo root: pwsh -File tools/new_handover.ps1

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-GitValue([string]$cmd) {
  $v = & git @($cmd.Split(' ')) 2>$null
  if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($v)) {
    throw "Git command failed: git $cmd"
  }
  return $v.Trim()
}

# --- Guards ---
if (-not (Test-Path ".git")) { throw "Run this from the repository root ('.git' not found)." }

$baselineCommit = "1b6be2e"
$headCommitFull = Get-GitValue "rev-parse HEAD"
$headCommitShort = Get-GitValue "rev-parse --short HEAD"
$branch = Get-GitValue "rev-parse --abbrev-ref HEAD"
$originUrl = ""
try { $originUrl = (Get-GitValue "remote get-url origin") } catch { $originUrl = "(no origin remote)" }

if ($branch -ne "main") {
  throw "Direction Lock violation: current branch is '$branch'. You must be on 'main'."
}

if ($headCommitFull -notlike "$baselineCommit*") {
  throw "Baseline mismatch: HEAD is '$headCommitShort' but must start with '$baselineCommit'. Aborting."
}

# Ensure clean working tree (no drift)
$porcelain = & git status --porcelain
if ($LASTEXITCODE -ne 0) { throw "git status failed." }

# Normalize output to a single string (handles both array and scalar cases)
$porcelainText = ($porcelain | Out-String).Trim()

# Allow exactly ONE untracked file: tools/new_handover.ps1 (this script).
# Anything else must be clean.
if (-not [string]::IsNullOrWhiteSpace($porcelainText)) {
  $lines = $porcelainText -split "`r?`n" | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
  $allowed = @("?? tools/new_handover.ps1", "?? tools\new_handover.ps1")

  $unexpected = @($lines | Where-Object { $allowed -notcontains $_ })
  if ($unexpected.Length -gt 0) {
    throw "Working tree not clean. Unexpected changes:`n$($unexpected -join "`n")"
  }
}

# --- Build content ---
$utcNow = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# NOTE: use ASCII '-' instead of '—' to avoid mojibake in some Windows console/codepage setups.
$handover = @"
# Paygod Kernel MVP - Phase 1 Closed Handover

## Direction Lock (Non-Negotiable)

- Phase 1: **CLOSED** at baseline commit $baselineCommit
- Baseline branch: **main only**
- Canonical Truth:
  - contracts/ = Law
  - docs/ = Literal reflection of contracts (no opinion)
  - CI = Execution gate / enforcement
- No re-interpretation of Phase 1 decisions is allowed.

## Repository Snapshot (as generated)

- Repository (origin): $originUrl
- Branch: $branch
- Baseline Commit: $headCommitShort
- Generated At (UTC): $utcNow

## What is Locked

- Contracts-first baseline at $baselineCommit
- BAP + Envelope contract alignment
- Schema governance (hash source-of-truth = Git HEAD blobs)
- CI as the enforcement mechanism

## What is NOT Implemented Yet (Explicitly Out of Phase 1)

- Persistent services
- External APIs
- Runtime ledger infrastructure
- Multi-pack composition engine

## Phase 2 Entrypoint (Single Goal)

Ship **one deterministic Proof Run** using:
- packs/core/bap-output-validator-guard

Outputs must be verifiable and enforced by CI:
- decision
- evidence (refs-only; no raw payload; no PII)
- ledger_entry (hash-chained)

## Phase 2 Composition Rule (Law-only, no implementation yet)

Phase 2 early execution uses **single-pack authority**.
Multi-pack composition deferred.
Future default: **deny-wins + reason aggregation**.
"@

# --- Write file (UTF-8 no BOM) ---
New-Item -ItemType Directory -Force -Path "docs" | Out-Null
$path = Join-Path (Get-Location) "docs/HANDOVER.md"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $handover, $utf8NoBom)

Write-Host "OK: generated docs/HANDOVER.md locked to baseline $baselineCommit at HEAD $headCommitShort"
Write-Host "Next: git add docs/HANDOVER.md tools/new_handover.ps1 && git commit -m `"docs: fix handover rendering and encoding`""
