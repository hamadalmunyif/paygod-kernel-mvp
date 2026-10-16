using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using Xunit;

namespace PayGod.Tests;

/// <summary>
/// Typed-comparison security regression for Issue #111.
/// The earlier RED witness remains preserved at commit d2228a6.
/// A missing/invalid fact must raise an evaluation error, never become an
/// "allow" because a policy negated a false comparison.
/// </summary>
public class PolicyExpressionTypeSafetyTests
{
    [Theory]
    [InlineData("{\"input\":{\"block\":false}}", true)]
    [InlineData("{\"input\":{\"block\":true}}", false)]
    public void EqualityAgainstFalse_UsesActualBoolean(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate("input.input.block == false", json));
    }

    [Theory]
    [InlineData("{\"input\":{\"block\":true}}", true)]
    [InlineData("{\"input\":{\"block\":false}}", false)]
    public void EqualityAgainstTrue_UsesActualBoolean(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate("input.input.block == true", json));
    }

    [Theory]
    [InlineData("{\"input\":{\"block\":0}}", true)]
    [InlineData("{\"input\":{\"block\":1}}", false)]
    public void EqualityAgainstNumber_UsesActualNumber(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate("input.input.block == 0", json));
    }

    [Theory]
    [InlineData("{\"input\":{}}")]
    [InlineData("{\"input\":{\"block\":null}}")]
    [InlineData("{\"input\":{\"block\":\"false\"}}")]
    [InlineData("{\"input\":{\"block\":0}}")]
    [InlineData("{\"input\":{\"block\":{}}}")]
    [InlineData("{}")]
    public void EqualityAgainstFalse_WithMissingOrWrongTypedInput_IsError(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.input.block == false", json));
    }

    [Theory]
    [InlineData("{\"input\":{}}")]
    [InlineData("{\"input\":{\"block\":\"true\"}}")]
    [InlineData("{\"input\":{\"block\":1}}")]
    [InlineData("{\"input\":{\"block\":null}}")]
    public void EqualityAgainstTrue_WithMissingOrWrongTypedInput_IsError(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.input.block == true", json));
    }

    [Theory]
    [InlineData("{\"input\":{}}")]
    [InlineData("{\"input\":{\"block\":\"0\"}}")]
    [InlineData("{\"input\":{\"block\":false}}")]
    [InlineData("{\"input\":{\"block\":null}}")]
    public void EqualityAgainstNumber_WithMissingOrWrongTypedInput_IsError(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.input.block == 0", json));
    }

    [Theory]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":98}]}}")]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":98,\"status\":null}]}}")]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":98,\"status\":false}]}}")]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":\"98\",\"status\":\"active\"}]}}")]
    [InlineData("{\"scan_report\":{}}")]
    public void NegatedCveAny_DoesNotAllowMalformedEvidence(string json)
    {
        const string allowCondition =
            "not input.scan_report.vulnerabilities.any(v => v.cvss_score_x10 >= 70 and v.status != 'fixed')";
        Assert.Throws<InvalidOperationException>(() => Evaluate(allowCondition, json));
    }

    [Fact]
    public void NegatedCveAny_CompleteEmptyArray_MatchesButIsNotSourceAdmission()
    {
        // This only shows DSL evaluation; the *external* scan-completion
        // proof and true schema admission are still separately required.
        Assert.True(Evaluate(
            "not input.scan_report.vulnerabilities.any(v => v.cvss_score_x10 >= 70 and v.status != 'fixed')",
            "{\"scan_report\":{\"vulnerabilities\":[]}}"));
    }

    [Theory]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":98,\"status\":\"active\"}]}}", false)]
    [InlineData("{\"scan_report\":{\"vulnerabilities\":[{\"cvss_score_x10\":32,\"status\":\"active\"}]}}", true)]
    public void NegatedCveAny_ValidTypedCasesRemainCompatible(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate(
            "not input.scan_report.vulnerabilities.any(v => v.cvss_score_x10 >= 70 and v.status != 'fixed')",
            json));
    }

    [Fact]
    public void ComparisonNotEqual_MissingInput_IsErrorEvenInAllowRule()
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.iam_event.policy_attached != 'AdministratorAccess'",
                "{\"iam_event\":{}}"));
    }

    [Theory]
    [InlineData("{\"input\":{}}")]
    [InlineData("{\"input\":{\"block\":null}}")]
    [InlineData("{\"input\":{\"block\":\"false\"}}")]
    [InlineData("{\"input\":{\"block\":0}}")]
    [InlineData("{\"input\":{\"block\":[]}}")]
    [InlineData("{\"input\":{\"block\":{}}}")]
    public void Negation_MissingOrNonBoolean_CannotBecomeAllow(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("not input.input.block", json));
    }

    [Theory]
    [InlineData("{\"input\":{\"block\":false}}", true)]
    [InlineData("{\"input\":{\"block\":true}}", false)]
    public void Negation_PresentBoolean_IsEvaluated(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate("not input.input.block", json));
    }

    [Theory]
    [InlineData("{\"input\":{}}")]
    [InlineData("{\"input\":{\"block\":\"true\"}}")]
    [InlineData("{\"input\":{\"block\":1}}")]
    public void StandalonePath_MissingOrNonBoolean_IsErrorInTypedProfile(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.input.block", json));
    }

    [Fact]
    public void LegacyProfile_NegatedMissingPathBehaviorIsPinnedForHistoricalReplayOnly()
    {
        // This is not approval to admit missing source data.
        var root = JsonNode.Parse("{\"input\":{}}")!;
        Assert.True(PolicyExpression.Evaluate("not input.input.block", root));
    }

    [Fact]
    public void TypedProfile_MissingBooleanInAnyPredicate_IsError()
    {
        const string policy = "input.items.any(v => v.required)";
        const string raw = "{\"items\":[{\"required\":\"true\"}]}";
        Assert.Throws<InvalidOperationException>(() => Evaluate(policy, raw));
    }

    [Fact]
    public void OptedInPack_RejectsWrongTypedBooleanBeforeAllow()
    {
        var pack = MakePack("typed-v1");
        var root = JsonNode.Parse("{\"input\":{\"block\":\"false\"}}")!;
        Assert.Throws<InvalidOperationException>(() => PolicyEngine.Evaluate(pack, root));
    }

    [Fact]
    public void OptedInPack_UsesTypedBooleanForAllow()
    {
        var pack = MakePack("typed-v1");
        var root = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Equal("allow", PolicyEngine.Evaluate(pack, root).Decision);
    }

    [Fact]
    public void UnspecifiedProfile_PreservesLegacyBehaviorForHistoricalWitnesses()
    {
        var pack = MakePack("legacy-v1");
        var root = JsonNode.Parse("{\"input\":{\"block\":\"false\"}}")!;
        // Record existing behavior *only* to prevent historical replay drift.
        // Legacy coercion is not permission to admit external untyped input.
        Assert.Equal("allow", PolicyEngine.Evaluate(pack, root).Decision);
    }

    [Fact]
    public void UnsupportedProfile_IsRejected()
    {
        var pack = MakePack("unsupported");
        var root = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Throws<InvalidOperationException>(() => PolicyEngine.Evaluate(pack, root));
    }

    private static PackDefinition MakePack(string profile) => new()
    {
        spec = new PackSpec
        {
            policy = new PackPolicy
            {
                evaluation_profile = profile,
                rules = new List<PolicyRule>
                {
                    new()
                    {
                        name = "allow-unblocked",
                        condition = "input.input.block == false",
                        decision = "allow",
                        reason = "Only properly typed boolean false in typed profile."
                    }
                }
            }
        }
    };

    private static bool Evaluate(string condition, string input)
    {
        var root = JsonNode.Parse(input)!;
        return PolicyExpression.Evaluate(condition, root, strictTypes: true);
    }
}
