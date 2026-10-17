using System.Text.Json;
using System.Text.Json.Nodes;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;
using YamlDotNet.RepresentationModel;

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
        // The Pack JSON Schema sets spec.policy.additionalProperties=false,
        // but YamlDotNet's IgnoreUnmatchedProperties would otherwise silently
        // ignore a misspelled evaluation_profile and fall back to legacy-v1.
        // Check policy keys for EVERY Pack, including legacy, BEFORE producing
        // a decision. This is Pack authoring admission, not source provenance.
        ValidatePolicyPropertyNames(content);
        return YamlDeserializer.Deserialize<PackDefinition>(content);
    }

    private static void ValidatePolicyPropertyNames(string rawYaml)
    {
        var stream = new YamlStream();
        using var reader = new StringReader(rawYaml);
        stream.Load(reader);
        if (stream.Documents.Count != 1 ||
            stream.Documents[0].RootNode is not YamlMappingNode root ||
            !root.Children.TryGetValue(new YamlScalarNode("spec"), out var spec) ||
            spec is not YamlMappingNode specMap ||
            !specMap.Children.TryGetValue(new YamlScalarNode("policy"), out var policy) ||
            policy is not YamlMappingNode policyMap)
            throw new InvalidOperationException("Pack must have one spec.policy mapping.");

        foreach (var key in policyMap.Children.Keys)
        {
            if (key is not YamlScalarNode scalar ||
                scalar.Value is not ("rules" or "evaluation_profile"))
                throw new InvalidOperationException(
                    "Unknown spec.policy field: only rules and evaluation_profile are permitted.");
        }

        var rulesKey = new YamlScalarNode("rules");
        if (!policyMap.Children.TryGetValue(rulesKey, out var rulesNode))
            throw new InvalidOperationException("Pack spec.policy.rules is required.");

        var profile = "legacy-v1";
        if (policyMap.Children.TryGetValue(
                new YamlScalarNode("evaluation_profile"), out var profileNode))
        {
            if (profileNode is not YamlScalarNode profileScalar ||
                string.IsNullOrWhiteSpace(profileScalar.Value))
                throw new InvalidOperationException(
                    "Pack spec.policy.evaluation_profile must be a non-empty scalar.");
            profile = profileScalar.Value!;
        }

        // Preserve historical legacy-v1 deserialization behavior. The stricter
        // rule-mapping admission below is version-gated to typed-v1 only.
        if (profile != "typed-v1") return;

        if (rulesNode is not YamlSequenceNode rules)
            throw new InvalidOperationException(
                "typed-v1 spec.policy.rules must be a sequence.");

        var permittedRuleFields = new HashSet<string>(StringComparer.Ordinal)
        {
            "name", "condition", "decision", "reason"
        };

        for (var index = 0; index < rules.Children.Count; index++)
        {
            if (rules.Children[index] is not YamlMappingNode ruleMap)
                throw new InvalidOperationException(
                    $"typed-v1 policy rule[{index}] must be a mapping.");

            foreach (var key in ruleMap.Children.Keys)
            {
                if (key is not YamlScalarNode scalar ||
                    string.IsNullOrEmpty(scalar.Value) ||
                    !permittedRuleFields.Contains(scalar.Value))
                    throw new InvalidOperationException(
                        $"Unknown typed-v1 policy rule[{index}] field.");
            }

            foreach (var required in permittedRuleFields)
            {
                if (!ruleMap.Children.TryGetValue(
                        new YamlScalarNode(required), out var value) ||
                    value is not YamlScalarNode scalar ||
                    string.IsNullOrWhiteSpace(scalar.Value))
                    throw new InvalidOperationException(
                        $"typed-v1 policy rule[{index}].{required} is required and must be non-empty.");
            }

            var decision = ((YamlScalarNode)ruleMap.Children[
                new YamlScalarNode("decision")]).Value;
            if (decision is not ("allow" or "deny" or "flag" or "error"))
                throw new InvalidOperationException(
                    $"typed-v1 policy rule[{index}].decision is unsupported.");
        }
    }

    public static PolicyResult Evaluate(PackDefinition pack, JsonNode? input)
    {
        if (input == null) return new PolicyResult { Decision = "error", Reason = "Input is null" };

        var profile = pack.spec.policy.evaluation_profile;
        if (profile is not ("legacy-v1" or "typed-v1"))
            throw new InvalidOperationException($"Unsupported policy evaluation profile: {profile}");

        // Preflight the WHOLE new-version policy grammar, even rules made
        // unreachable by an earlier match. A malformed tail is never safe
        // solely because the first matching rule would return allow.
        if (profile == "typed-v1")
        {
            foreach (var rule in pack.spec.policy.rules)
                PolicyExpression.ValidateSyntax(rule.condition);
        }

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

