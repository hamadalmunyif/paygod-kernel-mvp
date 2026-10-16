using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using Xunit;

namespace PayGod.Tests;

/// <summary>
/// RED TESTS on exact pinned baseline for Issue #111.
/// These are assertions of desired fail-closed typed-equality behavior,
/// not an assertion that the existing Kernel already satisfies it.
/// Only the literal typed JSON boolean false may satisfy == false.
/// Do not merge while red or silently change historical DSL semantics:
/// compare accepted pack compatibility and seek ADR / owner review.
/// </summary>
public class PolicyExpressionTypeSafetyTests
{
    [Theory]
    [InlineData("{\"input\":{\"block\":false}}", true)]
    [InlineData("{\"input\":{\"block\":true}}", false)]
    [InlineData("{\"input\":{}}", false)]
    [InlineData("{\"input\":{\"block\":null}}", false)]
    [InlineData("{\"input\":{\"block\":\"false\"}}", false)]
    [InlineData("{\"input\":{\"block\":0}}", false)]
    [InlineData("{\"input\":{\"block\":{}}}", false)]
    [InlineData("{}", false)]
    public void EqualityAgainstBooleanFalse_RequiresPresentTypedBoolean(
        string json,
        bool expected)
    {
        var root = JsonNode.Parse(json)!;
        Assert.Equal(expected, PolicyExpression.Evaluate(
            "input.input.block == false", root));
    }

    [Theory]
    [InlineData("{\"input\":{\"block\":true}}", true)]
    [InlineData("{\"input\":{\"block\":false}}", false)]
    [InlineData("{\"input\":{}}", false)]
    [InlineData("{\"input\":{\"block\":\"true\"}}", false)]
    [InlineData("{\"input\":{\"block\":1}}", false)]
    public void EqualityAgainstBooleanTrue_RequiresPresentTypedBoolean(
        string json,
        bool expected)
    {
        var root = JsonNode.Parse(json)!;
        Assert.Equal(expected, PolicyExpression.Evaluate(
            "input.input.block == true", root));
    }

    [Theory]
    [InlineData("{\"input\":{\"value\":0}}", true)]
    [InlineData("{\"input\":{\"value\":\"0\"}}", false)]
    [InlineData("{\"input\":{\"value\":false}}", false)]
    [InlineData("{\"input\":{}}", false)]
    public void NumericEquality_RejectsStringAndBooleanCoercion(
        string json,
        bool expected)
    {
        var root = JsonNode.Parse(json)!;
        Assert.Equal(expected, PolicyExpression.Evaluate(
            "input.input.value == 0", root));
    }
}
