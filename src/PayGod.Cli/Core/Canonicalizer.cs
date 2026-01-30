using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Globalization;

namespace PayGod.Cli.Core;

public static class Canonicalizer
{
    public static string Canonicalize(JsonNode? node)
    {
        var sb = new StringBuilder();
        CanonicalizeToBuilder(node, sb);
        return sb.ToString();
    }

    private static void CanonicalizeToBuilder(JsonNode? node, StringBuilder sb)
    {
        if (node == null)
        {
            sb.Append("null");
            return;
        }

        if (node is JsonObject obj)
        {
            sb.Append('{');
            var sortedKeys = obj.Select(x => x.Key).OrderBy(k => k, StringComparer.Ordinal).ToList();
            
            for (int i = 0; i < sortedKeys.Count; i++)
            {
                if (i > 0) sb.Append(',');
                var key = sortedKeys[i];
                WriteJcsString(key, sb);
                sb.Append(':');
                CanonicalizeToBuilder(obj[key], sb);
            }
            sb.Append('}');
            return;
        }

        if (node is JsonArray arr)
        {
            sb.Append('[');
            for (int i = 0; i < arr.Count; i++)
            {
                if (i > 0) sb.Append(',');
                CanonicalizeToBuilder(arr[i], sb);
            }
            sb.Append(']');
            return;
        }

        if (node is JsonValue val)
        {
            if (val.TryGetValue<double>(out var d))
            {
                if (double.IsNaN(d) || double.IsInfinity(d))
                    throw new InvalidOperationException("Non-finite numbers are not valid JSON.");

                if (d == 0) { sb.Append("0"); return; } // Avoid "-0"

                var numStr = d.ToString("R", CultureInfo.InvariantCulture);
                numStr = numStr.Replace("E", "e");
                sb.Append(numStr);
                return;
            }
            
            if (val.TryGetValue<string>(out var s))
            {
                WriteJcsString(s, sb);
                return;
            }

            if (val.TryGetValue<bool>(out var b))
            {
                sb.Append(b ? "true" : "false");
                return;
            }

            sb.Append("null");
        }
    }

    // RFC 8785 Section 3.2.2.2: Strings
    private static void WriteJcsString(string s, StringBuilder sb)
    {
        sb.Append('"');
        foreach (char c in s)
        {
            if (c == '"') sb.Append("\\\"");
            else if (c == '\\') sb.Append("\\\\");
            else if (c == '\b') sb.Append("\\b");
            else if (c == '\f') sb.Append("\\f");
            else if (c == '\n') sb.Append("\\n");
            else if (c == '\r') sb.Append("\\r");
            else if (c == '\t') sb.Append("\\t");
            else if (c < 0x20) // Control characters < 0x20 must be escaped as \uXXXX
            {
                sb.AppendFormat("\\u{0:x4}", (int)c);
            }
            else
            {
                // All other characters (including Emojis/Unicode) are passed through raw
                sb.Append(c);
            }
        }
        sb.Append('"');
    }
}
