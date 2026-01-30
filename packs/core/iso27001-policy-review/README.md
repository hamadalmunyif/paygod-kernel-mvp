# ISO/IEC 27001:2022 A.5.1 — Policy Review (Community Pack)

This pack demonstrates a **Standard Control Pack** pattern.

## Control
- ISO/IEC 27001:2022 — **A.5.1 Policies for information security**

## Pain this solves
Organizations often have policies but fail audits because:
- there is no traceable evidence of approval/review, or
- reviews are overdue without visibility.

## Inputs
`policy_inventory.policies[]` with:
- `required` (boolean)
- `last_reviewed_days` (number) — computed upstream
- `evidence_refs[]` (references-only)

## Decisions
- `deny` if required policy lacks evidence or is overdue (> 365 days)
- `flag` if review is approaching deadline (180–365 days)

## Run tests
```bash
dotnet run --project src/PayGod.Cli -- test --pack packs/core/iso27001-policy-review
```
