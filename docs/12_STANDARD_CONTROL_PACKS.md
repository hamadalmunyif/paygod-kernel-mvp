# Standard Control Packs (ISO pattern)

A *Standard Control Pack* maps a policy pack to an external standard (e.g. ISO).

## Why
- Makes compliance executable (controls-as-code)
- Produces reproducible proof outputs (plan/findings/truth ledger)
- Enables community contribution per control

## Required fields
In `spec.standard`:
- `name` (e.g. ISO/IEC 27001:2022)
- `controls[]` (id, title, intent)

## Example
See: `packs/core/iso27001-policy-review`
