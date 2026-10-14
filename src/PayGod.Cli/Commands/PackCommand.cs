using System.CommandLine;
using System.Text;
using System.Text.RegularExpressions;

namespace PayGod.Cli.Commands;

public static class PackCommand
{
    public static Command Create()
    {
        var command = new Command("pack", "Pack tools.");

        var init = new Command("init", "Generate a new pack skeleton (pack.yaml + tests + README).");
        var nameOpt = new Option<string>("--name", "Pack name (directory name).") { IsRequired = true };
        var providerOpt = new Option<string?>("--provider", "Provider name for provider-specific packs (aws|azure|gcp). If omitted, pack is created under packs/core.");
        var forceOpt = new Option<bool>("--force", "Overwrite existing directory.");

        init.AddOption(nameOpt);
        init.AddOption(providerOpt);
        init.AddOption(forceOpt);

        init.SetHandler((string name, string? provider, bool force) =>
        {
            RunInit(name, provider, force);
        }, nameOpt, providerOpt, forceOpt);

        command.AddCommand(init);
        return command;
    }

    private static void RunInit(string name, string? provider, bool force)
    {
        // Pack names are single path components. --force must never be able to
        // traverse out of packs/ or recursively delete an arbitrary directory.
        if (string.IsNullOrEmpty(name) ||
            !Regex.IsMatch(name, @"\A[a-z][a-z0-9-]{0,62}\z", RegexOptions.CultureInvariant))
        {
            Console.Error.WriteLine("Invalid Pack name. Use a lowercase slug: a-z, 0-9, hyphen; start with a letter (max 63 characters).");
            Environment.Exit(2);
            return;
        }

        var packDir = string.IsNullOrWhiteSpace(provider)
            ? Path.Combine("packs", "core", name)
            : Path.Combine("packs", "providers", provider.Trim().ToLowerInvariant(), name);

        if (!string.IsNullOrWhiteSpace(provider))
        {
            var p = provider.Trim().ToLowerInvariant();
            if (p != "aws" && p != "azure" && p != "gcp")
            {
                Console.Error.WriteLine("❌ Invalid --provider. Allowed: aws|azure|gcp.");
                Environment.Exit(2);
            }
        }

        if (Directory.Exists(packDir))
        {
            if ((File.GetAttributes(packDir) & FileAttributes.ReparsePoint) != 0)
            {
                Console.Error.WriteLine("Refusing to overwrite a symlink/reparse-point Pack directory.");
                Environment.Exit(2);
                return;
            }

            if (!force)
            {
                Console.Error.WriteLine($"❌ Directory exists: {packDir}. Use --force to overwrite.");
                Environment.Exit(2);
            }
            Directory.Delete(packDir, recursive: true);
        }

        Directory.CreateDirectory(Path.Combine(packDir, "tests"));

        var packYaml = $$"""
api_version: "paygod/v1"
kind: Pack
metadata:
  name: "{{name}}"
  version: "0.1.0"
  description: "Describe what this pack enforces."
  maintainer: "you@example.com"
  tags: ["mvp"]

spec:
  inputs:
    - name: "input"
      type: "observation"
      source: "custom"
      schema:
        type: "object"
        required: ["block"]
        additionalProperties: false
        properties:
          block: { type: "boolean" }

  policy:
    rules:
      - name: "deny-when-blocked"
        condition: "input.input.block == true"
        decision: "deny"
        reason: "Blocked by policy (block==true)."

      - name: "allow-when-not-blocked"
        condition: "input.input.block == false"
        decision: "allow"
        reason: "Allowed by policy for admitted boolean block=false."
""";

        var casesYaml = """
version: "1.0.0"
cases:
  - name: "allow_minimal"
    description: "Allow when block flag is false."
    input:
      input:
        block: false
    expected:
      decision: "allow"
      matchers:
        - field: "reason"
          operator: "contains"
          value: "Allowed by policy"

  - name: "deny_minimal"
    description: "Deny when block flag is true."
    input:
      input:
        block: true
    expected:
      decision: "deny"
      matchers:
        - field: "reason"
          operator: "contains"
          value: "Blocked by policy"
""";

        var readme = $$"""
# {{name}} (Pack)

## Scope
- **Core pack:** `packs/core/{{name}}` (cloud-agnostic)
- **Provider pack:** `packs/providers/<cloud>/{{name}}` (provider-specific)

## Structural admission and policy tests

This generator produces a template, **not** a production admission pipeline.
First validate an actual input's required fields/types using the optional
structural-only EIK check:

```bash
python3 tools/eik_admit.py --pack {{packDir}} --input <input.json>
dotnet run --project src/PayGod.Cli -- test --pack {{packDir}}
```

The admission command must not be interpreted as scanner completion,
authenticity, sufficient provenance, legal mandate, or authorization to release.
You must establish required external source status, freshness and permissions
before invoking canonical `run`; missing mandatory facts are
`WITHHELD / NOT RUN` in the **external workflow**, not Kernel verdicts.
The generic Kernel `run` does not enforce this Pack's embedded input schema.
""";

        File.WriteAllText(Path.Combine(packDir, "pack.yaml"), packYaml, new UTF8Encoding(false));
        File.WriteAllText(Path.Combine(packDir, "tests", "cases.yaml"), casesYaml, new UTF8Encoding(false));
        File.WriteAllText(Path.Combine(packDir, "README.md"), readme, new UTF8Encoding(false));

        Console.WriteLine($"✅ Created pack skeleton at: {packDir}");
    }
}
