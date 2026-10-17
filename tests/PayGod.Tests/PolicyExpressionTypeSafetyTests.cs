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

    [Theory]
    [InlineData(">", "{\"input\":{\"block\":false}}")]
    [InlineData(">=", "{\"input\":{\"block\":true}}")]
    [InlineData("<", "{\"input\":{\"block\":true}}")]
    [InlineData("<=", "{\"input\":{\"block\":false}}")]
    public void TypedBooleanOrdering_UnderNegation_ThrowsInsteadOfAllow(string op, string json)
    {
        // Without a throw, unsupported ordering fell through to false;
        // 'not (false)' could incorrectly satisfy an allow rule.
        Assert.Throws<InvalidOperationException>(() =>
            Evaluate($"not (input.input.block {op} false)", json));
    }

    [Theory]
    [InlineData("{\"input\":{\"block\":false}}", true)]
    [InlineData("{\"input\":{\"block\":true}}", false)]
    public void TypedBooleanEquality_StillWorksWithExplicitTypes(string json, bool expected)
    {
        Assert.Equal(expected, Evaluate("input.input.block == false", json));
    }

    [Theory]
    [InlineData("input.input.block == false && input.input.required")]
    [InlineData("input.input.block == false || true")]
    [InlineData("input.input.block == false #ignored-condition")]
    public void TypedPolicy_UnexpectedLexerCharacter_CannotTruncateAllowRule(string expression)
    {
        const string source = "{\"input\":{\"block\":false,\"required\":false}}";
        Assert.Throws<InvalidOperationException>(() => Evaluate(expression, source));
    }

    [Theory]
    [InlineData("input.input.count == 1e999")]
    [InlineData("input.input.count == 1-1")]
    public void TypedPolicy_InvalidNumericLiteral_CannotBecomeZero(string expression)
    {
        const string source = "{\"input\":{\"count\":0}}";
        Assert.Throws<InvalidOperationException>(() => Evaluate(expression, source));
    }

    [Fact]
    public void TypedPolicy_UnterminatedStringLiteral_IsError()
    {
        Assert.Throws<InvalidOperationException>(() =>
            Evaluate("input.input.word == 'open", "{\"input\":{\"word\":\"open\"}}"));
    }

    [Fact]
    public void LegacyLexerBehavior_IsNotSilentlyRewritten()
    {
        var input = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        // Historical replay of legacy-v1 remains deliberately unchanged.
        Assert.True(PolicyExpression.Evaluate("input.input.block == false && trailing", input));
    }

    [Theory]
    [InlineData("input.input.count == 0", true)]
    [InlineData("input.input.count != 0", false)]
    [InlineData("input.input.count < 1", true)]
    [InlineData("input.input.count == 1", false)]
    [InlineData("input.input.count > -1", true)]
    [InlineData("input.input.count == -1", false)]
    public void TypedNumericSafeIntegerComparison_IsExact(string condition, bool expected)
    {
        Assert.Equal(expected, Evaluate(condition, "{\"input\":{\"count\":0}}"));
    }

    [Theory]
    [InlineData("input.input.count == 0.0000000001")]
    [InlineData("input.input.count != 0.0000000001")]
    [InlineData("input.input.count == 1.0")]
    [InlineData("input.input.count == 1e0")]
    [InlineData("input.input.count == 9007199254740992")]
    public void TypedPolicy_RejectsFractionalExponentAndUnsafeLiterals(string expression)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate(expression, "{\"input\":{\"count\":0}}"));
    }

    [Theory]
    [InlineData("{\"input\":{\"count\":1.0}}")]
    [InlineData("{\"input\":{\"count\":1e0}}")]
    [InlineData("{\"input\":{\"count\":9007199254740992}}")]
    public void TypedNumericInput_RejectsNonCanonicalIntegerForms(string json)
    {
        Assert.Throws<InvalidOperationException>(
            () => Evaluate("input.input.count == 1", json));
    }

    [Fact]
    public void TypedNumericSafeIntegerBoundary_ComparedWithoutDoubleRounding()
    {
        const string atBoundary = "{\"input\":{\"count\":9007199254740991}}";
        Assert.True(Evaluate("input.input.count == 9007199254740991", atBoundary));
        Assert.False(Evaluate("input.input.count == 9007199254740990", atBoundary));
    }

    [Fact]
    public void LegacyProfile_FractionalEpsilonRemainsPinnedForReplay()
    {
        var root = JsonNode.Parse("{\"input\":{\"count\":0}}")!;
        Assert.True(PolicyExpression.Evaluate("input.input.count == 0.0000000001", root));
    }

    [Theory]
    [InlineData("input.input.block == true && ignored")]
    [InlineData("input.input.block == true # unexpected tail")]
    [InlineData("input.input.block == 1e999")]
    [InlineData("input.input.word == 'unfinished")]
    public void TypedProfile_RejectsMalformedRuleEvenWhenEarlierAllowMatches(string invalidRule)
    {
        var pack = MakePack("typed-v1");
        pack.spec.policy.rules.Add(new PolicyRule
        {
            name = "not-executed-but-invalid",
            condition = invalidRule,
            decision = "deny",
            reason = "Invalid syntax must block a preceding allow too."
        });
        var root = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Throws<InvalidOperationException>(() => PolicyEngine.Evaluate(pack, root));
    }

    [Fact]
    public void LegacyProfile_UnreachedInvalidRuleKeepsHistoricalShortCircuit()
    {
        var pack = MakePack("legacy-v1");
        pack.spec.policy.rules.Add(new PolicyRule
        {
            name = "legacy-unreached",
            condition = "input.input.block == true && ignored",
            decision = "deny",
            reason = "Old semantics pinned for historical replay only."
        });
        var root = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Equal("allow", PolicyEngine.Evaluate(pack, root).Decision);
    }

    [Theory]
    [InlineData(false, false)]
    [InlineData(true, true)]
    public void TypedNestedAny_ReusedLambdaRestoresOuterBinding(bool outerRequired, bool expected)
    {
        var json = "{\"groups\":[{\"required\":" +
                   (outerRequired ? "true" : "false") +
                   ",\"items\":[{\"ok\":true,\"required\":true}]}]}";
        const string condition = "input.groups.any(v => v.items.any(v => v.ok) and v.required)";
        Assert.Equal(expected, Evaluate(condition, json));
        if (!outerRequired)
        {
            // Historical lexical-leak behavior is preserved only for replay.
            var original = JsonNode.Parse(json)!;
            Assert.True(PolicyExpression.Evaluate(condition, original));
        }
    }

    [Fact]
    public void TypedNestedAny_ReservedInputVariableRejected()
    {
        const string json = "{\"groups\":[{\"required\":true}]}";
        Assert.Throws<InvalidOperationException>(() =>
            Evaluate("input.groups.any(input => input.required)", json));
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

    [Fact]
    public void TypedProfile_ReservedLambdaInUnreachedRule_FailsSyntaxPreflight()
    {
        var pack = MakePack("typed-v1");
        pack.spec.policy.rules.Add(new PolicyRule
        {
            name = "hidden-reserved-lambda",
            condition = "input.groups.any(input => true)",
            decision = "deny",
            reason = "Reserved input root must be rejected during grammar preflight."
        });
        var root = JsonNode.Parse("{\"input\":{\"block\":false},\"groups\":[]}")!;
        Assert.Throws<InvalidOperationException>(() => PolicyEngine.Evaluate(pack, root));
    }

    [Theory]
    [InlineData("evaluation_profıle")]
    [InlineData("evaluation_profiIe")]
    [InlineData("evaluation_profile_extra")]
    public void PackYaml_UnknownPolicyKey_DoesNotSilentlyUseLegacy(string key)
    {
        var temp = Path.GetTempFileName();
        try
        {
            var yaml = "api_version: paygod/v1\n" +
                       "kind: Pack\n" +
                       "metadata:\n  name: guard-test\n  version: 2.0.0\n" +
                       "spec:\n  policy:\n    " + key + ": typed-v1\n" +
                       "    rules:\n      - name: allow\n" +
                       "        condition: \"input.input.block == false\"\n" +
                       "        decision: allow\n        reason: regression\n";
            File.WriteAllText(temp, yaml);
            Assert.Throws<InvalidOperationException>(() => PolicyEngine.LoadPack(temp));
        }
        finally
        {
            File.Delete(temp);
        }
    }

    [Theory]
    [InlineData("legacy-v1")]
    [InlineData("typed-v1")]
    public void PackYaml_ValidDeclaredEvaluationProfile_Parses(string profile)
    {
        var temp = Path.GetTempFileName();
        try
        {
            var yaml = "api_version: paygod/v1\nkind: Pack\n" +
                       "metadata:\n  name: guard-test\n  version: 2.0.0\n" +
                       "spec:\n  policy:\n    evaluation_profile: " + profile + "\n" +
                       "    rules:\n      - name: allow\n" +
                       "        condition: \"input.input.block == false\"\n" +
                       "        decision: allow\n        reason: regression\n";
            File.WriteAllText(temp, yaml);
            Assert.Equal(profile, PolicyEngine.LoadPack(temp).spec.policy.evaluation_profile);
        }
        finally
        {
            File.Delete(temp);
        }
    }

    [Theory]
    [InlineData("true > false")]
    [InlineData("true >= false")]
    [InlineData("true < false")]
    [InlineData("true <= false")]
    [InlineData("true == 1")]
    [InlineData("false != 'false'")]
    [InlineData("1 == '1'")]
    [InlineData("1 != true")]
    [InlineData("'ready' < false")]
    public void TypedWholePolicyPreflight_RejectsUnreachableStaticallyInvalidComparison(
        string invalidRule)
    {
        var pack = MakePack("typed-v1");
        pack.spec.policy.rules.Add(new PolicyRule
        {
            name = "unreachable-but-invalid",
            condition = invalidRule,
            decision = "deny",
            reason = "An earlier allow cannot hide a statically impossible comparison."
        });
        var input = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Throws<InvalidOperationException>(() => PolicyEngine.Evaluate(pack, input));
    }

    [Theory]
    [InlineData("true == false")]
    [InlineData("1 < 2")]
    [InlineData("'a' != 'b'")]
    [InlineData("input.input.block == false")]
    [InlineData("not input.items.any(v => v.required == true)")]
    public void TypedWholePolicyPreflight_KeepsSupportedAndSourceDependentExpressions(
        string expression)
    {
        PolicyExpression.ValidateSyntax(expression);
    }

    [Fact]
    public void LegacyPolicy_UnreachableStaticMismatch_KeepsHistoricalFirstMatch()
    {
        var pack = MakePack("legacy-v1");
        pack.spec.policy.rules.Add(new PolicyRule
        {
            name = "legacy-unreached-mismatch",
            condition = "true > false",
            decision = "deny",
            reason = "Older replay behavior is intentionally not migrated."
        });
        var input = JsonNode.Parse("{\"input\":{\"block\":false}}")!;
        Assert.Equal("allow", PolicyEngine.Evaluate(pack, input).Decision);
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
