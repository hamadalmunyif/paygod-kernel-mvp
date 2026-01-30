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
    public static bool Evaluate(string expression, JsonNode input)
    {
        var parser = new Parser(expression);
        var ast = parser.ParseExpression();
        parser.Expect(TokenType.EOF);
        var ctx = new EvalContext(input);
        return ast.Eval(ctx).AsBool();
    }

    private sealed class EvalContext
    {
        public JsonNode Input { get; }
        private readonly Dictionary<string, JsonNode?> _vars = new(StringComparer.Ordinal);

        public EvalContext(JsonNode input) => Input = input;

        public JsonNode? ResolveVar(string name)
        {
            if (name.Equals("input", StringComparison.Ordinal)) return Input;
            return _vars.TryGetValue(name, out var v) ? v : null;
        }

        public void SetVar(string name, JsonNode? value) => _vars[name] = value;
    }

    private readonly record struct Value(JsonNode? Node)
    {
        public bool AsBool()
        {
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
        public override Value Eval(EvalContext ctx) => new(JsonValue.Create(!inner.Eval(ctx).AsBool()));
    }

    private sealed class BinaryBoolExpr(TokenType op, Expr left, Expr right) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var l = left.Eval(ctx).AsBool();
            if (op == TokenType.And)
            {
                if (!l) return new(JsonValue.Create(false));
                return new(JsonValue.Create(right.Eval(ctx).AsBool()));
            }
            if (op == TokenType.Or)
            {
                if (l) return new(JsonValue.Create(true));
                return new(JsonValue.Create(right.Eval(ctx).AsBool()));
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
    }

    private sealed class AnyExpr(PathRef arrayPath, string varName, Expr predicate) : Expr
    {
        public override Value Eval(EvalContext ctx)
        {
            var arrVal = arrayPath.Eval(ctx).Node;
            if (arrVal is not JsonArray arr) return new(JsonValue.Create(false));

            foreach (var item in arr)
            {
                ctx.SetVar(varName, item);
                if (predicate.Eval(ctx).AsBool()) return new(JsonValue.Create(true));
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

    private sealed class Lexer(string s)
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

            if (char.IsDigit(c) || (c == '.' && _i + 1 < s.Length && char.IsDigit(s[_i + 1])))
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
                _ => new(TokenType.EOF, "")
            };

            bool Peek(char ch) => _i < s.Length && s[_i] == ch;
        }

        private void SkipWs()
        {
            while (_i < s.Length && char.IsWhiteSpace(s[_i])) _i++;
        }
    }

    private sealed class Parser(string s)
    {
        private readonly Lexer _lx = new(s);
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
                left = new BinaryBoolExpr(TokenType.And, left, right);
            }
            return left;
        }

        private Expr ParseUnary()
        {
            if (_cur.Type == TokenType.Not)
            {
                Consume(TokenType.Not);
                return new NotExpr(ParseUnary());
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
                    _ = double.TryParse(numText, NumberStyles.Float, CultureInfo.InvariantCulture, out var d);
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
                    Consume(TokenType.Ident);
                    Consume(TokenType.Arrow);
                    var pred = ParseOr();
                    Consume(TokenType.RParen);
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
