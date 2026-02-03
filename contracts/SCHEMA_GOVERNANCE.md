# Schema Governance (Truth Source)

## Policy (Non-negotiable)
- CI computes schema digests from Git `HEAD` blobs only.
- Working tree bytes are NOT a source of truth for schema integrity.

## Developer Workflow (Legal Preview)
- Local tooling MAY compute schema digests from Git `STAGED` (index) and fallback to `HEAD`.
- This enables a legal preview of contract changes before commit, without relying on environment-specific working tree representations (e.g., CRLF/LF, encoding).

## Rationale
This prevents silent contract drift caused by platform/editor line-ending or encoding differences and ensures CI enforcement matches the repository's recorded history.