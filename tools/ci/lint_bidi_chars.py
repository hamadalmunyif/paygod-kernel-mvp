import os
import sys

BIDI_CHARS = {
    '\u202A',  # LRE
    '\u202B',  # RLE
    '\u202C',  # PDF
    '\u202D',  # LRM
    '\u202E',  # RLM
    '\u2066',  # LRI
    '\u2067',  # RLI
    '\u2068',  # FSI
    '\u2069',  # PDI
}

EXTENSIONS_TO_CHECK = (".cs", ".md", ".json")

def main():
    found_bidi = False
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(EXTENSIONS_TO_CHECK):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    for char in BIDI_CHARS:
                        if char in content:
                            print(f"ERROR: Found bidi character {char!r} in {path}")
                            found_bidi = True

    if found_bidi:
        sys.exit(1)

if __name__ == "__main__":
    main()
