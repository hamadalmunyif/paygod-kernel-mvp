# X1-R0 Preflight 001 — Public Offering Capture

Status: **PUBLIC LISTING CAPTURED — EXECUTABLE OFFERING OBJECT NOT YET CAPTURED — NO PURCHASE AUTHORIZED**  
Observed: 2026-10-05  
Scope: X1-R0 pre-purchase research only

## Purpose

Record the first post-Level-0 live-market observation before any wallet funding, USDC transfer, ACP job creation, provider purchase, or PayGod output.

This record narrows the next acquisition step. It does not authorize execution and it does not treat a public marketplace description as the executable ACP requirement schema.

## Selected offering class

Preferred provider/offering remains:

- provider display name: `Quiver`
- public marketplace agent reference: `019dcc66-4241-7ac4-b21e-8dd159898576`
- public wallet display observed: `0xd6a5...0261` only; full address NOT captured by this public surface
- offering: `getCongressTrades`
- public listed price: `0.01 USDC`
- public listed SLA: `5 min`
- service class: informational / structured data
- public description: latest congressional trades across all tickers, with optional ticker filter and limit
- public described row semantics include Representative/Senator, ReportDate, TransactionDate, Ticker, Transaction, Range/Amount, Party, House, and Quiver pre-computed ExcessReturn vs SPY
- public description states a 1-hour cache

Public marketplace reference:

`https://app.virtuals.io/acp/agent/019dcc66-4241-7ac4-b21e-8dd159898576`

## Why the public listing is not enough

The current ACP Node v2 discovery flow returns live offerings with typed requirements. The SDK job-creation path validates requirement data against the offering JSON schema when present before creating the on-chain job.

Therefore the public marketplace description is discovery evidence only. It is NOT treated as:

- the exact executable offering object;
- the exact requirements JSON schema;
- the full provider wallet identity;
- the current `requiredFunds` value;
- the exact current `priceValue`/token representation used by the SDK;
- a sufficient basis for constructing or submitting a job.

No request JSON is inferred from the prose description.

## Frozen semantic request candidate

If the exact live offering object faithfully supports the public description, the intended R0 request is frozen semantically as:

- offering name: `getCongressTrades`
- ticker filter: omitted / all tickers
- limit: `5`

If the exact live requirement schema does not accept this request without reinterpretation, coercion, or silent substitution:

`STOP — UPDATE PREFLIGHT RECORD BEFORE EXECUTION`

Do not switch to another offering merely to obtain a successful PayGod comparison.

## Frozen native acceptance criteria

Before seeing any PayGod result, the native evaluator criteria are:

1. the provider submits a deliverable within the native job lifecycle;
2. the deliverable is structurally inspectable rather than an opaque unsupported assertion;
3. where rows are returned, the response corresponds semantically to the public `getCongressTrades` description and the requested all-ticker / limit-5 scope;
4. no PayGod result is visible before the native evaluator decision artifact is committed;
5. factual truth/provenance of each congressional-trade row is NOT silently equated with structural service completion; any external factual cross-check is recorded as a separate evidence dimension.

The native decision remains `COMPLETE | REJECT | HOLD-NO-ACTION` under `CASE_PROTOCOL.md`.

## Remaining pre-purchase blockers

The following MUST be captured/frozen before a live paid job can be created:

- exact current ACP offering object;
- exact requirements JSON schema;
- full provider wallet address;
- current price/token/SLA fields as returned by authenticated/current discovery;
- `requiredFunds` / hook-related fields if present;
- client address;
- explicit non-zero evaluator address and its relationship to the client;
- exact requirement payload after schema validation;
- evidence-capture location and chronology references;
- maximum total approved economic exposure, including any service/gas/platform exposure.

## Economic gate

Current approved maximum total economic exposure remains:

`UNSET — EXPLICIT USER APPROVAL REQUIRED`

The observed public service price of `0.01 USDC` is not the approved total exposure.

This record does not authorize:

- wallet creation or funding;
- USDC transfer;
- transaction signing;
- ACP job creation;
- provider purchase;
- automated execution.

## Stop-build compliance

No Kernel, Pack, policy DSL, receipt, ledger, schema, verifier, ACP adapter, or execution-authority semantics are changed.

The next permitted step is exact live-offering/actor capture. Paid execution remains behind the separate explicit economic gate.
