# P0 Decision Log

This log records decisions made during P0. It does not rewrite the frozen custodian or reviewer artifacts.

| ID | Decision | Rationale |
| --- | --- | --- |
| P0-D001 | Classify the exercise as simulated_shadow_pilot. | The 15 cases, references, and dates are simulated and do not satisfy B2-REAL. |
| P0-D002 | Freeze the custodian intake and reviewer report without retrospective correction. | Source defects must remain observable rather than being repaired after downstream analysis. |
| P0-D003 | Apply the historical cut-off rule strictly, including the same-day rule. | Evidence that exists now is not proof that it existed at decision time. |
| P0-D004 | Adopt Reviewer Decision Semantics v1 prospectively only. | HOLD and REJECT thresholds must be frozen before future comparisons; the frozen P0 reviewer decisions remain unchanged. |
| P0-D005 | Separate Case Evidence from Professional/Normative Knowledge. | A reviewer may rely on professional knowledge, but that knowledge is not case evidence and must be recorded separately. |
| P0-D006 | Map frozen fields without semantic coercion. | Missing, UNPROVEN, partial, or semantically different evidence is not converted to FALSE. |
| P0-D007 | Use WITHHELD as a pre-kernel workflow state. | WITHHELD means a required frozen value cannot be assigned faithfully; it is not a kernel value. |
| P0-D008 | Fail the Executability Gate when any required frozen value is WITHHELD. | The canonical kernel path must receive a complete valid input rather than inferred booleans. |
| P0-D009 | Record NOT RUN instead of forcing PayGod execution. | NOT RUN is not a PayGod verdict and therefore produces no agreement/disagreement comparison. |
| P0-D010 | Do not classify a contract/kernel gap merely because P0 is NOT RUN. | Non-execution first identifies an admission boundary; architecture changes require recurrence and operational importance. |
| P0-D011 | Make no kernel or pack semantic change from P0. | The pilot did not demonstrate a kernel defect or justify contract expansion. |
| P0-D012 | Close P0 as PASS WITH BOUNDARY while keeping B2-REAL at 0 / 10. | The workflow objective was exercised successfully, but the data remain simulated. |
| P0-D013 | Preserve the frozen P0 source records without re-soliciting corrections for this pilot. | Future protocol improvements apply prospectively; the historical P0 witness remains immutable. |

## Stop-build rule

Observe → classify → count recurrence → assess operational importance → then decide architecture.

Only demonstrated kernel defects enter kernel Build.
