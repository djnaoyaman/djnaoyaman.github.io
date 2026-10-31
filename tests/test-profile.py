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
items=graph(home)[2]['mainEntity']['itemListElement']
assert len(items)==14
assert 'profile-works' not in text and 'href="/#worlds"' in text
assert set(p)=={'@type','@id','name','url'}
for banned in ['代表取締役','学歴','講演','15歳','父親','50以上','profile-career','profile-aliases']:
 assert banned not in text,banned
assert 'MIXWELLという考え方を大切にしています' in text
assert '確かめられることには出典を添え' in text
urls=[e.text for e in ET.parse(ROOT/'sitemap.xml').getroot().iter() if e.tag.endswith('}loc')]
assert 'https://djnaoyaman.github.io/profile.html' in urls
for name in ['llms.txt','llms-full.txt']:assert p['url'] in (ROOT/name).read_text(encoding='utf-8')
audit=(ROOT/'docs/profile-sources.md').read_text(encoding='utf-8')
assert len(re.findall(r'^\| [a-z].*? \|',audit,re.M))==14
assert len(text.encode('utf-8'))<50000
for fragment in ['career','azumane','music','activities','works','approach','links']:
 assert 'id="'+fragment+'"' in text
assert '<details class="author-story">' not in home
assert len(re.sub('<[^>]+>','',re.search(r'<main.*?</main>',text,re.S)[0]))<600
print('PASS: concise author intent, source policy, minimal Person, legacy fragments,14 WORLDs retained only on home, local assets and metadata')
# Same-site subordinate pages must use the maison shell rather than the retired home CSS.
for filename in ['profile.html','404.html']:
 sub=(ROOT/filename).read_text(); parsed=Page(sub)
 assert 'href="/maisons.css?' in sub and 'href="/subpages.css?' in sub
 assert 'href="/site.css?' not in sub
 assert 'content="#f7f6f2"' in sub
 assert '<a class="wordmark" href="/">' in sub and '<span>MIYAZAKINAOYA</span></a>' in sub and 'class="brand-symbol"' in sub
 for href,label in [('/#worlds','WORLDS'),('/#writing','JOURNAL'),('/#about','ABOUT')]:
  assert f'<a href="{href}">{label}</a>' in sub
 assert 'ずーっと、あれも、これも。' in sub
 assert len(parsed.ids)==len(set(parsed.ids)),filename
 for tag,url in parsed.links:
  u=urlsplit(url)
  if url.startswith('#'):assert u.fragment in parsed.ids,(filename,url)
  if tag!='a' and u.path.startswith('/'):assert (ROOT/u.path.lstrip('/')).is_file(),(filename,url)
 assert 'src="/site.js' not in sub
assert '音楽も、言葉も、日々の発見も。' in text
print('PASS: profile/404 shared maison shell, navigation, palette, tagline, anchors and local CSS')
