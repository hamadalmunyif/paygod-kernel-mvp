# Gates

Workflow configuration remains the source of truth for exact GitHub Actions implementation.

## Main branch merge gates
Changes to `main` must preserve required checks including:
- **Paygod Kernel CI** — build/test baseline.
- **Paygod CI Enforcement** — deterministic witness/proof enforcement.
- **Security Gate** — security checks.
- **Pack Contract Gate** — governed pack contract validation.

## Evidence/portability witnesses
- **Portable Evidence Witness:** artifact handoff, independent verification, fail-closed tamper rejection.
- **Standalone Third-Party Verifier Witness:** standalone transferred verifier, no repository checkout, no original pack replay, clean -> `VALID`, one-byte tamper -> `INVALID`.

These establish the documented CI trust boundary, not external real-world fact truth.

## Architecture gate
Before changing frozen kernel primitives, a PR must explain why the requirement cannot be implemented through a contract, pack, adapter, or explicitly versioned interface.

Frozen-by-default primitives are documented in `docs/ARCHITECTURE_AUDIT.md`.

## Documentation gate
`README.md` is the public contract and `START_HERE.md` is the developer entry point.

A PR that materially changes what Paygod is, a proven guarantee, the canonical trust path, required gates, or the supported developer workflow must update the relevant documentation in the same change.

Roadmap items must not be presented as proven guarantees.
