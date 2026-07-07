import re
from pathlib import Path


for path in Path(".").glob("sgx_*.js"):
    text = path.read_text(encoding="utf-8", errors="ignore")
    print(path)
    for match in sorted(set(re.findall(r'["\']([^"\']+?\.chunk\.js)["\']', text))):
        print(match)
    for match in sorted(set(re.findall(r'[A-Za-z0-9_.-]+\.chunk\.js', text))):
        print(match)
