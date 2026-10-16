using System.Text.Json;
using System.Text.Json.Nodes;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace PayGod.Cli.Core;

// Models matching pack.yaml
public class PackDefinition
{
    public string api_version { get; set; } = "";
    public string kind { get; set; } = "";
    public PackMetadata metadata { get; set; } = new();
    public PackSpec spec { get; set; } = new();
}

public class PackMetadata
{
    public string name { get; set; } = "";
    public string version { get; set; } = "";
}

public class PackSpec
{
    public PackPolicy policy { get; set; } = new();
}

public class PackPolicy
{
    // Explicitly opt into strict typed semantics; existing packs retain legacy behavior.
    public string evaluation_profile { get; set; } = "legacy-v1";
    public List<PolicyRule> rules { get; set; } = new();
}

public class PolicyRule
{
    public string name { get; set; } = "";
    public string condition { get; set; } = "";
    public string decision { get; set; } = "";
    public string reason { get; set; } = "";
}

public class PolicyResult
{
    public string Decision { get; set; } = "unknown";
    public string Reason { get; set; } = "";
    public string RuleName { get; set; } = "";
}

public static class PolicyEngine
{
    private static readonly IDeserializer YamlDeserializer = new DeserializerBuilder()
        .WithNamingConvention(UnderscoredNamingConvention.Instance)
        .IgnoreUnmatchedProperties()
        .Build();

    public static PackDefinition LoadPack(string path)
    {
        var content = File.ReadAllText(path);
        return YamlDeserializer.Deserialize<PackDefinition>(content);
    }

    public static PolicyResult Evaluate(PackDefinition pack, JsonNode? input)
    {
        if (input == null) return new PolicyResult { Decision = "error", Reason = "Input is null" };

        var profile = pack.spec.policy.evaluation_profile;
        if (profile is not ("legacy-v1" or "typed-v1"))
            throw new InvalidOperationException($"Unsupported policy evaluation profile: {profile}");

        foreach (var rule in pack.spec.policy.rules)
        {
            if (EvaluateCondition(rule.condition, input, profile))
            {
                return new PolicyResult 
                { 
                    Decision = rule.decision, 
                    Reason = rule.reason,
                    RuleName = rule.name
                };
            }
        }

        return new PolicyResult { Decision = "unknown", Reason = "No policy rules matched." };
    }

    private static bool EvaluateCondition(string condition, JsonNode input, string profile)
    {
        return PolicyExpression.Evaluate(condition, input, strictTypes: profile == "typed-v1");
    }
}

