# Architectural Boundaries


**Document status (2026-10-11):** HISTORICAL REPOSITORY SEPARATION SUMMARY — not the definitive current authority contract.  
For current allowed adapter behavior and actual boundary witnesses read REPOSITORY_BOUNDARY.md and GATES.md. An API permitted to change is not permitted to mint a canonical verdict, receipt, manifest or bundle identity.  
Current claim baseline: [Verified Claims Register](CLAIMS_REGISTER.md).

## Kernel repository
Repository: `paygod-kernel-mvp`

Do **NOT** modify:
- `contracts`
- `spec`
- canonicalization rules
- deterministic execution rules

## Cloud starter repository
Repository: `paygod-cloud-starter`

Allowed changes:
- API
- documentation
- tests
- orchestration
