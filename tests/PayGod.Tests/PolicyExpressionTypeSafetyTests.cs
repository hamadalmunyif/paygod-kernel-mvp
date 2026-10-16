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

    private static bool Evaluate(string condition, string input)
    {
        var root = JsonNode.Parse(input)!;
        return PolicyExpression.Evaluate(condition, root);
    }
}
