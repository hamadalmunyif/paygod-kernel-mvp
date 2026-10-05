# X1 Level 0 Protocol — Research Freeze

Status: OPEN — METHOD FROZEN; DEPLOYMENT WITNESS BLOCKING

Purpose: establish external facts and freeze the first current-rail experiment before observing PayGod outcomes.

## Current source references

- `Virtual-Protocol/acp-node-v2@0f4b678516c354c1541b92aa08db11ece3506261`
- `Virtual-Protocol/acp-cli@5c01771b964e0e431e6c4bea5a4d481514a30e24`

Current official SDK configuration identifies Base chain 8453 and ACP contract `0x238E541BfefD82238730D00a2208E5497F1832E0`.

Earlier modular ACP v2 references are retained as historical witnesses, not the default rail for new case acquisition.

A source constant is not proof of historical/live implementation identity.

## Level 0 resolution matrix

| Question | Current disposition |
| --- | --- |
| Current rail/source pins | RESOLVED |
| Current ACP address from pinned SDK | RESOLVED AS SOURCE FACT — not yet block-bound deployment proof |
| Target transition | FROZEN: `SUBMITTED → COMPLETED` with explicit non-zero evaluator |
| Zero-evaluator completion ambiguity | RESOLVED by current-runtime exclusion witness |
| Public chain vs ACP history boundary | RESOLVED at authentication boundary; unrelated-job authorization scope remains unclaimed |
| Pre-decision evidence cut-off | FROZEN |
| Native evaluator blindness | FROZEN as committed decision artifact before PayGod |
| PayGod shadow chronology | FROZEN after native-decision commitment |
| Historical-vs-prospective acquisition choice | RESOLVED: prospective bounded real job preferred |
| Provider/offering selection method | FROZEN |
| Case register / reconstruction record | FROZEN |
| Deployment/proxy/implementation method | FROZEN in `DEPLOYMENT_BINDING_METHOD.md` |
| Independent deployment witness at a Base reference block | **OPEN — BLOCKER** |
| Paid R0 execution | NOT AUTHORIZED; economic cap remains separate human approval |

## Current target transition

```text
SUBMITTED → COMPLETED
```

Requirements:

- current Node v2 rail;
- explicit non-zero evaluator;
- evidence available before evaluator action;
- economically consequential job where practical;
- no PayGod control of execution during the first comparison.

`SUBMITTED → REJECTED` remains a useful companion outcome but is not required for the first case.

## Evidence / decision ordering now frozen

For any prospective qualifying R0 case:

```text
freeze request + acceptance criteria
→ real provider submission
→ predecessor-state/evidence capture
→ evidence package commitment
→ native evaluator decision artifact
→ native decision commitment
→ Evidence Admission
→ NOT RUN or PayGod shadow
→ PayGod run commitment
→ execute already-committed native ACP action
→ successor-state / settlement observation
```

If a required PayGod input is not semantically representable/admissible:

`WITHHELD → NOT RUN`

NOT RUN is not a PayGod verdict.

If native-decision commitment cannot be shown to precede the PayGod-run commitment in the recorded chronology, the case MUST NOT claim a blinded comparison.

The chronology does not establish trusted external time.

## Deployment binding gate

Level 0 does not close merely because the official SDK names the current contract.

The repository now freezes the binding method in `DEPLOYMENT_BINDING_METHOD.md`.

Before Level 0 closure, X1 MUST capture one independent current Base reference-block witness containing at least:

```text
chain_id = 8453
block_number = B
block_hash = H(B)

proxy_address =
  0x238E541BfefD82238730D00a2208E5497F1832E0

ERC-1967 implementation slot @ B
raw storage word
implementation address

proxy bytecode hash @ B
implementation bytecode hash @ B
raw evidence references
```

This reference witness demonstrates that the method works and independently binds the current deployment at that block.

Every later real case MUST repeat the same binding at its own predecessor block.

## Authentication boundary

The pinned ACP client proves that history retrieval authenticates an agent before calling:

`/chats/{chainId}/{jobId}/history`.

It does NOT by itself prove the authorization scope for unrelated jobs.

Therefore Level 0 records only:

```text
AUTHENTICATION-GATED HISTORY
```

and does not claim:

```text
PARTICIPANT-ONLY HISTORY
```

unless separately tested.

Because the selected prospective R0 path operates as a legitimate participant, unrelated-job authorization scope is not a reason to invent a claim or mutate PayGod.

## Acquisition decision already frozen

The preferred first fully reconstructable case is a prospective bounded real ACP job with:

- an independent external provider;
- explicit non-zero evaluator;
- low economic exposure;
- no unnecessary execution/trading/bridge action;
- objective acceptance criteria where practical;
- complete participant-visible evidence preserved before evaluator action;
- PayGod shadow only.

The first live workflow remains `X1-R0 — instrumentation case`, not proof of protocol independence or market value.

The live spend gate remains separate:

`UNSET — EXPLICIT USER APPROVAL REQUIRED`

Level 0 methodological closure MUST NOT be interpreted as authorization to spend.

## Required Level 0 exit artifacts

The repository now has or has frozen:

- current-rail deployment inventory;
- deployment-binding method;
- event/state reconstruction protocol;
- target transition;
- public-vs-authentication-gated evidence boundary;
- pre-decision cut-off;
- frozen acquisition/sampling method;
- native-decision commitment rule;
- PayGod-run chronology rule;
- explicit exclusions/non-claims;
- no kernel change.

The remaining exit artifact is:

- **one raw current Base deployment-binding witness produced with the frozen method.**

## Stop conditions

Pause X1 rather than coding around the problem if:

- the current deployment cannot be independently bound at a reference block;
- the required pre-decision evidence cannot be obtained lawfully as observer/participant;
- a faithful predecessor snapshot cannot be reconstructed for the real case;
- the first useful experiment would require kernel mutation before observational evidence exists.

A Level 0 STOP is a valid research result.
