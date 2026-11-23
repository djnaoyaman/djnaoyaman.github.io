"""Check delivered, first-party HTML without sending analytics events."""
import concurrent.futures
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

ORIGIN = "https://djnaoyaman.github.io"
SEEDS = json.loads(Path(__file__).with_name("public-html.json").read_text())

def fetch(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"MINA-public-tag-review/1.0", "Cache-Control":"no-cache"})
            with urllib.request.urlopen(req, timeout=20) as res:
                return res.status, res.read().decode("utf-8-sig", "replace")
        except urllib.error.HTTPError as exc:
            if exc.code < 500 or attempt == 2:
                return exc.code, exc.read().decode("utf-8-sig", "replace")
        except OSError as exc:
            if attempt == 2:
                return 0, str(exc)
        time.sleep(1 + attempt)
    return 0, ""

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.srcs, self.js = [], [], []
        self.active = False
        self.redirect = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "meta" and a.get("http-equiv", "").lower() == "refresh":
            self.redirect = True
        if tag == "script":
            self.active = a.get("type", "").lower() in ("", "text/javascript", "application/javascript", "module")
            if self.active and a.get("src"):
                self.srcs.append(a["src"])
    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False
    def handle_data(self, data):
        if self.active:
            self.js.append(data)

def local_path(base, current, href):
    if not href or href.startswith(("#", "?", "mailto:", "tel:", "javascript:", "data:")):
        return None
    parsed = urllib.parse.urlsplit(urllib.parse.urljoin(current, href))
    if parsed.netloc != urllib.parse.urlsplit(base).netloc or parsed.scheme != "https":
        return None
    path = parsed.path
    if base == ORIGIN + "/":
        if "/" in path.strip("/") or (path.count("/") > 1 and path != "/"):
            return None
    if not (parsed.netloc + path).startswith(base.split("://")[1]):
        return None
    if not (path.endswith("/") or path.lower().endswith((".htm", ".html"))):
        return None
    if path.endswith("/index.html"):
        path = path[:-10]
    return parsed.scheme + "://" + parsed.netloc + path

def audit(site, extra, executor):
    base = "https://yoshida-farm.co.jp/" if site == "yoshida-farmer" else ORIGIN + ("/" if site == "djnaoyaman.github.io" else "/" + site + "/")
    todo = {base}
    for p in extra:
        u = local_path(base, base, p)
        if u:
            todo.add(u)
    status, xml = fetch(base + "sitemap.xml")
    if status == 200:
        for el in ET.fromstring(xml).iter():
            if el.tag.split("}")[-1] == "loc":
                u = local_path(base, base, el.text)
                if u:
                    todo.add(u)
    processed, scripts = {}, {}
    while todo:
        batch = sorted(todo)
        todo = set()
        for url, (code, html) in zip(batch, executor.map(fetch, batch)):
            if code != 200:
                processed[url] = ("HTTP " + str(code),)
                continue
            page = Page()
            page.feed(html)
            linked = (local_path(base, url, link) for link in page.links)
            todo.update(u for u in linked if u)
            direct = [s for s in page.srcs if re.search(r"googletagmanager\.com/gtag/js", s)]
            combined = "\n".join(page.js)
            for src in page.srcs:
                absolute = urllib.parse.urljoin(url, src)
                if urllib.parse.urlsplit(absolute).netloc != urllib.parse.urlsplit(base).netloc:
                    continue
                if absolute not in scripts:
                    sc, js = fetch(absolute)
                    scripts[absolute] = js if sc == 200 and re.search(r"googletagmanager\.com/(?:gtag|gtm)|['\"]config['\"]\s*,",js) else ""
                combined += "\n" + scripts[absolute]
            configs = re.findall(r"(?:\bgtag|\btrack)\s*\(\s*['\"]config['\"]\s*,\s*['\"](G-[A-Z0-9]+)", combined)
            gtms = sorted(set(re.findall(r"\bGTM-[A-Z0-9]+", combined)))
            dynamic = len(re.findall(r"googletagmanager\.com/gtag/js", combined))
            loader_ids = [urllib.parse.parse_qs(urllib.parse.urlsplit(s).query).get("id",["?"])[0] for s in direct]
            processed[url] = ("redirect" if page.redirect else "page", tuple(loader_ids), tuple(configs), tuple(gtms), dynamic)
        todo.difference_update(processed)
    groups = defaultdict(list)
    for u, g in sorted(processed.items()):
        groups[g].append(u[len(base):] or "/")
    for g, paths in groups.items():
        print("TAG_AUDIT",json.dumps([site,g,len(paths),paths[:8]],ensure_ascii=False), flush=True)

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        for site, extra in SEEDS.items():
            try:
                audit(site, extra, executor)
            except Exception as exc:
                print("AUDIT_ERROR", site, str(exc), flush=True)
