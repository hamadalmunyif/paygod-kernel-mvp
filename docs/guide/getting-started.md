# Getting Started with PayGod Kernel

**Authoritative onboarding:** [START_HERE.md](../../START_HERE.md). The commands below are introductory and do not replace the pinned witness and CI test instructions there.

## Build the canonical CLI

Prerequisite: .NET SDK 8.

```bash
git clone https://github.com/hamadalmunyif/paygod-kernel-mvp.git
cd paygod-kernel-mvp
dotnet publish src/PayGod.Cli/PayGod.Cli.csproj -c Release -o out
```

The canonical CLI can validate, test and run compatible policy packs. See the example commands in [START_HERE](../../START_HERE.md). Use the versioned `paygod-c14n-v1` profile: external fractional measurements cannot be silently passed as JSON decimal values into canonical decision hashes.

## Independent verification

The standalone Python verifier can verify transferred manifest/receipt/ledger/file integrity without rerunning the originating policy. It supports an optional detached Ed25519 receipt signature under a **recipient-owned** trust store. See [Standalone Verifier](../STANDALONE_VERIFIER.md).

For real/deidentified sources, apply [ADR 0003](../../adrs/0003-evidence-admission-before-decision-execution.md) before evaluation: unavailable/unrepresentable mandatory evidence produces orchestration `NOT RUN`, not a forged `FALSE`.

## Contributing

Read [Contributing](../../CONTRIBUTING.md), [Gates](../../GATES.md) and the active [Stop-Build](../STOP_BUILD_RULE.md). This repository is the canonical public implementation. External research results do not become installed Kernel features by publication alone.
