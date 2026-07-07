from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE = "https://api.eex-group.com/pub/market-data"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json,text/plain,*/*",
    "Origin": "https://www.eex.com",
    "Referer": "https://www.eex.com/en/market-data/market-data-hub",
}

paths = [
    "",
    "/",
    "/contracts",
    "/products",
    "/filters",
    "/commodity",
    "/metadata",
    "/data",
    "/table",
    "/chart",
]

queries = [
    {},
    {"commodity": "Freight"},
    {"commodity": "Freight", "pricing": "Futures"},
    {"commodity": "Freight", "pricing": "Futures", "product": "Capesize"},
    {
        "commodity": "Freight",
        "pricing": "Futures",
        "product": "Capesize",
        "productSpecific": "5TC",
        "maturityType": "Month",
        "delivery": "July 2026",
    },
]

for path in paths:
    for query in queries:
        url = BASE + path
        if query:
            url += "?" + urlencode(query)
        print("=" * 80)
        print(url)
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=20) as response:
                body = response.read(800)
                print(response.status, response.headers.get("content-type"))
                print(body.decode("utf-8", errors="ignore")[:800])
        except HTTPError as exc:
            print("HTTP", exc.code, exc.reason)
            print(exc.read(200).decode("utf-8", errors="ignore"))
        except Exception as exc:
            print(type(exc).__name__, exc)
