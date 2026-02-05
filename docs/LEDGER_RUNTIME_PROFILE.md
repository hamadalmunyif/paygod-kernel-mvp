# Runtime Ledger Profile (Phase 2)

## Purpose
Provide an append-only *runtime* ledger trail **outside git**.
This is NOT the repo proof ledger. Repo outputs remain deterministic and reproducible.

Runtime ledger is meant to support:
- audit trail per run
- traceability to a git commit (HEAD)
- refs-only integrity (hashes) without storing sensitive content

## Enablement
Set the environment variable:

- PAYGOD_LEDGER_PATH = path to a JSONL file (will be created if missing)

When PAYGOD_LEDGER_PATH is set, running:
- tools/run_proof.ps1

will append one JSON line (JSONL) per run by calling:
- tools/append_ledger.ps1

When PAYGOD_LEDGER_PATH is NOT set:
- runtime ledger is disabled (no side effects outside git)

## Format (JSONL)
One line per entry (UTF-8, no BOM). Minimal refs-only record.

Example (single JSON line):
{"v":1,"at_utc":"2026-02-05T22:58:13Z","repo":"https://github.com/<org>/<repo>.git","head":"<git_sha>","decision":{"path":"docs/examples/proof_run/outputs/decision.json","sha256":"<sha256>"},"evidence":{"path":"docs/examples/proof_run/outputs/evidence.json","sha256":"<sha256>"},"ledger_entry":{"path":"docs/examples/proof_run/outputs/ledger_entry.json","sha256":"<sha256>"}}

Fields:
- v: record version (integer)
- at_utc: runtime timestamp (UTC) — allowed because this file is outside git
- repo: remote origin URL (informational)
- head: git commit SHA (traceability)
- decision/evidence/ledger_entry: refs-only paths + SHA256 digests

## Policy (Hard Rules)
- refs-only: never store raw payloads, secrets, or full evidence content
- no PII: never write personal data into runtime ledger
- runtime ledger MUST be outside git (not committed)

## Notes on Time
Repo proof outputs must remain deterministic and reproducible.
Runtime ledger time (at_utc) is permitted because it is:
- outside git
- not part of proof hashing within the repo

## Operational Example
Windows PowerShell:

# disable (default)
Remove-Item Env:\PAYGOD_LEDGER_PATH -ErrorAction SilentlyContinue
pwsh -File tools/run_proof.ps1

# enable
 = "C:\Users\User\Desktop\paygod_runtime_ledger.jsonl"
pwsh -File tools/run_proof.ps1
Get-Content  -Tail 1
