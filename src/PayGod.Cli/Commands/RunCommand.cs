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
            .ToArray();

        var bundleDigest = ComputeBundleDigest(fileEntries);

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
                file_count = fileEntries.Length,
                bundle_digest = bundleDigest
            },
            files = fileEntries
        };

        var manifestPath = Path.Combine(outDir.FullName, "manifest.json");
        WriteJson(manifestPath, manifest);

        Console.WriteLine("✅ Run complete.");
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
        // plan.json=<sha256>\nfindings.json=<sha256>\nledger.jsonl=<sha256>
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
        Console.Error.WriteLine($"❌ {msg}");
        Environment.Exit(2);
    }
}

