import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URLS = [
    "https://api.sgx.com/derivatives/v1/nlt/metalist",
    "https://api.sgx.com/derivatives/v1.0/nlt/metalist",
    "https://api2.sgx.com/derivatives/v1/nlt/metalist",
    "https://api2.sgx.com/derivatives/v1.0/nlt/metalist",
    "https://api.sgx.com/derivatives/v1/negotiated-large-trade/metalist",
    "https://api.sgx.com/derivatives/v1.0/negotiated-large-trade/metalist",
    "https://api2.sgx.com/derivatives/v1/negotiated-large-trade/metalist",
    "https://api2.sgx.com/derivatives/v1.0/negotiated-large-trade/metalist",
    "https://api.sgx.com/derivatives/v1/negotiated-large-trades/metalist",
    "https://api.sgx.com/derivatives/v1.0/negotiated-large-trades/metalist",
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
    "Accept": "application/json,text/plain,*/*",
    "Referer": "https://www.sgx.com/derivatives/negotiated-large-trade-nlt?category=futures",
}

for url in URLS:
    print("=" * 80)
    print(url)
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=20) as response:
            raw = response.read(1000)
            print(response.status, response.headers.get("content-type"))
            print(raw.decode("utf-8", errors="replace")[:1000])
    except HTTPError as exc:
        print("HTTP", exc.code)
        print(exc.read(300).decode("utf-8", errors="ignore").encode("ascii", "ignore").decode("ascii"))
    except URLError as exc:
        print("URL", exc)
    except Exception as exc:
        print(type(exc).__name__, exc)
