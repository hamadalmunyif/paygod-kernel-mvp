# GHG Scope 1 & 2 — Pack Readiness Research Gate v0

**Status:** CANDIDATE ADMISSION PROFILE / NOT PRODUCTION-READY / NOT AN EMISSIONS CALCULATOR  
**Reference software:** [Canonical PayGod Kernel](../../../README.md)  
**Pack:** [ghg-scope-1-2-guard](../../../packs/core/ghg-scope-1-2-guard/)  
**Date:** 2026-10-10

## Why this gate exists

The real community Pack evaluates **reference presence** for a *previously calculated* emissions inventory. The canonical `RunCommand` currently hashes representable JSON and evaluates rules; it does **not** apply the input schema embedded in each `pack.yaml` before evaluation.

Consequently, the Pack's three positive/unit fixtures (DENY / FLAG / ALLOW) do not prove that arbitrary external JSON will fail closed before evaluation. Missing measurement fields, wrong types, and absent sources require a distinct admission decision under [ADR 0003](../../../adrs/0003-evidence-admission-before-decision-execution.md).

This is a **separate opt-in pre-kernel research adapter**, not a Kernel feature, universal input validator, or new policy DSL. It never creates `ALLOW`, a receipt, manifest, bundle digest or a second decision engine.

## Boundary and current trade-off

- Reject malformed/duplicate-key/non-UTF-8 input, fractional/exponent numeric values, invalid safe integers, wrong types, missing fields and unknown fields.
- Require a complete set of metadata references for this **shape-only demonstration**. Missing references return `WITHHELD` and `NOT_RUN`, rather than a policy `DENY` or `FLAG`. This is deliberate: the demonstration cannot distinguish *unknown completeness* from *proven absence*. The existing Pack's direct fixture `deny/flag` outcomes still describe deterministic lower-level rules on already admitted facts; those results are not equivalent to end-to-end workflow decisions.
- Retain source bytes' SHA-256 as a **local identity fingerprint**, not a proof of sensor, factor, origin, issuer, or time authenticity. This adapter does not currently create a full referenced Observation Pack.
- A successful shape check reports `SHAPE_PASSED_ONLY`, never "evidence is true". Running the canonical CLI requires explicit `--cli` and `--out`.
- Direct use of the canonical CLI **bypasses this optional wrapper**. No downstream institution may rely on the wrapper as a production security perimeter.
- The pilot profile currently assumes nonnegative integer **kg CO₂e**, with values computed by another validated process. It does not support decimals, removals/negative emissions, recalculation of factors, market/location Scope 2 method selection, source-byte verification, duplicate inventory prevention or emission-factor version authority.
- No independent party has accepted this domain profile; no production claims can be inferred from a green CI run.

## Reproduce shape checks

After `pip install -r tools/requirements.txt`:

```bash
python3 -m unittest discover -s research/pack-readiness/ghg-scope12-v0 -p 'test_*.py' -v
python3 research/pack-readiness/ghg-scope12-v0/admit.py \
  --input research/pack-readiness/ghg-scope12-v0/fixtures/complete-synthetic.json
```

The CLI run and portable integrity check must be performed independently of shape admission and reuse the **canonical** CLI, with a new output directory:

```bash
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
python3 research/pack-readiness/ghg-scope12-v0/admit.py \
  --input research/pack-readiness/ghg-scope12-v0/fixtures/complete-synthetic.json \
  --cli ./out/PayGod.Cli --out /tmp/ghg-bundle
python3 tools/verify_portable_evidence.py /tmp/ghg-bundle \
  --allow-unbound-clock --result /tmp/ghg-verification.json
```

The verifier's result is **bundle integrity** only. `--allow-unbound-clock` explicitly accepts an *unbound* receipt clock for this local demonstration and is not a trusted timestamp.

## Production acceptance conditions — UNMET

| Gate | Needed witness | Current state |
|---|---|---|
| Structural input validation | Invalid/incomplete input refuses orchestration before Kernel | Candidate code and synthetic tests in this research folder; opt-in only |
| Source provenance | Raw real reading and certified/calibrated source identifiers, checks against tampering | NOT PROVEN |
| Calculation profile | Fixed frozen factor version, units, scale, Scope 2 methodology, adjustment and rounding | NOT IMPLEMENTED |
| Semantic completeness | Distinguish known-absent references from unknown/missing observations | NOT PROVEN |
| Kernel path | Admitted real input produces canonical decision and independently verified bundle | Synthetic CI witness proposed; no live institution |
| External acceptance | A second party agrees to a named acceptance profile and verifies without producer service | NOT PROVEN |
| Security integration | All production entrypoints demonstrably enforce admission without bypass | NOT IMPLEMENTED |
| Business use | Measured sign-off cost and an accountable recipient | NOT PROVEN |

The existing [Stop-Build rule](../../../docs/STOP_BUILD_RULE.md) remains active. A domain-specific product or schema can be promoted only through reproducible external evidence and an explicit reviewed record. Until then the website may say **"real executable Pack, research preflight"**, not **"production certified Scope 1/2"**.
