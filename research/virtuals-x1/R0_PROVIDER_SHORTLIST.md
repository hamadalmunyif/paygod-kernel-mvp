# X1-R0 Provider / Offering Shortlist

Status: FROZEN SHORTLIST — NO PURCHASE AUTHORIZED  
Observed: 2026-10-05  
Purpose: choose a low-risk, objectively inspectable first real workflow without tailoring selection to a PayGod result.

## Selection criteria

The R0 provider/offering should maximize observability and minimize unrelated execution risk.

Required:

- current Virtuals ACP marketplace;
- independent external provider;
- low fixed service price;
- no leveraged trading, token swap, bridge, custody, or required fund-transfer action;
- output that can be checked structurally and, where practical, against an external public source;
- short SLA;
- requirements simple enough to freeze before work starts;
- deliverable can be retained in the X1 evidence package;
- no custom hook complexity unless unavoidable.

Preferred:

- structured JSON/data output;
- deterministic filter/limit semantics;
- public-source subject matter;
- provider with prior completed jobs.

## Preferred candidate — Quiver / getCongressTrades

Public marketplace reference:

`https://app.virtuals.io/acp/agent/019dcc66-4241-7ac4-b21e-8dd159898576`

Observed public listing:

- provider: Quiver;
- offering: `getCongressTrades`;
- fixed listed price: `0.01 USDC`;
- listed SLA: `5 min`;
- optional ticker filter and limit;
- described output includes Representative/Senator, ReportDate, TransactionDate, Ticker, Transaction, Range/Amount, Party, House, and ExcessReturn.

### Why preferred

This offering is a strong instrumentation candidate because:

- the service is informational rather than an execution action;
- the economic exposure is small at the listed service price;
- output is structured;
- filter and limit behavior can be frozen and checked;
- congressional-trade subject matter has public external references, allowing a later distinction between structural acceptance and independent factual cross-checking.

### Remaining requirement before purchase

The exact live offering object and requirement schema MUST be retrieved from the current ACP browse surface immediately before the R0 freeze.

Do not infer the exact request JSON from the public description.

If the live offering schema, price, SLA, or provider identity materially differs from this record, stop and update the pre-purchase record before proceeding.

## Alternate — 3D Claw / data-only status or search offering

Public marketplace reference:

`https://app.virtuals.io/acp/agent/1747`

Observed public listings include fixed-price `0.01 USDC` offerings such as:

- `get_printer_status`;
- `check_ams_filament`;
- `search_3d_models`.

This is an alternate only.

Reason for lower rank: printer/filament state is harder for X1 to independently verify outside the provider, while model search is more externally checkable but less directly tied to a consequential evaluation question.

## Excluded from R0

### Wasabot execution offerings

Trading/position/vault operations are excluded from R0 because they introduce market risk, leverage, collateral, and downstream state changes unrelated to the first evidence-admission experiment.

### Token-swap / bridge offerings

Swap, bridge, or fund-transfer offerings are excluded because they introduce token routing, slippage, destination, hook, and execution-risk semantics before X1 has validated the simpler informational workflow.

## Selection decision

Preferred R0 offering class:

`Quiver / getCongressTrades`

Selection is provisional until the current authenticated/current ACP browse result is captured and frozen.

## Economic boundary

The public listing shows a service price of `0.01 USDC`.

This is NOT the approved total spend cap. Gas, platform mechanics, wallet funding requirements, or other transaction costs may exist.

The total economic exposure remains:

`UNSET — EXPLICIT USER APPROVAL REQUIRED`

No transaction is authorized by this shortlist.
