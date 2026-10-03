# Gas Site Readiness — Synthetic Internal Rehearsal v0.1

This directory is **not a production gas-compliance pack** and does not certify regulatory compliance.

Its purpose is to exercise a complete Paygod decision workflow before any design-partner pilot:

```text
synthetic site evidence
        ↓
mechanical checklist baseline
        ↓
Paygod policy execution
        ↓
READY / HOLD / REJECT mapping
        ↓
receipt + ledger + manifest
        ↓
independent integrity verification
```

## External source boundary

The requirement categories are derived from the public Saudi Civil Defense engineering-services guidance for central LPG/gas systems:

https://998.gov.sa/Ar/Page/SafetyInstForEngServices/web/Safety/SafetyInstructionList/

The rehearsal references clauses 4-12/10/4/3 and 4-12/11/1 through 4-12/11/5 for categories such as isolation valves, pre-operation coordination, pressure testing, fire-protection readiness, warning signage, and leak detection/automatic shutoff.

**The source does not define Paygod's READY/HOLD/REJECT labels.** Those labels are deliberately an internal test policy so we can pressure-test evidence sufficiency and fail-closed behavior.

## Outcome mapping

- Paygod `allow` → **READY**
- Paygod `flag` → **HOLD**
- Paygod `deny` → **REJECT**

A subject/site identifier mismatch is also REJECT in this rehearsal.

## B1 data

B1 contains 30 engineering cases:

- 10 curated source-derived synthetic decision cases;
- 10 deterministic generated combinations after the policy is fixed;
- 10 adversarial cases against input canonicalization, bundle integrity, decision binding, and external receipt commitment.

It contains:

- **0 real historical cases**;
- **0 independent human judgments**.

Therefore B1 can only reach `engineering_ready_for_real_cases`. It cannot close the full Internal Rehearsal in #70.

## Baseline

A separate mechanical checklist oracle in `tools/run_gas_site_readiness_rehearsal.py` evaluates the same evidence without parsing the pack expression.

This provides implementation separation but not human independence.

## Run

After publishing the CLI:

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
python tools/run_gas_site_readiness_rehearsal.py \
  --cli ./out/PayGod.Cli \
  --pack rehearsals/gas-site-readiness \
  --result gas-site-readiness-rehearsal-result.json
```

Success means the engineering pipeline is ready to accept real/de-identified cases next. It does not mean market demand, regulatory approval, or external-pilot success.
