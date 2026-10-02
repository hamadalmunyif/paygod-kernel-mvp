# Changelog

## Unreleased

### Verification contract repair (v0.5.1)
- replace the inaccurate `rfc8785` declaration with restricted `paygod-c14n-v1`;
- fail closed on floats/decimals, unsafe integers, non-NFC property names, and unsupported canonical values;
- preserve raw string values without silent NFC normalization;
- expose verification dimensions for integrity, issuer authenticity, replay, and time authority;
- add external `receipt.json` SHA-256 pinning;
- expose the verified ledger head;
- reject unexpected transferred files/symlinks;
- migrate decision-critical example packs away from floating-point inputs;
- prepare the repository for an Internal Rehearsal before any external pilot.
