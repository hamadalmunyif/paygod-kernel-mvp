using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using Xunit;

namespace PayGod.Tests;

public class CanonicalizerTests
{
    [Fact]
    public void Canonicalize_NullNode_ReturnsNull()
    {
        JsonNode? node = null;
        Assert.Equal("null", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_EmptyObject_ReturnsEmptyObject()
    {
        Assert.Equal("{}", Canonicalizer.Canonicalize(JsonNode.Parse("{}")));
    }

    [Fact]
    public void Canonicalize_EmptyArray_ReturnsEmptyArray()
    {
        Assert.Equal("[]", Canonicalizer.Canonicalize(JsonNode.Parse("[]")));
    }

    [Fact]
    public void Canonicalize_SimpleObject_SortsKeys()
    {
        var node = JsonNode.Parse("{\"z\":1,\"a\":2,\"m\":3}");
        Assert.Equal("{\"a\":2,\"m\":3,\"z\":1}", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_NestedObject_SortsKeysRecursively()
    {
        var node = JsonNode.Parse("{\"outer\":{\"z\":1,\"a\":2},\"first\":true}");
        Assert.Equal("{\"first\":true,\"outer\":{\"a\":2,\"z\":1}}", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_ArrayOfObjects_MaintainsOrder()
    {
        var node = JsonNode.Parse("[{\"b\":2,\"a\":1},{\"d\":4,\"c\":3}]");
        Assert.Equal("[{\"a\":1,\"b\":2},{\"c\":3,\"d\":4}]", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_StringValues_EscapesCorrectly()
    {
        var node = JsonNode.Parse("{\"text\":\"hello\\nworld\"}");
        Assert.Equal("{\"text\":\"hello\\nworld\"}", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_BooleanValues_ReturnsLowercase()
    {
        var node = JsonNode.Parse("{\"isTrue\":true,\"isFalse\":false}");
        Assert.Equal("{\"isFalse\":false,\"isTrue\":true}", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_SafeIntegerValues_FormatExactly()
    {
        var node = JsonNode.Parse("{\"integer\":42,\"negative\":-7,\"zero\":0}");
        Assert.Equal("{\"integer\":42,\"negative\":-7,\"zero\":0}", Canonicalizer.Canonicalize(node));
    }

    [Theory]
    [InlineData("1.0")]
    [InlineData("1.230")]
    [InlineData("1E2")]
    [InlineData("1e-2")]
    [InlineData("0.1")]
    public void Canonicalize_FloatingPointOrExponentNumber_FailsClosed(string input)
    {
        var node = JsonNode.Parse(input);
        Assert.Throws<InvalidOperationException>(() => Canonicalizer.Canonicalize(node));
    }

    [Theory]
    [InlineData("9007199254740991", "9007199254740991")]
    [InlineData("-9007199254740991", "-9007199254740991")]
    [InlineData("-0", "0")]
    public void Canonicalize_SafeIntegerBoundary_IsAccepted(string input, string expected)
    {
        var node = JsonNode.Parse(input);
        Assert.Equal(expected, Canonicalizer.Canonicalize(node));
    }

    [Theory]
    [InlineData("9007199254740992")]
    [InlineData("-9007199254740992")]
    public void Canonicalize_UnsafeInteger_FailsClosed(string input)
    {
        var node = JsonNode.Parse(input);
        Assert.Throws<InvalidOperationException>(() => Canonicalizer.Canonicalize(node));
    }

    [Theory]
    [InlineData("\"e\u0301\"", "\"e\\u0301\"")]
    [InlineData("\"\u00e9\"", "\"\\u00e9\"")]
    [InlineData("\"سلام\"", "\"\\u0633\\u0644\\u0627\\u0645\"")]
    public void Canonicalize_StringValues_ArePreservedWithoutNormalization(string input, string expected)
    {
        var node = JsonNode.Parse(input);
        Assert.Equal(expected, Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_NonNfcPropertyName_FailsClosed()
    {
        var node = JsonNode.Parse("{\"e\\u0301\":\"value\"}");
        Assert.Throws<InvalidOperationException>(() => Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_NfcPropertyName_IsAccepted()
    {
        var node = JsonNode.Parse("{\"\\u00e9\":\"value\"}");
        Assert.Equal("{\"\\u00e9\":\"value\"}", Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_UnpairedUnicodeSurrogate_FailsClosed()
    {
        var node = JsonValue.Create(new string('\\uD800', 1));
        Assert.Throws<InvalidOperationException>(() => Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_ComplexNestedStructure_ProducesConsistentOutput()
    {
        var json = @"{
            ""user"": {
                ""name"": ""Alice"",
                ""age"": 30,
                ""active"": true
            },
            ""items"": [
                {""id"": 2, ""name"": ""Item B""},
                {""id"": 1, ""name"": ""Item A""}
            ],
            ""metadata"": {
                ""version"": ""1.0"",
                ""timestamp"": 1234567890
            }
        }";
        var node = JsonNode.Parse(json);
        var result = Canonicalizer.Canonicalize(node);
        Assert.StartsWith("{\"items\":", result);
        Assert.Contains("\"metadata\":", result);
        Assert.Contains("\"user\":", result);
        Assert.Contains("{\"active\":true,\"age\":30,\"name\":\"Alice\"}", result);
        Assert.Contains("{\"timestamp\":1234567890,\"version\":\"1.0\"}", result);
    }

    [Fact]
    public void Canonicalize_GoldenFile_MatchesExpectedOutput()
    {
        var inputJson = File.ReadAllText("golden.json");
        var node = JsonNode.Parse(inputJson);
        var expected = "{\"a\":1,\"b\":0,\"c\":100,\"d\":\"hello\\nworld\",\"e\":{\"y\":2,\"z\":1},\"f\":[1,2,3]}";
        Assert.Equal(expected, Canonicalizer.Canonicalize(node));
    }

    [Fact]
    public void Canonicalize_DoubleRun_IsConsistent()
    {
        var inputJson = File.ReadAllText("golden.json");
        var node = JsonNode.Parse(inputJson);
        var result1 = Canonicalizer.Canonicalize(node);
        var result2 = Canonicalizer.Canonicalize(node);
        Assert.Equal(result1, result2);
    }
}
