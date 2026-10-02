# Changelog

## Unreleased

### Verification contract repair (v0.5.1)
- Replace the inaccurate `rfc8785` canonicalization claim with the restricted `paygod-c14n-v1` profile.
- Reject decision-critical floats/decimals/exponents, unsafe integers, non-NFC property names, and unsupported values.
- Preserve raw string values without silent Unicode normalization.
- Gate Python and .NET against shared canonicalization acceptance/rejection vectors.
- Separate verification dimensions for integrity, issuer authenticity, replay, and time authority.
- Add `receipt_sha256`, external receipt-digest pinning, verified `ledger_head`, and strict transferred-file membership.
- Align existing decision-critical numeric pack inputs with integer/scaled-integer representation.
- Reframe the next stage as an Internal Verification Challenge and Internal Rehearsal before any external pilot.

### Historical
- Initial scaffold and subsequent deterministic execution, portable evidence, standalone verifier, and repository-boundary work predate formal changelog maintenance. Git history remains the source of record for those merged changes.
