#!/usr/bin/env python3
import sys, pathlib

# Unicode bidi / directionality control chars (Trojan Source-related)
BIDI = {
    "\u202A", "\u202B", "\u202D", "\u202E", "\u202C",  # LRE/RLE/LRO/RLO/PDF
    "\u2066", "\u2067", "\u2068", "\u2069",            # LRI/RLI/FSI/PDI
    "\u200E", "\u200F",                                # LRM/RLM
    "\u061C",                                          # ALM
}

# extensions to scan
EXTS = {".cs", ".csproj", ".sln", ".json", ".md", ".yml", ".yaml", ".ps1", ".sh", ".txt"}

def scan_file(p: pathlib.Path) -> list[tuple[int, str]]:
    hits = []
    try:
        data = p.read_text(encoding="utf-8", errors="strict")
    except Exception:
        # If not valid UTF-8, treat as a failure (optional). Or skip.
        return [(0, "NON_UTF8")]
    for i, ch in enumerate(data):
        if ch in BIDI:
            # line number
            line = data.count("\n", 0, i) + 1
            hits.append((line, f"U+{ord(ch):04X}"))
    return hits

def main(root: str) -> int:
    rootp = pathlib.Path(root)
    bad = []
    for p in rootp.rglob("*"):
        if p.is_file() and p.suffix.lower() in EXTS:
            hits = scan_file(p)
            if hits:
                for line, code in hits:
                    bad.append((p, line, code))
    if bad:
        print("❌ Bidi / directionality control characters found:")
        for p, line, code in bad:
            if line == 0 and code == "NON_UTF8":
                print(f" - {p}: non-UTF8 or unreadable")
            else:
                print(f" - {p}:{line} contains {code}")
        print("\nFix: remove these chars (VS Code can reveal them) and re-push.")
        return 2
    print("✅ No bidi control characters found.")
    return 0

if __name__ == "__main__":
    sys.exit(main("."))"))
(main("."))
