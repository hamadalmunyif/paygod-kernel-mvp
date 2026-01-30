using System.CommandLine;
using System.Text;

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
        properties:
          block: { type: "boolean" }

  policy:
    rules:
      - name: "deny-when-blocked"
        condition: "input.input.block == true"
        decision: "deny"
        reason: "Blocked by policy (block==true)."

      - name: "allow-when-not-blocked"
        condition: "input.input.block != true"
        decision: "allow"
        reason: "Allowed by policy (block!=true)."
""";

        var casesYaml = """version: "1.0.0"
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

## Tests
```bash
dotnet run --project src/PayGod.Cli -- test --pack {{packDir}}
```
""";

        File.WriteAllText(Path.Combine(packDir, "pack.yaml"), packYaml, new UTF8Encoding(false));
        File.WriteAllText(Path.Combine(packDir, "tests", "cases.yaml"), casesYaml, new UTF8Encoding(false));
        File.WriteAllText(Path.Combine(packDir, "README.md"), readme, new UTF8Encoding(false));

        Console.WriteLine($"✅ Created pack skeleton at: {packDir}");
    }
}
