using System.CommandLine;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using PayGod.Cli.Core;

namespace PayGod.Cli.Commands;

public static class RunCommand
{
    public static Command Create()
    {
        var command = new Command("run", "Run a pack against an input and emit loop artifacts (plan/findings/ledger/manifest).");

        var packOpt = new Option<string>("--pack", "Path to the pack directory.") { IsRequired = true };
        var inputOpt = new Option<FileInfo>("--input", "Path to input JSON.") { IsRequired = true };
        var outOpt = new Option<DirectoryInfo>("--out", "Output directory.") { IsRequired = true };

        command.AddOption(packOpt);
        command.AddOption(inputOpt);
        command.AddOption(outOpt);

        command.SetHandler((string packDir, FileInfo input, DirectoryInfo outDir) =>
        {
            Run(packDir, input, outDir);
        }, packOpt, inputOpt, outOpt);

        return command;
    }

    private static void Run(string packDir, FileInfo input, DirectoryInfo outDir)
    {
        var packPath = Path.Combine(packDir, "pack.yaml");
        if (!File.Exists(packPath)) Fail($"Missing pack.yaml: {packPath}");
        if (!input.Exists) Fail($"Missing input file: {input.FullName}");

        outDir.Create();

        var pack = PolicyEngine.LoadPack(packPath);
        var inputJson = JsonNode.Parse(File.ReadAllText(input.FullName)) ?? throw new InvalidOperationException("Invalid input JSON.");

        // One run timestamp for the whole bundle (important for determinism)
        var runTs = PaygodClock.UtcNowOffset.ToString("o");

        var inputHash = Hasher.ComputeHash(inputJson);
        var packDigest = Sha256Hex(File.ReadAllBytes(packPath));

        // Unified pack object (used everywhere)
        var packObj = new
        {
            name = pack.metadata.name,
            version = pack.metadata.version,
            path = packDir,
            digest_sha256 = packDigest
        };

        // 1) Plan
        var plan = new
        {
            api_version = "paygod/v1",
            kind = "PlanReport",
            generated_at = runTs,
            pack = packObj,
            input = new { path = input.FullName, canonical_hash = inputHash },
            settings = new { }
        };
        var planPath = Path.Combine(outDir.FullName, "plan.json");
        WriteJson(planPath, plan);

        // 2) Evaluate
        var result = PolicyEngine.Evaluate(pack, inputJson);

        // 3) Findings
        var findings = new List<object>();
        if (result.Decision == "flag")
        {
            findings.Add(new
            {
                kind = "flag",
                severity = "medium",
                code = "PACK_FLAG",
                message = result.Reason,
                rule_name = result.RuleName,
                evidence_refs = Array.Empty<string>()
            });
        }
        else if (result.Decision == "error" || result.Decision == "unknown")
        {
            findings.Add(new
            {
                kind = "flag",
                severity = "high",
                code = "EVAL_ERROR",
                message = result.Decision == "unknown" ? "No policy rules matched." : result.Reason,
                rule_name = result.RuleName,
                evidence_refs = Array.Empty<string>()
            });
        }

        var findingsReport = new
        {
            api_version = "paygod/v1",
            kind = "FindingsReport",
            generated_at = runTs,
            pack = packObj,
            findings
        };
        var findingsPath = Path.Combine(outDir.FullName, "findings.json");
        WriteJson(findingsPath, findingsReport);

        // 4) Truth ledger (allow/deny/error only)
        var verdict = result.Decision == "unknown" ? "error" : result.Decision;
        var ledgerPath = Path.Combine(outDir.FullName, "ledger.jsonl");
        if (verdict is "allow" or "deny" or "error")
        {
            AppendLedger(ledgerPath, packObj, inputHash, verdict, result, runTs);
        }

        // 5) Manifest (bundle lock)
        // Compute file hashes (stable order) then compute bundle digest from "name=sha256" lines.
        // NOTE: receipt.json will be included after we write it.
        var files = new[]
        {
            new FileInfo(planPath),
            new FileInfo(findingsPath),
            new FileInfo(ledgerPath)
        }.Where(f => f.Exists).ToArray();

        var fileEntries = files
            .OrderBy(f => f.Name, StringComparer.Ordinal)
            .Select(f => new
            {
                name = f.Name,
                sha256 = Sha256FileHex(f.FullName),
                bytes = f.Length
            })
            .ToList();

        // We'll compute bundleDigest later after receipt is emitted (so receipt is part of the bundle)
        // For now, placeholder (will be replaced).
        var bundleDigest = "pending";

        var manifest = new
        {
            api_version = "paygod/v1",
            kind = "Manifest",
            generated_at = runTs,
            pack = packObj,
            input = new { canonical_hash = inputHash },
            bundle = new
            {
                algorithm = "sha256",
                digest_method = "sha256(join_lines(name='name=sha256' sorted by name))",
                file_count = 0,
                bundle_digest = bundleDigest
            },
            files = Array.Empty<object>()
        };

        var manifestPath = Path.Combine(outDir.FullName, "manifest.json");

        // We need manifest to reference receipt, and receipt to reference manifest_sha256.
        // So we write manifest AFTER receipt is generated, but receipt needs manifest path.
        // Approach:
        //  - write a temporary manifest after receipt generation fields are prepared? (avoid)
        // Better:
        //  - generate receipt AFTER writing manifest, but then manifest won't include receipt unless we rewrite it.
        // MVP choice:
        //  - write manifest, generate receipt, then rewrite manifest to include receipt and updated digest.

        // Write initial manifest WITHOUT receipt (will be overwritten deterministically after receipt is written)
        var initialManifest = new
        {
            api_version = "paygod/v1",
            kind = "Manifest",
            generated_at = runTs,
            pack = packObj,
            input = new { canonical_hash = inputHash },
            bundle = new
            {
                algorithm = "sha256",
                digest_method = "sha256(join_lines(name='name=sha256' sorted by name))",
                file_count = fileEntries.Count,
                bundle_digest = ComputeBundleDigest(fileEntries)
            },
            files = fileEntries.ToArray()
        };

        WriteJson(manifestPath, initialManifest);

        // 6) Receipt (execution certificate) - separate from manifest
        // MUST be deterministic: generated_at MUST use injected PAYGOD_CLOCK (not wall time).
        var clockValue = Environment.GetEnvironmentVariable("PAYGOD_CLOCK") ?? "unset";

        // Runner identity (prefer injected by docker pipeline; keep deterministic defaults)
        var runnerImage = Environment.GetEnvironmentVariable("PAYGOD_RUNNER_IMAGE") ?? "paygod/runner:dev";
        var runnerDigest = Environment.GetEnvironmentVariable("PAYGOD_RUNNER_DIGEST") ?? "unknown";

        // Schema manifest sha (optional for now). Keep deterministic placeholder.
        var schemaManifestSha = new string('0', 64);

        // manifest sha256 binds receipt -> bundle lock (this is the first manifest write)
        var manifestSha = Sha256FileHex(manifestPath);

        var receipt = new
        {
            api_version = "paygod/v1",
            kind = "Receipt",
            spec_version = "0.1.0",

            // Deterministic by design: MUST equal PAYGOD_CLOCK (not wall time)
            generated_at = clockValue,

            clock = new { value = clockValue, source = "env:PAYGOD_CLOCK" },

            canonicalization = new
            {
                json = "rfc8785",
                schema_manifest_sha256 = schemaManifestSha
            },

            runner = new
            {
                image = runnerImage,
                image_digest = runnerDigest
            },

            pack = packObj,
            input = new { canonical_hash = inputHash },

            // bundle_digest will be set after we include receipt and re-write manifest
            bundle = new
            {
                bundle_digest = "pending",
                manifest_sha256 = manifestSha,
                files = Array.Empty<object>()
            },

            verdict = new
            {
                value = verdict,
                rule_name = result.RuleName,
                reason = result.Reason
            },

            replay = new
            {
                command =
                    $"docker run --rm -e PAYGOD_CLOCK={clockValue} -e PAYGOD_STRICT=1 " +
                    $"-v \"<PACK_DIR>:/pack:ro\" -v \"<INPUT_FILE>:/input/input.json:ro\" -v \"<OUT_DIR>:/out:rw\" " +
                    $"{runnerImage} run --pack /pack --input /input/input.json --out /out"
            }
        };

        var receiptPath = Path.Combine(outDir.FullName, "receipt.json");
        WriteJson(receiptPath, receipt);

        // Now include receipt into the bundle and finalize deterministic manifest + receipt binding
        fileEntries.Add(new
        {
            name = "receipt.json",
            sha256 = Sha256FileHex(receiptPath),
            bytes = new FileInfo(receiptPath).Length
        });

        var finalFileEntries = fileEntries
            .OrderBy(f => f.name, StringComparer.Ordinal)
            .ToArray();

        var finalBundleDigest = ComputeBundleDigest(finalFileEntries);

        var finalManifest = new
        {
            api_version = "paygod/v1",
            kind = "Manifest",
            generated_at = runTs,
            pack = packObj,
            input = new { canonical_hash = inputHash },
            bundle = new
            {
                algorithm = "sha256",
                digest_method = "sha256(join_lines(name='name=sha256' sorted by name))",
                file_count = finalFileEntries.Length,
                bundle_digest = finalBundleDigest
            },
            files = finalFileEntries
        };

        // rewrite manifest deterministically
        WriteJson(manifestPath, finalManifest);

        // recompute manifest sha after final manifest write
        var finalManifestSha = Sha256FileHex(manifestPath);

        var finalReceipt = new
        {
            api_version = "paygod/v1",
            kind = "Receipt",
            spec_version = "0.1.0",
            generated_at = clockValue,
            clock = new { value = clockValue, source = "env:PAYGOD_CLOCK" },
            canonicalization = new { json = "rfc8785", schema_manifest_sha256 = schemaManifestSha },
            runner = new { image = runnerImage, image_digest = runnerDigest },
            pack = packObj,
            input = new { canonical_hash = inputHash },
            bundle = new
            {
                bundle_digest = finalBundleDigest,
                manifest_sha256 = finalManifestSha,
                files = finalFileEntries
            },
            verdict = new { value = verdict, rule_name = result.RuleName, reason = result.Reason },
            replay = new
            {
                command =
                    $"docker run --rm -e PAYGOD_CLOCK={clockValue} -e PAYGOD_STRICT=1 " +
                    $"-v \"<PACK_DIR>:/pack:ro\" -v \"<INPUT_FILE>:/input/input.json:ro\" -v \"<OUT_DIR>:/out:rw\" " +
                    $"{runnerImage} run --pack /pack --input /input/input.json --out /out"
            }
        };

        // rewrite receipt deterministically after manifest finalized
        WriteJson(receiptPath, finalReceipt);

        Console.WriteLine("OK: Run complete.");
    }

    private static void AppendLedger(
        string ledgerPath,
        object packObj,
        string inputHash,
        string verdict,
        PolicyResult result,
        string runTs)
    {
        var zeros = new string('0', 64);
        var (prevHash, nextIndex) = ReadLedgerTail(ledgerPath, zeros);

        // Use the same run timestamp for determinism
        var now = runTs;

        var data = new
        {
            verdict,
            rule_name = result.RuleName,
            reason = result.Reason,
            pack = packObj,
            input_hash = inputHash,
            evidence_refs = Array.Empty<string>()
        };

        var hashInput = new JsonObject
        {
            ["previous_hash"] = prevHash,
            ["timestamp"] = now,
            ["data"] = JsonNode.Parse(JsonSerializer.Serialize(data))!
        };

        var recordHash = Hasher.ComputeHash(hashInput);

        var entry = new
        {
            entry_index = nextIndex,
            timestamp = now,
            previous_hash = prevHash,
            data,
            record_hash = recordHash
        };

        File.AppendAllText(ledgerPath, JsonSerializer.Serialize(entry) + "\n", new UTF8Encoding(false));
    }

    private static (string prevHash, int nextIndex) ReadLedgerTail(string ledgerPath, string genesis)
    {
        if (!File.Exists(ledgerPath)) return (genesis, 0);

        string? lastLine = null;
        foreach (var line in File.ReadLines(ledgerPath))
        {
            if (!string.IsNullOrWhiteSpace(line)) lastLine = line;
        }
        if (lastLine is null) return (genesis, 0);

        using var doc = JsonDocument.Parse(lastLine);
        var root = doc.RootElement;

        var prev = root.GetProperty("record_hash").GetString() ?? genesis;
        var idx = root.GetProperty("entry_index").GetInt32() + 1;
        return (prev, idx);
    }

    private static string Sha256Hex(byte[] bytes)
    {
        using var sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(bytes)).ToLowerInvariant();
    }

    private static string Sha256FileHex(string path)
    {
        using var sha = SHA256.Create();
        using var fs = File.OpenRead(path);
        return Convert.ToHexString(sha.ComputeHash(fs)).ToLowerInvariant();
    }

    private static string ComputeBundleDigest(IEnumerable<dynamic> fileEntries)
    {
        // Deterministic string form:
        // plan.json=<sha256>\nfindings.json=<sha256>\nledger.jsonl=<sha256>\nreceipt.json=<sha256>
        var sb = new StringBuilder();
        foreach (var f in fileEntries)
        {
            sb.Append(f.name);
            sb.Append('=');
            sb.Append(f.sha256);
            sb.Append('\n');
        }
        var bytes = Encoding.UTF8.GetBytes(sb.ToString());
        return Sha256Hex(bytes);
    }

    private static void WriteJson(string path, object obj)
    {
        File.WriteAllText(
            path,
            JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true }),
            new UTF8Encoding(false));
    }

    private static void Fail(string msg)
    {
        Console.Error.WriteLine($"ERR: {msg}");
        Environment.Exit(2);
    }
}