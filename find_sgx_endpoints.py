import re
from pathlib import Path


text = Path("sgx_index.js").read_text(encoding="utf-8", errors="ignore")

for match in re.finditer("endpoints", text):
    print("=" * 80)
    print(match.start())
    print(text[max(0, match.start() - 400) : match.start() + 800])
