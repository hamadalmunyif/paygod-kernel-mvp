# Pull Request

## Summary
What does this change do and why?

## Motivation
What problem does this solve? Any risk to determinism, artifacts, authority boundaries, or CI enforcement?

## Type of change
- [ ] Determinism-related change
- [ ] Pack logic update
- [ ] Contract / Schema change
- [ ] CI enforcement update
- [ ] Adapter / execution-surface change
- [ ] Documentation only
- [ ] Refactor (no functional change)

## Determinism impact
- [ ] Preserves bit-for-bit determinism
- [ ] Changes canonicalization logic
- [ ] Alters artifact structure
- [ ] Requires witness update

Explain any digest behavior change (if any).

## Evidence / artifact impact
- [ ] No artifact format changes
- [ ] Artifact envelope updated
- [ ] Schema version bumped (SemVer): ____

## Repository authority boundary
- [ ] This change does not add or modify an execution-facing adapter.
- [ ] If it does: the adapter is registered in `tools/check_repository_boundary.py`.
- [ ] If it does: the adapter delegates to the Canonical Kernel or fails closed.
- [ ] If it does: the mutation witness covers local verdict, receipt, and bundle-identity authority.
- [ ] No non-kernel component originates canonical decision, receipt, manifest, policy, or bundle-identity semantics.

Explain any new execution-facing surface and why it cannot become an alternate authority.

## Testing
- [ ] Witness double-run PASS (strict)
- [ ] Pack contract gate PASS
- [ ] Repository Boundary Gate PASS
- [ ] CI checks PASS

**Env**
.NET:
OS:
Docker:
PowerShell:
