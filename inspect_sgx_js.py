import re
from pathlib import Path


text = Path("sgx_index.js").read_text(encoding="utf-8", errors="ignore")

for pattern in [
    "negotiated",
    "large-trade",
    "nlt",
    "api2",
    "baltic",
    "trade",
    "derivatives",
]:
    print("=" * 80)
    print(pattern, text.lower().find(pattern.lower()))
    match = re.search(pattern, text, flags=re.I)
    if match:
        start = max(0, match.start() - 500)
        end = min(len(text), match.end() + 1000)
        print(text[start:end])

print("=" * 80)
print("URL-like fragments")
fragments = sorted(
    set(
        re.findall(
            r"https?://[^\"'`\\]+|/[A-Za-z0-9_./?=&%:-]*api[A-Za-z0-9_./?=&%:-]*|/[A-Za-z0-9_./?=&%:-]*derivatives[A-Za-z0-9_./?=&%:-]*",
            text,
        )
    )
)
for fragment in fragments[:500]:
    print(fragment[:500])
