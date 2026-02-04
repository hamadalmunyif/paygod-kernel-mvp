# ADR-0001: Envelope schema pointer naming (schema_ref preferred)

## Status
Accepted (MVP)

## Context
The Belloop Artifact Envelope needs a stable way to point to the payload schema used for `data`.
We previously used `schema` and then introduced `schema_id`, which created ambiguity with the payload-level `schema_id`
(where payload schemas use official URIs like https://paygod.org/schemas/*).

This caused confusion in documentation and examples.

## Decision
The envelope uses **schema_ref** as the preferred field for schema binding, pointing to a repo-local schema path, e.g.:
- contracts/schemas/decision.schema.json

For backward compatibility, the envelope still accepts:
- schema (legacy)
- schema_id (legacy; envelope only)

The validator must enforce:
- One of (schema_ref | schema | schema_id) exists (anyOf)
- No guessing. Binding must be explicit.

## Consequences
- Examples and documentation must prefer schema_ref.
- Legacy fields remain supported during MVP to avoid breaking existing artifacts.
- Payload schema_id remains the canonical public URI and must not be confused with envelope pointer.
