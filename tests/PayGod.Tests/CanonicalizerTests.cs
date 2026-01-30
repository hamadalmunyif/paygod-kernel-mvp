using System.Text.Json;
using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using Xunit;

namespace PayGod.Tests;

public class CanonicalizerTests
{
    [Fact]
    public void Canonicalize_NullNode_ReturnsNull()
    {
        // Arrange
        JsonNode? node = null;

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("null", result);
    }

    [Fact]
    public void Canonicalize_EmptyObject_ReturnsEmptyObject()
    {
        // Arrange
        var node = JsonNode.Parse("{}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("{}", result);
    }

    [Fact]
    public void Canonicalize_EmptyArray_ReturnsEmptyArray()
    {
        // Arrange
        var node = JsonNode.Parse("[]");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("[]", result);
    }

    [Fact]
    public void Canonicalize_SimpleObject_SortsKeys()
    {
        // Arrange
        var node = JsonNode.Parse("{\"z\":1,\"a\":2,\"m\":3}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("{\"a\":2,\"m\":3,\"z\":1}", result);
    }

    [Fact]
    public void Canonicalize_NestedObject_SortsKeysRecursively()
    {
        // Arrange
        var node = JsonNode.Parse("{\"outer\":{\"z\":1,\"a\":2},\"first\":true}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("{\"first\":true,\"outer\":{\"a\":2,\"z\":1}}", result);
    }

    [Fact]
    public void Canonicalize_ArrayOfObjects_MaintainsOrder()
    {
        // Arrange
        var node = JsonNode.Parse("[{\"b\":2,\"a\":1},{\"d\":4,\"c\":3}]");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("[{\"a\":1,\"b\":2},{\"c\":3,\"d\":4}]", result);
    }

    [Fact]
    public void Canonicalize_StringValues_EscapesCorrectly()
    {
        // Arrange
        var node = JsonNode.Parse("{\"text\":\"hello\\nworld\"}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("{\"text\":\"hello\\nworld\"}", result);
    }

    [Fact]
    public void Canonicalize_BooleanValues_ReturnsLowercase()
    {
        // Arrange
        var node = JsonNode.Parse("{\"isTrue\":true,\"isFalse\":false}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal("{\"isFalse\":false,\"isTrue\":true}", result);
    }

    [Fact]
    public void Canonicalize_NumericValues_FormatsCorrectly()
    {
        // Arrange
        var node = JsonNode.Parse("{\"integer\":42,\"float\":3.14,\"zero\":0}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Contains("\"integer\":42", result);
        Assert.Contains("\"zero\":0", result);
        Assert.Contains("\"float\":", result);
    }

    [Fact]
    public void Canonicalize_SpecialCharacters_EscapesCorrectly()
    {
        // Arrange
        var node = JsonNode.Parse("{\"quote\":\"\\\"\",\"backslash\":\"\\\\\"}");

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Contains("\\\"", result);
        Assert.Contains("\\\\", result);
    }

    [Fact]
    public void Canonicalize_ComplexNestedStructure_ProducesConsistentOutput()
    {
        // Arrange
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

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        // Verify keys are sorted at all levels
        Assert.StartsWith("{\"items\":", result);
        Assert.Contains("\"metadata\":", result);
        Assert.Contains("\"user\":", result);
        
        // Verify nested keys are also sorted
        Assert.Contains("{\"active\":true,\"age\":30,\"name\":\"Alice\"}", result);
        Assert.Contains("{\"timestamp\":1234567890,\"version\":\"1.0\"}", result);
    }

    [Fact]
    public void Canonicalize_GoldenFile_MatchesExpectedOutput()
    {
        // Arrange
        var inputJson = File.ReadAllText("golden.json");
        var node = JsonNode.Parse(inputJson);
        var expected = "{\"a\":1,\"b\":0,\"c\":100,\"d\":\"hello\\nworld\",\"e\":{\"y\":2,\"z\":1},\"f\":[1,2,3]}";

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal(expected, result);
    }

    [Fact]
    public void Canonicalize_DoubleRun_IsConsistent()
    {
        // Arrange
        var inputJson = File.ReadAllText("golden.json");
        var node = JsonNode.Parse(inputJson);

        // Act
        var result1 = Canonicalizer.Canonicalize(node);
        var result2 = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal(result1, result2);
    }

    [Theory]
    [InlineData("1.0", "1")]
    [InlineData("1.230", "1.23")]
    [InlineData("1E2", "100")]
    [InlineData("1e-2", "0.01")]
    [InlineData("-0", "0")]
    public void Canonicalize_NumberFormatting_IsStrict(string input, string expected)
    {
        // Arrange
        var node = JsonNode.Parse(input);

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData("\"e\u0301\"", "\"\\u00e9\"")] // NFC: é
    [InlineData("\"\u00e9\"", "\"\\u00e9\"")]   // NFD: e + ´
    public void Canonicalize_UnicodeNormalization_IsConsistent(string input, string expected)
    {
        // Arrange
        var node = JsonNode.Parse(input);

        // Act
        var result = Canonicalizer.Canonicalize(node);

        // Assert
        Assert.Equal(expected, result);
    }
}
