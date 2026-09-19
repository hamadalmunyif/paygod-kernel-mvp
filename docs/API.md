# API Reference

This document describes the small Node demo surface under `api/`.

## Boundary status

Under Repository Boundary Closure v0.1 this demo server is **not** an execution authority. It does not run packs, create decisions, create receipts, or originate bundle identity. Until it is replaced by a thin adapter to the Canonical Kernel, execution-like routes fail closed.

Base URL (local): `http://localhost:3000`

## GET /health

Returns service liveness.

```bash
curl -s http://localhost:3000/health
```

Expected response:

```json
{"status":"OK"}
```

## POST /run — deprecated / fail closed

This route no longer fabricates a demo run or `bundle_digest`.

Expected status: **410 Gone**.

```json
{
  "error": "Demo execution endpoint deprecated",
  "authority": "canonical-kernel-required"
}
```

## GET /runs/:bundle_digest — deprecated / fail closed

Expected status: **410 Gone**. The demo server does not maintain an authoritative run store.

## GET /runs/:bundle_digest/zip — deprecated / fail closed

Expected status: **410 Gone**. The demo server does not construct or expose pseudo evidence bundles.

## Canonical execution adapter

The repository also contains `deploy/docker/api/app/Program.cs`. That HTTP adapter delegates execution to `/runner/PayGod.Cli.dll run` and returns the artifacts produced by that canonical path. It may transport/package those outputs; it must not independently invent decision, receipt, manifest, or canonical bundle identity semantics.

See `docs/REPOSITORY_BOUNDARY.md`.
