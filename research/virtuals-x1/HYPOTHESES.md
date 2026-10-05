# X1 Hypothesis Register

Status: OPEN

A hypothesis is not a primitive and does not authorize implementation.

| ID | Hypothesis | Falsification question | Status |
| --- | --- | --- | --- |
| X1-H01 | External predecessor state can be reconstructed deterministically enough for a bounded decision. | Can two independent reconstructions of the same pinned ACP state produce the same decision-relevant snapshot without hidden context? | UNTESTED |
| X1-H02 | Evidence Admission generalizes beyond the gas workflow. | Can ACP evidence be mapped as ADMIT/WITHHELD without inventing semantics or changing the kernel? | UNTESTED |
| X1-H03 | A shadow PayGod decision can add information beyond ACP native authorization. | Do real cases expose material evidence-basis distinctions not already captured by actor permission and phase validity? | UNTESTED |
| X1-H04 | Decision-to-predecessor binding may be reusable across protocols. | Is the required state context stable and minimal enough to bind without importing ACP semantics into the kernel? | UNTESTED |
| X1-H05 | Post-flight conformance may be a separate reusable layer. | Can execution be checked against a pre-flight decision without treating execution success as decision correctness? | UNTESTED |
| X1-H06 | Next-transition eligibility may matter but may belong outside the kernel. | Does successor eligibility recur as a real requirement, and which layer should own it? | UNTESTED |
| X1-H07 | PayGod can remain protocol-independent. | Can the same kernel remain unchanged while only adapters/evidence mappings vary across ACP and another external transition system? | UNTESTED |

## Promotion rule

A hypothesis may be promoted only after a recorded witness, recurrence/importance assessment, layer analysis, and explicit architecture decision.

No X1 hypothesis authorizes code during Level 0.
