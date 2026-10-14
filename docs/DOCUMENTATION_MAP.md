# PayGod public documentation map — current entry points

**Updated 2026-10-14.** This navigation page is descriptive, not a new execution or trust contract. All claimed behavior is limited by the [dated claims register](CLAIMS_REGISTER.md), [Kernel README](../README.md), and the exact recorded CI witnesses.

## Start according to your task

| You want to... | Read / do | What it does **not** promise |
| --- | --- | --- |
| Understand the platform quickly | [Kernel README](../README.md) → [START_HERE](../START_HERE.md) | No complete enterprise or financial service |
| Build your own **private** Pack | [EIK Learn / Build / Verify](eik/README.md) → [Pack contract](../contracts/schemas/pack.schema.json) → [Pack examples](STARTER_PACKS.md) | Neither registration nor upstream contribution is required |
| Let a coding agent assist | [AGENTS.md](../AGENTS.md) → [machine-readable capability snapshot](eik/capabilities.v0.json) | Advisory instructions are not sandbox security or authority |
| Inspect a complete integration example | [Saved synthetic GitHub Actions reference](../examples/eik-github-actions/README.md) → [reference workflow](../.github/workflows/eik-reference.yml) | No live scanner, automated authoring service, or real GitHub source authentication |
| Admit typed inputs before evaluation | [ADR 0003](../adrs/0003-evidence-admission-before-decision-execution.md) → [optional eik_admit.py](../tools/eik_admit.py) | Structural validation does not prove data origin, scan completion or authorization |
| Verify a transferred canonical bundle | [Standalone verifier scope](STANDALONE_VERIFIER.md) → [verifier implementation](../tools/verify_portable_evidence.py) | Integrity is not fact truth, issuer mandate, trusted time or policy replay |
| Propose an optional public contribution | [CONTRIBUTING.md](../CONTRIBUTING.md) → [GATES.md](../GATES.md) | A merged Pack is not production certification or a promise of payment |
| Evaluate what is planned | [ROADMAP.md](../ROADMAP.md) → [current EIK evidence status](eik/STATUS_2026-10-14.md) | A planned feature is not shipped capacity |

## The single-authority boundary

```text
Permitted external source / saved observation
    -> domain-specific pre-Kernel admission (WITHHELD / NOT RUN if mandatory facts missing)
    -> existing canonical Kernel evaluates a versioned Pack
    -> Kernel-generated decision + receipt + manifest + ledger + portable bundle
    -> independent recipient checks bounded integrity, authenticity only if explicitly configured
```

The source/system owner alone authorizes its native actions. Only the canonical Kernel owns PayGod decision and evidence identity; no optional EIK adapter, website, agent instructions, or private research workflow can silently acquire that authority.

## Documentation change control

- Preserve earlier dated evidence snapshots and exact commit pins as history. **Append** new technical-status records for newly merged work.
- Treat the [capabilities snapshot](eik/capabilities.v0.json) as an **informational description**, not a signed service discovery protocol or runtime guarantee.
- Website EN/AR pages must link to public accepted Kernel witnesses only. The private Observatory's research record is not a public attestation.
- Before marking a feature "available," verify exact implementation SHA, executable checks, applicable non-claims, and independently assessed deployment state where relevant.
