using System.Security.Cryptography;
using System.Text;
using System.Text.Json.Nodes;

namespace PayGod.Cli.Core;

public static class Hasher
{
    public static string ComputeHash(JsonNode? node)
    {
        // 1. Canonicalize
        var canonical = Canonicalizer.Canonicalize(node);
        
        // 2. Encode UTF-8
        var bytes = Encoding.UTF8.GetBytes(canonical);
        
        // 3. SHA-256
        using var sha256 = SHA256.Create();
        var hashBytes = sha256.ComputeHash(bytes);
        
        // 4. Hex Lowercase
        return Convert.ToHexString(hashBytes).ToLowerInvariant();
    }
}
