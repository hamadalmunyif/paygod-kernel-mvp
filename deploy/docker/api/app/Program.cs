using System.Diagnostics;
using System.IO.Compression;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
builder.Services.ConfigureHttpJsonOptions(o =>
{
    o.SerializerOptions.PropertyNamingPolicy = JsonNamingPolicy.CamelCase;
    o.SerializerOptions.WriteIndented = false;
});

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { ok = true, service = "paygod-api", ts = DateTimeOffset.UtcNow }));

app.MapPost("/api/run", async (HttpContext ctx) =>
{
    // Request schema (minimal)
    // {
    //   "pack": "core/secrets-in-repo-guard",
    //   "input": { ...optional... }
    // }
    using var reader = new StreamReader(ctx.Request.Body);
    var body = await reader.ReadToEndAsync();

    string packRel = "core/secrets-in-repo-guard";

    // ✅ IMPORTANT: snapshot input JSON as string (do NOT keep JsonElement across doc lifetime)
    string? inputJsonOverride = null;

    if (!string.IsNullOrWhiteSpace(body))
    {
        using var doc = JsonDocument.Parse(body);
        var root = doc.RootElement;

        if (root.TryGetProperty("pack", out var packProp) && packProp.ValueKind == JsonValueKind.String)
            packRel = packProp.GetString() ?? packRel;

        if (root.TryGetProperty("input", out var inputProp))
            inputJsonOverride = inputProp.GetRawText(); // snapshot while doc alive
    }

    // Security: disallow path traversal / absolute
    packRel = packRel.Replace('\\', '/').Trim();
    if (packRel.StartsWith("/") || packRel.Contains(".."))
        return Results.BadRequest(new { error = "Invalid pack path" });

    var packFull = Path.Combine("/packs", packRel).Replace('\\', '/');

    // Default input (matches witness concept)
    var defaultInput = new
    {
        apiVersion = "belloop.io/v1",
        kind = "Input",
        metadata = new { id = "api-run", tenant = "dev", source = "api" },
        spec = new { target = new { type = "repo", path = "/work" } }
    };

    var runId = Guid.NewGuid().ToString("n");
    var outDir = Path.Combine("/out", runId);
    Directory.CreateDirectory(outDir);

    var inputPath = Path.Combine(Path.GetTempPath(), $"input-{runId}.json");

    var inputJson = inputJsonOverride ?? JsonSerializer.Serialize(defaultInput);
    await File.WriteAllTextAsync(inputPath, inputJson);

    // Execute runner CLI (no --clock unless supported; we stay strict)
    // Contract: run --pack --input --out
    var psi = new ProcessStartInfo
    {
        FileName = "dotnet",
        ArgumentList =
        {
            "/runner/PayGod.Cli.dll",
            "run",
            "--pack", packFull,
            "--input", inputPath,
            "--out", outDir
        },
        RedirectStandardOutput = true,
        RedirectStandardError = true
    };

    var p = Process.Start(psi);
    if (p is null) return Results.Problem("Failed to start runner");

    var stdout = await p.StandardOutput.ReadToEndAsync();
    var stderr = await p.StandardError.ReadToEndAsync();
    await p.WaitForExitAsync();

    if (p.ExitCode != 0)
    {
        return Results.Problem(
            title: "Runner failed",
            detail: stderr.Length > 0 ? stderr : stdout,
            statusCode: 500
        );
    }

    // Zip the artifacts directory and return it
    var zipPath = Path.Combine(Path.GetTempPath(), $"artifacts-{runId}.zip");
    if (File.Exists(zipPath)) File.Delete(zipPath);
    ZipFile.CreateFromDirectory(outDir, zipPath, CompressionLevel.Fastest, includeBaseDirectory: false);

    ctx.Response.Headers["X-Run-Id"] = runId;

    var zipBytes = await File.ReadAllBytesAsync(zipPath);
    return Results.File(zipBytes, "application/zip", $"artifacts-{runId}.zip");
});

app.Run("http://0.0.0.0:8080");
