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
        var command = new Command("run", "Run a pack against an input and emit loop artifacts (plan/findings/ledger).");

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

        var inputHash = Hasher.ComputeHash(inputJson);
        var packDigest = Sha256Hex(File.ReadAllBytes(packPath));
        var now = DateTimeOffset.UtcNow.ToString("o");

        // Plan
        var plan = new
        {
            api_version = "paygod/v1",
            kind = "PlanReport",
            generated_at = now,
            pack = new { name = pack.metadata.name, version = pack.metadata.version, path = packDir, digest_sha256 = packDigest },
            input = new { path = input.FullName, canonical_hash = inputHash },
            settings = new { }
        };

        WriteJson(Path.Combine(outDir.FullName, "plan.json"), plan);

        // Evaluate
        var result = PolicyEngine.Evaluate(pack, inputJson);

        // Findings
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
            generated_at = now,
            pack = new { name = pack.metadata.name, version = pack.metadata.version },
            findings
        };
        WriteJson(Path.Combine(outDir.FullName, "findings.json"), findingsReport);

        // Truth ledger append (allow/deny/error only)
        var verdict = result.Decision == "unknown" ? "error" : result.Decision;
        if (verdict is "allow" or "deny" or "error")
        {
            AppendLedger(Path.Combine(outDir.FullName, "ledger.jsonl"), pack, inputHash, verdict, result);
        }

        Console.WriteLine("✅ Run complete.");
    }

    private static void AppendLedger(string ledgerPath, PackDefinition pack, string inputHash, string verdict, PolicyResult result)
    {
        var zeros = new string('0', 64);
        var (prevHash, nextIndex) = ReadLedgerTail(ledgerPath, zeros);

        var now = DateTimeOffset.UtcNow.ToString("o");
        var data = new
        {
            verdict,
            rule_name = result.RuleName,
            reason = result.Reason,
            pack = new { name = pack.metadata.name, version = pack.metadata.version },
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

    private static void WriteJson(string path, object obj)
    {
        File.WriteAllText(path, JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true }), new UTF8Encoding(false));
    }

    private static void Fail(string msg)
    {
        Console.Error.WriteLine($"❌ {msg}");
        Environment.Exit(2);
    }
}
