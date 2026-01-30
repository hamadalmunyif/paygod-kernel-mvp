using System.CommandLine;
using System.Text.Json;
using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using YamlDotNet.Serialization;
using YamlDotNet.Serialization.NamingConventions;

namespace PayGod.Cli.Commands;

public static class TestCommand
{
    public static Command Create()
    {
        var command = new Command("test", "Run compliance tests for a policy pack.");
        var packOption = new Option<string>("--pack", "Path to the pack directory.") { IsRequired = true };
        var jsonOption = new Option<bool>("--json", "Output results as JSON.");

        command.AddOption(packOption);
        command.AddOption(jsonOption);

        command.SetHandler((string packDir, bool jsonOutput) =>
        {
            RunTests(packDir, jsonOutput);
        }, packOption, jsonOption);

        return command;
    }

    private static void RunTests(string packDir, bool jsonOutput)
    {
        try
        {
            var packPath = Path.Combine(packDir, "pack.yaml");
            var casesPath = Path.Combine(packDir, "tests", "cases.yaml");

            if (!File.Exists(packPath) || !File.Exists(casesPath))
            {
                WriteError("Pack or test cases not found.", jsonOutput);
                Environment.Exit(2);
            }

            var pack = PolicyEngine.LoadPack(packPath);
            var testCases = LoadTestCases(casesPath);

            var results = new List<object>();
            int passed = 0;
            int failed = 0;

            foreach (var testCase in testCases.cases)
            {
                // Convert input dictionary to JsonNode for the engine
                var inputJson = JsonSerializer.Serialize(testCase.input);
                var inputNode = JsonNode.Parse(inputJson);

                var result = PolicyEngine.Evaluate(pack, inputNode);

                bool isMatch = result.Decision == testCase.expected.decision;
                
                // Check matchers if any (simplified: check reason contains)
                if (isMatch && testCase.expected.matchers != null)
                {
                    foreach (var matcher in testCase.expected.matchers)
                    {
                        if (matcher.field == "reason" && matcher.@operator == "contains")
                        {
                            if (!result.Reason.Contains(matcher.value))
                            {
                                isMatch = false;
                                break;
                            }
                        }
                    }
                }

                if (isMatch) passed++;
                else failed++;

                results.Add(new
                {
                    name = testCase.name,
                    status = isMatch ? "pass" : "fail",
                    expected = testCase.expected.decision,
                    actual = result.Decision,
                    reason = result.Reason
                });
            }

            if (jsonOutput)
            {
                Console.WriteLine(JsonSerializer.Serialize(new
                {
                    summary = new { total = passed + failed, passed, failed },
                    results
                }, new JsonSerializerOptions { WriteIndented = false }));
            }
            else
            {
                Console.WriteLine($"📦 Testing Pack: {pack.metadata.name} v{pack.metadata.version}");
                foreach (dynamic res in results)
                {
                    if (res.status == "pass")
                        Console.WriteLine($"✅ {res.name}");
                    else
                        Console.WriteLine($"❌ {res.name} (Expected: {res.expected}, Got: {res.actual})");
                }
                Console.WriteLine($"\nSummary: {passed} Passed, {failed} Failed");
            }

            if (failed > 0) Environment.Exit(1);
        }
        catch (Exception ex)
        {
            WriteError($"Test Execution Error: {ex.Message}", jsonOutput);
            Environment.Exit(2);
        }
    }

    private static TestCaseFile LoadTestCases(string path)
    {
        var deserializer = new DeserializerBuilder()
            .WithNamingConvention(UnderscoredNamingConvention.Instance)
            .IgnoreUnmatchedProperties()
            .Build();
        return deserializer.Deserialize<TestCaseFile>(File.ReadAllText(path));
    }

    private static void WriteError(string message, bool jsonOutput)
    {
        if (jsonOutput)
            Console.WriteLine(JsonSerializer.Serialize(new { status = "error", message }));
        else
            Console.Error.WriteLine($"❌ Error: {message}");
    }
}

// Test Case Models
public class TestCaseFile
{
    public List<TestCase> cases { get; set; } = new();
}

public class TestCase
{
    public string name { get; set; } = "";
    public Dictionary<string, object> input { get; set; } = new();
    public TestExpected expected { get; set; } = new();
}

public class TestExpected
{
    public string decision { get; set; } = "";
    public List<TestMatcher> matchers { get; set; } = new();
}

public class TestMatcher
{
    public string field { get; set; } = "";
    public string @operator { get; set; } = "";
    public string value { get; set; } = "";
}
