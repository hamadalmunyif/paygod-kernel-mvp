# tools/new_handover.ps1
# Phase 2 - STEP 1: Generate docs/HANDOVER.md (UTF-8 no BOM).
# Baseline commit is a fixed reference (does NOT require HEAD == baseline).
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

if (-not (Test-Path ".git")) { throw "Run this from the repository root ('.git' not found)." }

# Fixed Phase 1 baseline reference (law baseline)
$baselineCommit = "1b6be2e"

# Current repo state (snapshot)
$headCommitShort = Get-GitValue "rev-parse --short HEAD"
$branch          = Get-GitValue "rev-parse --abbrev-ref HEAD"

$originUrl = ""
try { $originUrl = (Get-GitValue "remote get-url origin") } catch { $originUrl = "(no origin remote)" }

if ($branch -ne "main") {
  throw "Direction Lock violation: current branch is '$branch'. You must be on 'main'."
}

# NOTE: We do NOT gate on working tree cleanliness in STEP 1 generator.
# This script is used to create/update HANDOVER.md and may be edited during execution.

$utcNow = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ", [System.Globalization.CultureInfo]::InvariantCulture)

# ASCII-only to avoid mojibake in Windows codepages.
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
- Current HEAD: $headCommitShort
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

New-Item -ItemType Directory -Force -Path "docs" | Out-Null
$path = Join-Path (Get-Location) "docs/HANDOVER.md"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $handover, $utf8NoBom)

Write-Host "OK: generated docs/HANDOVER.md (baseline=$baselineCommit, head=$headCommitShort)"
