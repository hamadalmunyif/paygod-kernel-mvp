using System.Globalization;
using System.Text.Json.Nodes;

namespace PayGod.Cli.Core;

/// <summary>
/// Minimal, safe policy expression evaluator.
/// Supports: and/or/not, == != > >= < <=, parentheses,
/// existence checks, and array quantifier: path.any(v => expr).
/// </summary>
public static class PolicyExpression
{
    public static bool Evaluate(string expression, JsonNode input, bool strictTypes = false)
    {
        var parser = new Parser(expression, strictTypes);
        var ast = parser.ParseExpression();
        parser.Expect(TokenType.EOF);
        var ctx = new EvalContext(input, strictTypes);
        return ast.Eval(ctx).AsBool(ctx.StrictTypes);
    }

    // Parse the complete expression without evaluating source values. An
    // unreachable malformed rule must not be hidden by earlier allow rules.
    // Only called by the explicit typed-v1 profile, not legacy replay.
    public static void ValidateSyntax(string expression)
    {
        var parser = new Parser(expression, strictSyntax: true);
        var ast = parser.ParseExpression();
        parser.Expect(TokenType.EOF);
        RequireStaticallyBooleanContext(ast, "top-level policy condition");
    }

    // A typed policy is parsed completely even if its first rule ALLOWs.
    // Reject impossible comparisons of statically known types during that
    // parse rather than waiting for a potentially unreachable rule to Eval().
    // A PathRef has unknown type until actual admitted input is evaluated.
    private enum StaticKind { Unknown, Boolean, SafeInteger, String }

    private static StaticKind InferStaticKind(Expr expr) => expr switch
    {
        BoolLiteral or NotExpr or BinaryBoolExpr or CompareExpr or AnyExpr
            => StaticKind.Boolean,
        SafeIntegerLiteral => StaticKind.SafeInteger,
        StringLiteral => StaticKind.String,
        _ => StaticKind.Unknown
    };

    private static void RequireStaticallyValidComparison(TokenType op, Expr left, Expr right)
    {
        var lhs = InferStaticKind(left);
        var rhs = InferStaticKind(right);
        if (lhs == StaticKind.Unknown || rhs == StaticKind.Unknown)
            return; // Runtime admission must check both operands, even under not.
        if (lhs != rhs)
            throw new InvalidOperationException(
                "typed-v1 policy comparison has incompatible static operand types.");
        if (lhs == StaticKind.Boolean && op is not (TokenType.Eq or TokenType.Ne))
            throw new InvalidOperationException(
                "typed-v1 Boolean literals/expressions support equality or inequality only.");
    }

    private static void RequireStaticallyBooleanContext(Expr expr, string context)
    {
        var kind = InferStaticKind(expr);
        if (kind is StaticKind.SafeInteger or StaticKind.String)
            throw new InvalidOperationException(
                $"typed-v1 {context} requires a Boolean expression.");
        // Unknown is permitted here because PathRef type is source-dependent
        // and will still be checked fail-closed during strict evaluation.
    }

    private sealed class EvalContext
    {
        public JsonNode Input { get; }
        public bool StrictTypes { get; }
        private readonly Dictionary<string, JsonNode?> _vars = new(StringComparer.Ordinal);

        public EvalContext(JsonNode input, bool strictTypes)
        {
            Input = input;
            StrictTypes = strictTypes;
        }

        public JsonNode? ResolveVar(string name)
        {
            if (name.Equals("input", StringComparison.Ordinal)) return Input;
            return _vars.TryGetValue(name, out var v) ? v : null;
        }

        public void SetVar(string name, JsonNode? value) => _vars[name] = value;
        public bool TryGetVar(string name, out JsonNode? value) => _vars.TryGetValue(name, out value);
        public void RemoveVar(string name) => _vars.Remove(name);
    }

    private readonly record struct Value(JsonNode? Node)
    {
        public bool AsBool(bool strictTypes = false)
        {
            // Only real JSON Boolean may stand as a truth value in typed-v1.
            // Missing/null/string/number/array/object are not evidence of false.
            if (strictTypes)
            {
                var kind = Node?.GetValueKind();
                if (kind is System.Text.Json.JsonValueKind.True or System.Text.Json.JsonValueKind.False)
                    return kind == System.Text.Json.JsonValueKind.True;
                throw new InvalidOperationException(
                    "Policy Boolean expression requires a present JSON boolean.");
            }
            if (Node is null) return false;
            if (Node is JsonValue v)
            {
                if (v.TryGetValue<bool>(out var b)) return b;
                if (v.TryGetValue<string>(out var s)) return !string.IsNullOrEmpty(s);
                if (TryGetDouble(v, out var d)) return Math.Abs(d) > 0;
            }
            if (Node is JsonArray a) return a.Count > 0;
            if (Node is JsonObject o) return o.Count > 0;
            return false;
        }

        public string? AsString()
        {
            if (Node is JsonValue v && v.TryGetValue<string>(out var s)) return s;
            return Node?.ToString();
        }

        public double? AsNumber()
        {
            if (Node is JsonValue v && TryGetDouble(v, out var d)) return d;
            if (Node is JsonValue vs && double.TryParse(vs.ToString(), NumberStyles.Float, CultureInfo.InvariantCulture, out var p)) return p;
            return null;
        }

        public static bool TryGetDouble(JsonValue v, out double d)
        {
            if (v.TryGetValue<double>(out d)) return true;
            if (v.TryGetValue<int>(out var i)) { d = i; return true; }
            if (v.TryGetValue<long>(out var l)) { d = l; return true; }
            if (v.TryGetValue<decimal>(out var m)) { d = (double)m; return true; }
            var s = v.ToString();
            return double.TryParse(s, NumberStyles.Float, CultureInfo.InvariantCulture, out d);
        }
    }

    private abstract class Expr
    {
        public abstract Value Eval(EvalContext ctx);
    }

    private sealed class BoolLiteral(bool value) : Expr
    {
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(value));
    }

    private sealed class NumberLiteral(double value) : Expr
    {
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(value));
    }

    // typed-v1 authored numbers are c14n-v1 safe integers, never doubles.
    private sealed class SafeIntegerLiteral(long value) : Expr
    {
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(value));
    }

    private sealed class StringLiteral(string value) : Expr
    {
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(value));
    }

    private sealed class PathRef(string root, IReadOnlyList<string> segments) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var node = ctx.ResolveVar(root);
            foreach (var seg in segments)
            {
                if (node is JsonObject obj)
                {
                    if (!obj.TryGetPropertyValue(seg, out node)) return new(null);
                }
                else
                {
                    return new(null);
                }
            }
            return new(node);
        }
    }

    private sealed class NotExpr(Expr inner) : Expr
    {
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(!inner.Eval(ctx).AsBool(ctx.StrictTypes)));
    }

    private sealed class BinaryBoolExpr(TokenType op, Expr left, Expr right) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var l = left.Eval(ctx).AsBool(ctx.StrictTypes);
            if (op == TokenType.And)
            {
                if (!l) return new(JsonValue.Create(false));
                return new(JsonValue.Create(right.Eval(ctx).AsBool(ctx.StrictTypes)));
            }
            if (op == TokenType.Or)
            {
                if (l) return new(JsonValue.Create(true));
                return new(JsonValue.Create(right.Eval(ctx).AsBool(ctx.StrictTypes)));
            }
            return new(JsonValue.Create(false));
        }
    }

    private sealed class CompareExpr(TokenType op, Expr left, Expr right) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var l = left.Eval(ctx);
            var r = right.Eval(ctx);

            // Typed comparisons: a missing/null operand is not negative evidence.
            // Disallow implicit string/number/boolean coercion in policy comparisons.
            // Invalid operands raise an evaluation error (including under 'not'),
            // rather than emitting a false result that a negation could turn
            // into an unsafe allow. Admission still gates external source facts.
            if (!ctx.StrictTypes)
            {
            var ln = l.AsNumber();
            var rn = r.AsNumber();
            if (ln.HasValue && rn.HasValue)
            {
                var res = op switch
                {
                    TokenType.Eq => Math.Abs(ln.Value - rn.Value) < 1e-9,
                    TokenType.Ne => Math.Abs(ln.Value - rn.Value) >= 1e-9,
                    TokenType.Gt => ln.Value > rn.Value,
                    TokenType.Ge => ln.Value >= rn.Value,
                    TokenType.Lt => ln.Value < rn.Value,
                    TokenType.Le => ln.Value <= rn.Value,
                    _ => false
                };
                return new(JsonValue.Create(res));
            }

            var ls = l.AsString();
            var rs = r.AsString();
            if (ls is not null && rs is not null)
            {
                var cmp = string.CompareOrdinal(ls, rs);
                var res = op switch
                {
                    TokenType.Eq => cmp == 0,
                    TokenType.Ne => cmp != 0,
                    TokenType.Gt => cmp > 0,
                    TokenType.Ge => cmp >= 0,
                    TokenType.Lt => cmp < 0,
                    TokenType.Le => cmp <= 0,
                    _ => false
                };
                return new(JsonValue.Create(res));
            }

            var lb = l.AsBool();
            var rb = r.AsBool();
            var bres = op switch
            {
                TokenType.Eq => lb == rb,
                TokenType.Ne => lb != rb,
                _ => false
            };
            return new(JsonValue.Create(bres));
            }
            
            // Explicit new profile only; never alter historic pack replay defaults.
            var lk = l.Node?.GetValueKind();
            var rk = r.Node?.GetValueKind();
            if (lk is null || rk is null)
                throw new InvalidOperationException("Policy comparison requires present, non-null operands.");

            // paygod-c14n-v1 source numbers are bounded safe integers; numeric
            // equality in a security policy must not use legacy 1e-9 fuzz.
            if (lk == System.Text.Json.JsonValueKind.Number &&
                rk == System.Text.Json.JsonValueKind.Number)
            {
                // Evaluator equality must not depend on binary floating point.
                // paygod-c14n-v1 source and explicit typed policy literals are
                // bounded integers; compare the exact 64-bit values.
                var ln = RequireTypedSafeInteger(l);
                var rn = RequireTypedSafeInteger(r);
                var result = op switch
                {
                    TokenType.Eq => ln == rn,
                    TokenType.Ne => ln != rn,
                    TokenType.Gt => ln > rn,
                    TokenType.Ge => ln >= rn,
                    TokenType.Lt => ln < rn,
                    TokenType.Le => ln <= rn,
                    _ => false
                };
                return new(JsonValue.Create(result));
            }

            if (lk == System.Text.Json.JsonValueKind.String &&
                rk == System.Text.Json.JsonValueKind.String)
            {
                var cmp = string.CompareOrdinal(l.AsString(), r.AsString());
                var result = op switch
                {
                    TokenType.Eq => cmp == 0,
                    TokenType.Ne => cmp != 0,
                    TokenType.Gt => cmp > 0,
                    TokenType.Ge => cmp >= 0,
                    TokenType.Lt => cmp < 0,
                    TokenType.Le => cmp <= 0,
                    _ => false
                };
                return new(JsonValue.Create(result));
            }

            var lhsBool = lk is System.Text.Json.JsonValueKind.True or System.Text.Json.JsonValueKind.False;
            var rhsBool = rk is System.Text.Json.JsonValueKind.True or System.Text.Json.JsonValueKind.False;
            if (lhsBool && rhsBool)
            {
                var lhs = lk == System.Text.Json.JsonValueKind.True;
                var rhs = rk == System.Text.Json.JsonValueKind.True;
                // Ordering booleans is undefined for typed-v1. Returning false
                // here would let a surrounding 'not' turn malformed policy
                // syntax into an ALLOW, violating fail-closed evaluation.
                if (op is not TokenType.Eq and not TokenType.Ne)
                    throw new InvalidOperationException(
                        "Policy Boolean comparison supports equality and inequality only.");
                var result = op == TokenType.Eq ? lhs == rhs : lhs != rhs;
                return new(JsonValue.Create(result));
            }

            // A false result under 'not' could become an unsafe allow.
            // Refuse malformed/cross-kind comparisons instead of producing a
            // boolean that the policy could invert.
            throw new InvalidOperationException("Policy comparison operands have incompatible or unsupported types.");
        }
    }

    private static long RequireTypedSafeInteger(Value value)
    {
        // ToJsonString retains the lexical JSON number for parsed source
        // nodes and emits an integer for SafeIntegerLiteral values.
        // Reject decimal/exponent source forms instead of coercing to double.
        if (value.Node is not JsonValue number ||
            !long.TryParse(number.ToJsonString(), NumberStyles.AllowLeadingSign,
                CultureInfo.InvariantCulture, out var integral) ||
            integral < -Canonicalizer.SafeIntegerMax ||
            integral > Canonicalizer.SafeIntegerMax)
            throw new InvalidOperationException(
                "typed-v1 numeric comparisons require canonical safe integers.");
        return integral;
    }

    private sealed class AnyExpr(PathRef arrayPath, string varName, Expr predicate) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var arrVal = arrayPath.Eval(ctx).Node;
            if (arrVal is not JsonArray arr)
            {
                if (ctx.StrictTypes)
                    throw new InvalidOperationException("Policy any() requires a present JSON array.");
                return new(JsonValue.Create(false));
            }

            if (ctx.StrictTypes)
            {
                // An inner any(v => ...) may shadow an outer any(v => ...).
                // Restore lexical binding even on early success or exception.
                // Preserve old legacy-v1 variable behavior for historical replay.
                if (varName == "input")
                    throw new InvalidOperationException("Policy any() cannot shadow the reserved input root.");
                var hadPrevious = ctx.TryGetVar(varName, out var previous);
                try
                {
                    foreach (var item in arr)
                    {
                        ctx.SetVar(varName, item);
                        if (predicate.Eval(ctx).AsBool(true))
                            return new(JsonValue.Create(true));
                    }
                    return new(JsonValue.Create(false));
                }
                finally
                {
                    if (hadPrevious) ctx.SetVar(varName, previous);
                    else ctx.RemoveVar(varName);
                }
            }

            foreach (var item in arr)
            {
                ctx.SetVar(varName, item);
                if (predicate.Eval(ctx).AsBool(ctx.StrictTypes)) return new(JsonValue.Create(true));
            }
            return new(JsonValue.Create(false));
        }
    }

    private enum TokenType
    {
        EOF,
        Ident,
        Number,
        String,
        True,
        False,
        Dot,
        LParen,
        RParen,
        Comma,
        Arrow,
        Eq,
        Ne,
        Gt,
        Ge,
        Lt,
        Le,
        And,
        Or,
        Not
    }

    private sealed record Token(TokenType Type, string Text);

    private sealed class Lexer(string s, bool strictSyntax)
    {
        private int _i;

        public Token Next()
        {
            SkipWs();
            if (_i >= s.Length) return new(TokenType.EOF, "");
            var c = s[_i];

            if (char.IsLetter(c) || c == '_')
            {
                var start = _i++;
                while (_i < s.Length && (char.IsLetterOrDigit(s[_i]) || s[_i] == '_')) _i++;
                var text = s[start.._i];
                return text switch
                {
                    "and" => new(TokenType.And, text),
                    "or" => new(TokenType.Or, text),
                    "not" => new(TokenType.Not, text),
                    "true" => new(TokenType.True, text),
                    "false" => new(TokenType.False, text),
                    _ => new(TokenType.Ident, text)
                };
            }

            if (char.IsDigit(c) ||
                (strictSyntax && c == '-' && _i + 1 < s.Length && char.IsDigit(s[_i + 1])) ||
                (c == '.' && _i + 1 < s.Length && char.IsDigit(s[_i + 1])))
            {
                var start = _i++;
                while (_i < s.Length && (char.IsDigit(s[_i]) || s[_i] == '.' || s[_i] == 'e' || s[_i] == 'E' || s[_i] == '+' || s[_i] == '-')) _i++;
                return new(TokenType.Number, s[start.._i]);
            }

            if (c is '\'' or '"')
            {
                var quote = c;
                _i++;
                var start = _i;
                while (_i < s.Length && s[_i] != quote) _i++;
                var text = s[start.._i];
                if (_i < s.Length) _i++;
                else if (strictSyntax)
                    throw new InvalidOperationException("Unterminated policy string literal.");
                return new(TokenType.String, text);
            }

            _i++;
            return c switch
            {
                '.' => new(TokenType.Dot, "."),
                '(' => new(TokenType.LParen, "("),
                ')' => new(TokenType.RParen, ")"),
                ',' => new(TokenType.Comma, ","),
                '=' when Peek('=') => (_i++, new Token(TokenType.Eq, "==")).Item2,
                '!' when Peek('=') => (_i++, new Token(TokenType.Ne, "!=")).Item2,
                '>' when Peek('=') => (_i++, new Token(TokenType.Ge, ">=")).Item2,
                '<' when Peek('=') => (_i++, new Token(TokenType.Le, "<=")).Item2,
                '>' => new(TokenType.Gt, ">"),
                '<' => new(TokenType.Lt, "<"),
                '=' when Peek('>') => (_i++, new Token(TokenType.Arrow, "=>")).Item2,
                _ => strictSyntax
                    ? throw new InvalidOperationException($"Unsupported character in policy expression: U+{(int)c:X4}.")
                    : new(TokenType.EOF, "")
            };

            bool Peek(char ch) => _i < s.Length && s[_i] == ch;
        }

        private void SkipWs()
        {
            while (_i < s.Length && char.IsWhiteSpace(s[_i])) _i++;
        }
    }

    private sealed class Parser(string s, bool strictSyntax)
    {
        private readonly Lexer _lx = new(s, strictSyntax);
        private Token _cur = new(TokenType.EOF, "");

        public Expr ParseExpression()
        {
            _cur = _lx.Next();
            return ParseOr();
        }

        public void Expect(TokenType t)
        {
            if (_cur.Type != t) throw new InvalidOperationException($"Expected {t} but got {_cur.Type}");
        }

        private Expr ParseOr()
        {
            var left = ParseAnd();
            while (_cur.Type == TokenType.Or)
            {
                Consume(TokenType.Or);
                var right = ParseAnd();
                if (strictSyntax)
                {
                    RequireStaticallyBooleanContext(left, "or left operand");
                    RequireStaticallyBooleanContext(right, "or right operand");
                }
                left = new BinaryBoolExpr(TokenType.Or, left, right);
            }
            return left;
        }

        private Expr ParseAnd()
        {
            var left = ParseUnary();
            while (_cur.Type == TokenType.And)
            {
                Consume(TokenType.And);
                var right = ParseUnary();
                if (strictSyntax)
                {
                    RequireStaticallyBooleanContext(left, "and left operand");
                    RequireStaticallyBooleanContext(right, "and right operand");
                }
                left = new BinaryBoolExpr(TokenType.And, left, right);
            }
            return left;
        }

        private Expr ParseUnary()
        {
            if (_cur.Type == TokenType.Not)
            {
                Consume(TokenType.Not);
                var inner = ParseUnary();
                if (strictSyntax)
                    RequireStaticallyBooleanContext(inner, "not operand");
                return new NotExpr(inner);
            }
            return ParsePrimary();
        }

        private Expr ParsePrimary()
        {
            if (_cur.Type == TokenType.LParen)
            {
                Consume(TokenType.LParen);
                var e = ParseOr();
                Consume(TokenType.RParen);
                return e;
            }

            var left = ParseValue();

            // comparisons
            if (_cur.Type is TokenType.Eq or TokenType.Ne or TokenType.Gt or TokenType.Ge or TokenType.Lt or TokenType.Le)
            {
                var op = _cur.Type;
                _cur = _lx.Next();
                var right = ParseValue();
                if (strictSyntax)
                    RequireStaticallyValidComparison(op, left, right);
                return new CompareExpr(op, left, right);
            }

            // value in boolean context
            return left;
        }

        private Expr ParseValue()
        {
            switch (_cur.Type)
            {
                case TokenType.True: Consume(TokenType.True); return new BoolLiteral(true);
                case TokenType.False: Consume(TokenType.False); return new BoolLiteral(false);
                case TokenType.Number:
                    var numText = _cur.Text; Consume(TokenType.Number);
                    if (strictSyntax)
                    {
                        if (!long.TryParse(numText, NumberStyles.AllowLeadingSign,
                                CultureInfo.InvariantCulture, out var integer) ||
                            integer < -Canonicalizer.SafeIntegerMax ||
                            integer > Canonicalizer.SafeIntegerMax)
                            throw new InvalidOperationException(
                                "typed-v1 policy numeric literals must be safe integers.");
                        return new SafeIntegerLiteral(integer);
                    }
                    _ = double.TryParse(numText, NumberStyles.Float,
                        CultureInfo.InvariantCulture, out var d);
                    return new NumberLiteral(d);
                case TokenType.String:
                    var sText = _cur.Text; Consume(TokenType.String);
                    return new StringLiteral(sText);
                case TokenType.Ident:
                    return ParsePathOrAny();
                default:
                    throw new InvalidOperationException($"Unexpected token: {_cur.Type}");
            }
        }

        private Expr ParsePathOrAny()
        {
            var root = _cur.Text;
            Consume(TokenType.Ident);
            var segments = new List<string>();

            while (_cur.Type == TokenType.Dot)
            {
                Consume(TokenType.Dot);
                if (_cur.Type != TokenType.Ident) throw new InvalidOperationException("Expected identifier after '.'");
                var seg = _cur.Text;
                Consume(TokenType.Ident);

                // any(...) quantifier
                if (seg == "any" && _cur.Type == TokenType.LParen)
                {
                    // path already includes segments collected so far (excluding 'any')
                    var pathRef = new PathRef(root, segments);
                    Consume(TokenType.LParen);
                    if (_cur.Type != TokenType.Ident) throw new InvalidOperationException("Expected variable name in any()");
                    var varName = _cur.Text;
                    if (strictSyntax && varName == "input")
                        throw new InvalidOperationException(
                            "Policy any() cannot shadow reserved input root.");
                    Consume(TokenType.Ident);
                    Consume(TokenType.Arrow);
                    var pred = ParseOr();
                    Consume(TokenType.RParen);
                    if (strictSyntax)
                        RequireStaticallyBooleanContext(pred, "any() predicate");
                    return new AnyExpr(pathRef, varName, pred);
                }

                segments.Add(seg);
            }

            return new PathRef(root, segments);
        }

        private void Consume(TokenType t)
        {
            if (_cur.Type != t) throw new InvalidOperationException($"Expected {t} but got {_cur.Type}");
            _cur = _lx.Next();
        }
    }
}
