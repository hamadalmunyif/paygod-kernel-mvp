using System.Security.Cryptography;
using System.Text;
using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using Xunit;

namespace PayGod.Tests;

public class CanonicalProfileVectorTests
{
    [Fact]
    public void SharedPaygodCanonicalizationVectorsMatchProducer()
    {
        var vectorPath = Path.Combine(AppContext.BaseDirectory, "canonical-json.json");
        var vectors = JsonNode.Parse(File.ReadAllText(vectorPath))?.AsArray()
            ?? throw new InvalidOperationException("canonical-json.json did not contain an array");

        foreach (var caseNode in vectors)
        {
            var testCase = caseNode?.AsObject()
                ?? throw new InvalidOperationException("canonical vector case must be an object");
            var description = testCase["description"]?.GetValue<string>() ?? "unnamed case";
            var input = testCase["input"]?.DeepClone();
            var expectedError = testCase["expected_error"]?.GetValue<string>();

            if (expectedError is not null)
            {
                var ex = Assert.Throws<InvalidOperationException>(() => Canonicalizer.Canonicalize(input));
                Assert.Contains(expectedError.ToLowerInvariant(), ex.Message.ToLowerInvariant());
                continue;
            }

            var expectedCanonical = testCase["expected_canonical"]?.GetValue<string>()
                ?? throw new InvalidOperationException($"missing expected_canonical: {description}");
            var expectedHash = testCase["expected_hash"]?.GetValue<string>()
                ?? throw new InvalidOperationException($"missing expected_hash: {description}");

            var actualCanonical = Canonicalizer.Canonicalize(input);
            Assert.True(
                actualCanonical == expectedCanonical,
                $"{description}: canonical mismatch. Expected {expectedCanonical}, actual {actualCanonical}");

            var actualHash = Convert.ToHexString(
                SHA256.HashData(Encoding.UTF8.GetBytes(actualCanonical))
            ).ToLowerInvariant();
            Assert.True(
                actualHash == expectedHash,
                $"{description}: hash mismatch. Expected {expectedHash}, actual {actualHash}");
        }
    }
}
