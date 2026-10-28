"""Profile navigation, metadata and source provenance checks, without dependencies."""
import json,re,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.links=[];self.h1=0;self.labels=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if a.get('aria-labelledby'):self.labels.extend(a['aria-labelledby'].split())
  if tag in ('a','link','script'):self.links.append((tag,a.get('href') or a.get('src') or ''))
def graph(text):return json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)[1])['@graph']
home=(ROOT/'index.html').read_text(encoding='utf-8')
text=(ROOT/'profile.html').read_text(encoding='utf-8');page=Page(text)
assert page.h1==1
assert len(page.ids)==len(set(page.ids))
assert all(label in page.ids for label in page.labels)
for tag,url in page.links:
 u=urlsplit(url)
 assert u.scheme in ('','https'),url
 if url.startswith('#'):assert u.fragment in page.ids,url
 if tag!='a' and u.path.startswith('/'):assert (ROOT/u.path.lstrip('/')).is_file(),url
assert 'href="/profile.html"' in home
assert 'href="/"' in text
assert 'href="/profile.css?' in text and 'href="/profile.css?' not in home
assert 'src="/site.js' not in text,'Home-only sharing script must not share the root URL from the profile.'
g=graph(text);p=next(x for x in g if x['@type']=='Person')
assert p==next(x for x in graph(home) if x['@type']=='Person')
assert g[0]['@type']=='ProfilePage' and g[0]['mainEntity']['@id']==p['@id']
assert p['url']=='https://djnaoyaman.github.io/profile.html'
assert '<link rel="canonical" href="https://djnaoyaman.github.io/profile.html">' in text
assert '<meta property="og:url" content="https://djnaoyaman.github.io/profile.html">' in text
works=re.search(r'<ul class="profile-works">(.*?)</ul>',text,re.S)[1]
items=graph(home)[2]['mainEntity']['itemListElement']
assert len(re.findall(r'<li>',works))==len(items)==13
for item in items:assert 'href="'+item['item']['url']+'"' in works
for alias in ['Nobleman','一見坊','クランポック','湯気文吾','犬井静','紫波金魚']:assert alias in p['alternateName'] and alias in text
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').getroot().iter() if e.tag.endswith('}loc')]
assert 'https://djnaoyaman.github.io/profile.html' in urls
for name in ['llms.txt','llms-full.txt']:assert p['url'] in (ROOT/name).read_text(encoding='utf-8')
audit=(ROOT/'docs/profile-sources.md').read_text(encoding='utf-8')
assert len(re.findall(r'^\| [a-z].*? \|',audit,re.M))==14
assert len(text.encode('utf-8'))<50000
assert 'id="azumane"' in text and 'href="#azumane"' in text
assert 'href="/profile.html#azumane"' in home
assert 'town.shiwa.iwate.jp/soshiki/2_3/3_azumane/172677769112728/' in text
assert 'Partner Noteを読む（PDF・49ページ）' in text
print('PASS: profile navigation, IDs, labels, Person consistency, 13 works, aliases, canonical, sitemap and 14-repository evidence')
