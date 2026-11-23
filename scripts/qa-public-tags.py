"""Check only six release representatives; never send analytics events."""
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

ORIGIN = "https://djnaoyaman.github.io"
TARGETS = [
    ("/", "G-PT03XG7KQR", "shared"),
    ("/profile.html", "G-PT03XG7KQR", "shared"),
    ("/chems/404.html", "G-GKZHN40P02", "inline"),
    ("/bookkeeping/404.html", "G-837HXKXW8Q", "inline"),
    ("/beforeweeat/404.html", "G-HBPDX2M5HR", "inline"),
    ("/buncho-ureshi/garden35-plan/", "GTM-W9SQSCBT", "gtm"),
]
CACHE = {}
CONFIG = re.compile(r"\b(?:gtag|track)\s*\(\s*['\"]config['\"]\s*,\s*['\"](G-[A-Z0-9]+)")

def fetch(url):
    assert urllib.parse.urlsplit(url).netloc == "djnaoyaman.github.io"
    if url not in CACHE:
        request = urllib.request.Request(url, headers={
            "User-Agent": "MINA-limited-release-check/1.0",
            "Cache-Control": "no-cache",
        })
        with urllib.request.urlopen(request, timeout=12) as response:
            assert response.status == 200, (url, response.status)
            CACHE[url] = response.read().decode("utf-8-sig")
    return CACHE[url]

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs, self.base = [], None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "base" and attrs.get("href"):
            self.base = attrs["href"]
        if tag == "script" and attrs.get("src"):
            self.srcs.append(attrs["src"])

failed = False
for path, expected, mode in TARGETS:
    try:
        url = ORIGIN + path
        html = fetch(url)
        page = Page()
        page.feed(html)
        base = urllib.parse.urljoin(url, page.base) if page.base else url
        sources = [urllib.parse.urljoin(base, src) for src in page.srcs]
        if mode == "gtm":
            loaders = [src for src in sources
                       if urllib.parse.urlsplit(src).path == "/buncho-ureshi/src/analytics-loader.js"]
            assert len(loaders) == 1, ("shared GTM loaders", loaders)
            assert expected in fetch(loaders[0]), "Unexpected GTM container"
            assert "googletagmanager.com/gtm.js" not in html, "Duplicate inline GTM loader"
            result = {"path": path, "container": expected, "loader_count": 1}
        else:
            loaders = [src for src in sources if "googletagmanager.com/gtag/js" in src]
            assert len(loaders) == 1, ("Google loader count", loaders)
            assert urllib.parse.parse_qs(urllib.parse.urlsplit(loaders[0]).query).get("id") == [expected]
            combined = html
            if mode == "shared":
                shared = [src for src in sources if urllib.parse.urlsplit(src).path == "/analytics.js"]
                assert len(shared) == 1, ("initializer count", shared)
                combined += "\n" + fetch(shared[0])
                for src in sources:
                    if urllib.parse.urlsplit(src).path == "/site.js":
                        assert "v=20261123-ga-shared" in src, "Old homepage script cache key"
                        combined += "\n" + fetch(src)
            configs = CONFIG.findall(combined)
            assert configs == [expected], ("config count or ID", configs)
            result = {"path": path, "measurement_id": expected,
                      "loader_count": 1, "config_count": 1}
        print("GA_SMOKE " + json.dumps(result, ensure_ascii=False), flush=True)
    except Exception as error:
        failed = True
        print("GA_SMOKE " + json.dumps({"path": path, "error": str(error)}), flush=True)

print("GA_SMOKE_SUMMARY " + json.dumps({
    "html_pages": len(TARGETS),
    "first_party_requests": len(CACHE),
    "analytics_requests": 0,
    "passed": not failed,
}), flush=True)
sys.exit(1 if failed else 0)
