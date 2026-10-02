using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;

namespace PayGod.Cli.Core;

public static class Canonicalizer
{
    public const string ProfileName = "paygod-c14n-v1";
    public const long SafeIntegerMax = 9_007_199_254_740_991L;

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
            foreach (var property in obj)
            {
                if (!property.Key.IsNormalized(NormalizationForm.FormC))
                    throw new InvalidOperationException("JSON object key is not NFC-normalized.");
            }

            sb.Append('{');
            var sortedKeys = obj.Select(x => x.Key).OrderBy(k => k, StringComparer.Ordinal).ToList();

            for (int i = 0; i < sortedKeys.Count; i++)
            {
                if (i > 0) sb.Append(',');
                var key = sortedKeys[i];
                WriteProfileString(key, sb);
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
            if (val.TryGetValue<JsonElement>(out var element))
            {
                switch (element.ValueKind)
                {
                    case JsonValueKind.Null:
                        sb.Append("null");
                        return;
                    case JsonValueKind.True:
                        sb.Append("true");
                        return;
                    case JsonValueKind.False:
                        sb.Append("false");
                        return;
                    case JsonValueKind.String:
                        WriteProfileString(element.GetString() ?? string.Empty, sb);
                        return;
                    case JsonValueKind.Number:
                        WriteRestrictedInteger(element.GetRawText(), sb);
                        return;
                    default:
                        throw new InvalidOperationException($"Unsupported JSON value kind: {element.ValueKind}.");
                }
            }

            if (val.TryGetValue<string>(out var s))
            {
                WriteProfileString(s, sb);
                return;
            }

            if (val.TryGetValue<bool>(out var b))
            {
                sb.Append(b ? "true" : "false");
                return;
            }

            if (val.TryGetValue<long>(out var l))
            {
                WriteSafeInteger(l, sb);
                return;
            }

            if (val.TryGetValue<int>(out var i))
            {
                WriteSafeInteger(i, sb);
                return;
            }

            throw new InvalidOperationException("Unsupported JSON value for paygod-c14n-v1.");
        }

        throw new InvalidOperationException($"Unsupported JSON node type: {node.GetType().Name}.");
    }

    private static void WriteRestrictedInteger(string raw, StringBuilder sb)
    {
        if (string.IsNullOrEmpty(raw))
            throw new InvalidOperationException("Empty JSON number is not allowed.");

        var index = raw[0] == '-' ? 1 : 0;
        if (index == raw.Length)
            throw new InvalidOperationException("Invalid integer representation.");

        for (var i = index; i < raw.Length; i++)
        {
            if (raw[i] < '0' || raw[i] > '9')
                throw new InvalidOperationException("Floating-point and exponent numbers are not allowed by paygod-c14n-v1.");
        }

        if (!long.TryParse(raw, NumberStyles.AllowLeadingSign, CultureInfo.InvariantCulture, out var value))
            throw new InvalidOperationException("Integer is outside the supported range.");

        WriteSafeInteger(value, sb);
    }

    private static void WriteSafeInteger(long value, StringBuilder sb)
    {
        if (value < -SafeIntegerMax || value > SafeIntegerMax)
            throw new InvalidOperationException("integer outside paygod-c14n-v1 safe range");

        sb.Append(value.ToString(CultureInfo.InvariantCulture));
    }

    private static void WriteProfileString(string s, StringBuilder sb)
    {
        sb.Append('"');
        for (var index = 0; index < s.Length; index++)
        {
            var c = s[index];

            if (char.IsHighSurrogate(c))
            {
                if (index + 1 >= s.Length || !char.IsLowSurrogate(s[index + 1]))
                    throw new InvalidOperationException("Unpaired Unicode surrogate is not allowed by paygod-c14n-v1.");

                sb.AppendFormat("\\u{0:x4}", (int)c);
                index++;
                sb.AppendFormat("\\u{0:x4}", (int)s[index]);
                continue;
            }

            if (char.IsLowSurrogate(c))
                throw new InvalidOperationException("Unpaired Unicode surrogate is not allowed by paygod-c14n-v1.");

            if (c == '"') sb.Append("\\\"");
            else if (c == '\\') sb.Append("\\\\");
            else if (c == '\b') sb.Append("\\b");
            else if (c == '\f') sb.Append("\\f");
            else if (c == '\n') sb.Append("\\n");
            else if (c == '\r') sb.Append("\\r");
            else if (c == '\t') sb.Append("\\t");
            else if (c < 0x20 || c > 0x7E)
            {
                sb.AppendFormat("\\u{0:x4}", (int)c);
            }
            else
            {
                sb.Append(c);
            }
        }
        sb.Append('"');
    }
}
