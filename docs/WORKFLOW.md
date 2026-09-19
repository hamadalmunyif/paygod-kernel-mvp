# Developer Workflow

## Current boundary

Repository Boundary Closure v0.1 separates the deprecated Node demo API from the canonical execution adapter.

### Node demo API

`api/server.js` may be used for liveness testing:

```bash
cd api
node server.js
curl -s http://localhost:3000/health
```

Do **not** use `POST /run` as an execution path. It intentionally returns HTTP 410 with `canonical-kernel-required`. The corresponding run/bundle retrieval routes also fail closed. This prevents the demo surface from originating alternate execution truth.

### Canonical Docker HTTP adapter

`deploy/docker/api/app/Program.cs` is the repository-hosted execution-facing adapter. It accepts a request, invokes:

```text
dotnet /runner/PayGod.Cli.dll run --pack ... --input ... --out ...
```

and transports the artifacts produced by that canonical execution path.

The adapter must not independently create decision verdicts, receipts, manifest semantics, or canonical bundle identity.

## Boundary witness

Run:

```bash
python3 tools/check_repository_boundary.py --contract tests/boundary/valid-adapter.json --expect pass
python3 tools/check_repository_boundary.py --contract tests/boundary/alternate-authority.json --expect reject
python3 tools/check_repository_boundary.py --scan-current
```

The first and third commands must pass. The second command succeeds only when the deliberately invalid alternate-authority fixture is rejected.

See `docs/REPOSITORY_BOUNDARY.md`.
