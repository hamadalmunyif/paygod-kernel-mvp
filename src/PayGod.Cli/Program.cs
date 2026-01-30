using System.CommandLine;
using System.Text.Json;
using System.Text.Json.Nodes;
using PayGod.Cli.Core;
using PayGod.Cli.Commands;

namespace PayGod.Cli;

class Program
{
    static async Task<int> Main(string[] args)
    {
        var rootCommand = new RootCommand("Paygod Kernel CLI - The High-Assurance Decision Engine");

        // Command: validate
        var validateCommand = new Command("validate", "Validate a JSON file and compute its canonical hash.");
        var inputOption = new Option<FileInfo>("--input", "Path to the JSON file to validate.") { IsRequired = true };
        var jsonOption = new Option<bool>("--json", "Output result as JSON.");
        
        validateCommand.AddOption(inputOption);
        validateCommand.AddOption(jsonOption);

        validateCommand.SetHandler((FileInfo input, bool jsonOutput) => 
        {
            ValidateHandler(input, jsonOutput);
        }, inputOption, jsonOption);

        // Command: test
        // Use the factory method from TestCommand class
        var testCommand = TestCommand.Create();

        // Add commands
        rootCommand.AddCommand(validateCommand);
        rootCommand.AddCommand(testCommand);
        rootCommand.AddCommand(PackCommand.Create());
        rootCommand.AddCommand(RunCommand.Create());

        // Add verify-vectors (Hidden/Internal)
        var verifyCommand = new Command("verify-vectors", "Internal: Verify compliance with spec vectors.") { IsHidden = true };
        var vectorFileOption = new Option<string>("--file", "Vector file path");
        verifyCommand.AddOption(vectorFileOption);
        verifyCommand.SetHandler((string file) => 
        {
             Console.WriteLine($"Verifying {file}...");
        }, vectorFileOption);
        rootCommand.AddCommand(verifyCommand);

        return await rootCommand.InvokeAsync(args);
    }

    static void ValidateHandler(FileInfo input, bool jsonOutput)
    {
        try
        {
            if (!input.Exists)
            {
                WriteError("Input file not found.", jsonOutput);
                Environment.Exit(1);
            }

            var content = File.ReadAllText(input.FullName);
            var node = JsonNode.Parse(content);
            
            var canonical = Canonicalizer.Canonicalize(node);
            var hash = Hasher.ComputeHash(node);

            if (jsonOutput)
            {
                var result = new
                {
                    status = "success",
                    code = 0,
                    data = new
                    {
                        hash = hash,
                        canonical_size = canonical.Length
                    }
                };
                Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = false }));
            }
            else
            {
                Console.WriteLine($"✅ Valid JSON");
                Console.WriteLine($"📝 Canonical Hash: {hash}");
            }
        }
        catch (JsonException ex)
        {
            WriteError($"Invalid JSON: {ex.Message}", jsonOutput);
            Environment.Exit(1);
        }
        catch (Exception ex)
        {
            WriteError($"System Error: {ex.Message}", jsonOutput);
            Environment.Exit(2);
        }
    }

    static void WriteError(string message, bool jsonOutput)
    {
        if (jsonOutput)
        {
            var result = new
            {
                status = "error",
                code = 1,
                errors = new[] { new { message = message } }
            };
            Console.WriteLine(JsonSerializer.Serialize(result));
        }
        else
        {
            Console.Error.WriteLine($"❌ Error: {message}");
        }
    }
}
