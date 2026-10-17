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
        command.SetHandler((string packDir, FileInfo input, DirectoryInfo outDir) => Run(packDir, input, outDir), packOpt, inputOpt, outOpt);
        return command;
    }

    private static void Run(string packDir, FileInfo input, DirectoryInfo outDir)
    {
        // Path.Join preserves the supplied base path even if a later segment looks rooted;
        // all appended artifact names below are fixed trusted leaf names.
        var packPath = Path.Join(packDir, "pack.yaml");
        if (!File.Exists(packPath)) Fail($"Missing pack.yaml: {packPath}");
        if (!input.Exists) Fail($"Missing input file: {input.FullName}");

        var pack = PolicyEngine.LoadPack(packPath);
        var scopedTypedRun = pack.spec.policy.evaluation_profile != "legacy-v1";
        // A typed-profile invocation must own a fresh output location: using
        // an existing directory could expose an old receipt after an early
        // error, and make a consumer mistake stale files for current output.
        // Do not delete or rewrite prior evidence on a failed invocation.
        if (scopedTypedRun && Directory.Exists(outDir.FullName))
        {
            FailCode("OUTPUT_DIRECTORY_NOT_FRESH",
                "Typed-profile execution requires a new output directory.");
            return;
        }
        if (!scopedTypedRun) outDir.Create();

        JsonNode inputJson;
        try
        {
            var rawInput = File.ReadAllText(input.FullName);
            // Parse raw bytes BEFORE JsonNode materialization for typed-v1.
            // A JSON object with duplicate property names is ambiguous across
            // consumers and must never be allowed to reach an ALLOW decision.
            if (scopedTypedRun)
            {
                using var rawDocument = JsonDocument.Parse(rawInput);
                RequireUniqueJsonKeys(rawDocument.RootElement);
            }
            inputJson = JsonNode.Parse(rawInput)
                ?? throw new JsonException("Input JSON produced a null document.");
        }
        catch (JsonException ex)
        {
            FailCode("INPUT_JSON_INVALID", ex.Message);
            return;
        }
        catch (InvalidOperationException ex) when (scopedTypedRun)
        {
            FailCode("INPUT_JSON_DUPLICATE_KEY", ex.Message);
            return;
        }

        var runTs = PaygodClock.UtcNowOffset.ToString("o");

        string inputHash;
        try
        {
            inputHash = Hasher.ComputeHash(inputJson);
        }
        catch (InvalidOperationException ex)
        {
            FailCode("CANONICAL_INPUT_REJECTED", ex.Message);
            return;
        }

        // Preserve legacy profile replay while refusing malformed evidence
        // before writing ANY canonical artifacts for explicit typed-v1 Packs.
        // This is only evaluator-type admission; source completeness and truth
        // require external evidence admission under ADR 0003.
        PolicyResult? typedResult = null;
        if (pack.spec.policy.evaluation_profile != "legacy-v1")
        {
            try
            {
                typedResult = PolicyEngine.Evaluate(pack, inputJson);
            }
            catch (InvalidOperationException ex)
            {
                FailCode("POLICY_INPUT_REJECTED", ex.Message);
                return;
            }
        }

        // Create a new output location only after typed evaluation succeeded.
        // This does not authorize concurrent writers; use a unique path per run.
        if (scopedTypedRun) outDir.Create();

        var packDigest = Sha256Hex(File.ReadAllBytes(packPath));
        var packObj = new { name = pack.metadata.name, version = pack.metadata.version, path = packDir, digest_sha256 = packDigest };

        var plan = new
        {
            api_version = "paygod/v1", kind = "PlanReport", generated_at = runTs, pack = packObj,
            input = new { path = input.FullName, canonical_hash = inputHash }, settings = new { }
        };
        var planPath = Path.Join(outDir.FullName, "plan.json");
        WriteJson(planPath, plan);

        var result = typedResult ?? PolicyEngine.Evaluate(pack, inputJson);
        var findings = new List<object>();
        if (result.Decision == "flag")
            findings.Add(new { kind = "flag", severity = "medium", code = "PACK_FLAG", message = result.Reason, rule_name = result.RuleName, evidence_refs = Array.Empty<string>() });
        else if (result.Decision == "error" || result.Decision == "unknown")
            findings.Add(new { kind = "flag", severity = "high", code = "EVAL_ERROR", message = result.Decision == "unknown" ? "No policy rules matched." : result.Reason, rule_name = result.RuleName, evidence_refs = Array.Empty<string>() });

        var findingsReport = new { api_version = "paygod/v1", kind = "FindingsReport", generated_at = runTs, pack = packObj, findings };
        var findingsPath = Path.Join(outDir.FullName, "findings.json");
        WriteJson(findingsPath, findingsReport);

        var verdict = result.Decision == "unknown" ? "error" : result.Decision;
        var ledgerPath = Path.Join(outDir.FullName, "ledger.jsonl");
        if (verdict is "allow" or "deny" or "flag" or "error") AppendLedger(ledgerPath, packObj, inputHash, verdict, result, runTs);

        // The manifest locks the evidence payload. receipt.json is deliberately NOT a
        // manifest member: the receipt binds to the finalized manifest. Including the
        // receipt in the manifest while the receipt contains manifest_sha256 creates an
        // impossible circular hash dependency.
        var payloadFiles = new[] { new FileInfo(planPath), new FileInfo(findingsPath), new FileInfo(ledgerPath) }
            .Where(f => f.Exists).ToArray();
        var fileEntries = payloadFiles.OrderBy(f => f.Name, StringComparer.Ordinal).Select(f => new
        {
            name = f.Name, sha256 = Sha256FileHex(f.FullName), bytes = f.Length
        }).ToArray();
        var bundleDigest = ComputeBundleDigest(fileEntries);

        var manifest = new
        {
            api_version = "paygod/v1", kind = "Manifest", generated_at = runTs, pack = packObj,
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
        var manifestPath = Path.Join(outDir.FullName, "manifest.json");
        WriteJson(manifestPath, manifest);
        var manifestSha = Sha256FileHex(manifestPath);

        // Receipt is the deterministic execution certificate over the immutable manifest.
        var clockValue = Environment.GetEnvironmentVariable("PAYGOD_CLOCK") ?? "unset";
        var runnerImage = Environment.GetEnvironmentVariable("PAYGOD_RUNNER_IMAGE") ?? "paygod/runner:dev";
        var runnerDigest = Environment.GetEnvironmentVariable("PAYGOD_RUNNER_DIGEST") ?? "unknown";
        // A bind-mounted Docker output directory already exists. For typed-v1
        // the CLI requires a fresh *child* path, so mount the existing parent,
        // not the target directory. Preserve historical replay commands.
        var replayMount = scopedTypedRun
            ? "-v \"<OUT_PARENT_DIR>:/out-parent:rw\""
            : "-v \"<OUT_DIR>:/out:rw\"";
        var replayOut = scopedTypedRun
            ? "/out-parent/<NEW_RUN_SUBDIR>"
            : "/out";

        var receipt = new
        {
            api_version = "paygod/v1", kind = "Receipt", spec_version = "0.2.0", generated_at = clockValue,
            clock = new { value = clockValue, source = "env:PAYGOD_CLOCK" },
            canonicalization = new { json = Canonicalizer.ProfileName },
            runner = new { image = runnerImage, image_digest = runnerDigest },
            pack = packObj,
            input = new { canonical_hash = inputHash },
            bundle = new { bundle_digest = bundleDigest, manifest_sha256 = manifestSha, files = fileEntries },
            verdict = new { value = verdict, rule_name = result.RuleName, reason = result.Reason },
            replay = new
            {
                command = $"docker run --rm -e PAYGOD_CLOCK={clockValue} -e PAYGOD_STRICT=1 " +
                          $"-v \"<PACK_DIR>:/pack:ro\" -v \"<INPUT_FILE>:/input/input.json:ro\" {replayMount} " +
                          $"{runnerImage} run --pack /pack --input /input/input.json --out {replayOut}"
            }
        };
        WriteJson(Path.Join(outDir.FullName, "receipt.json"), receipt);
        Console.WriteLine("OK: Run complete.");
    }

    // Lexical object-key admission is scoped to the opted-in typed-v1 profile.
    // This does not prove source authenticity, scanner completeness, or
    // authorized release; those must be admitted independently.
    private static void RequireUniqueJsonKeys(JsonElement element)
    {
        switch (element.ValueKind)
        {
            case JsonValueKind.Object:
                var seen = new HashSet<string>(StringComparer.Ordinal);
                foreach (var property in element.EnumerateObject())
                {
                    if (!seen.Add(property.Name))
                        throw new InvalidOperationException(
                            "Duplicate JSON property name in typed-v1 input.");
                    RequireUniqueJsonKeys(property.Value);
                }
                break;
            case JsonValueKind.Array:
                foreach (var item in element.EnumerateArray())
                    RequireUniqueJsonKeys(item);
                break;
        }
    }

    private static void AppendLedger(string ledgerPath, object packObj, string inputHash, string verdict, PolicyResult result, string runTs)
    {
        var zeros = new string('0', 64);
        var (prevHash, nextIndex) = ReadLedgerTail(ledgerPath, zeros);
        var data = new { verdict, rule_name = result.RuleName, reason = result.Reason, pack = packObj, input_hash = inputHash, evidence_refs = Array.Empty<string>() };
        var hashInput = new JsonObject
        {
            ["previous_hash"] = prevHash,
            ["timestamp"] = runTs,
            ["data"] = JsonNode.Parse(JsonSerializer.Serialize(data))!
        };
        var recordHash = Hasher.ComputeHash(hashInput);
        var entry = new { entry_index = nextIndex, timestamp = runTs, previous_hash = prevHash, data, record_hash = recordHash };
        File.AppendAllText(ledgerPath, JsonSerializer.Serialize(entry) + "\n", new UTF8Encoding(false));
    }

    private static (string prevHash, int nextIndex) ReadLedgerTail(string ledgerPath, string genesis)
    {
        if (!File.Exists(ledgerPath)) return (genesis, 0);
        var lastLine = File.ReadLines(ledgerPath).Where(line => !string.IsNullOrWhiteSpace(line)).LastOrDefault();
        if (lastLine is null) return (genesis, 0);
        using var doc = JsonDocument.Parse(lastLine);
        var root = doc.RootElement;
        return (root.GetProperty("record_hash").GetString() ?? genesis, root.GetProperty("entry_index").GetInt32() + 1);
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
        var sb = new StringBuilder();
        foreach (var f in fileEntries)
        {
            sb.Append(f.name); sb.Append('='); sb.Append(f.sha256); sb.Append('\n');
        }
        return Sha256Hex(Encoding.UTF8.GetBytes(sb.ToString()));
    }

    private static void WriteJson(string path, object obj)
    {
        File.WriteAllText(path, JsonSerializer.Serialize(obj, new JsonSerializerOptions { WriteIndented = true }), new UTF8Encoding(false));
    }

    private static void Fail(string msg)
    {
        Console.Error.WriteLine($"ERR: {msg}");
        Environment.Exit(2);
    }

    private static void FailCode(string code, string message)
    {
        Console.Error.WriteLine($"ERR[{code}]: {message}");
        Environment.Exit(2);
    }
}
