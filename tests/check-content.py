"""Dependency-free structural checks for GitHub Pages source."""
import json,struct,xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.refs=[];self.meta={};self.ld=[];self.in_ld=False;self.headings=[];self.descriptions=[];self.in_desc=False;self.in_h3=False;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='meta':self.meta[a.get('name') or a.get('property') or a.get('http-equiv')]=a.get('content')
  if tag in ['a','link','script','img']:
   v=a.get('href') or a.get('src')
   if v:self.refs.append((tag,v))
  if tag=='script' and a.get('type')=='application/ld+json':self.in_ld=True
  if tag=='h3':self.in_h3=True
  if tag=='p' and a.get('class')=='description':self.in_desc=True
 def handle_endtag(self,tag):
  if tag=='script':self.in_ld=False
  if tag=='h3':self.in_h3=False
  if tag=='p':self.in_desc=False
 def handle_data(self,data):
  if self.in_ld:self.ld.append(json.loads(data))
  if self.in_h3:self.headings.append(data)
  if self.in_desc:self.descriptions.append(data)
for filename in ['index.html','404.html']:
 page=Page((ROOT/filename).read_text())
 assert len(page.ids)==len(set(page.ids)),f'duplicate IDs: {filename}'
 for tag,url in page.refs:
  u=urlsplit(url)
  if url.startswith('#'):assert u.fragment in page.ids,url
  if not u.scheme and u.path.startswith('/'):
   local=ROOT/u.path.lstrip('/')
   if tag!='a':assert local.is_file(),url
 assert "default-src 'none'" in page.meta['Content-Security-Policy']
 assert "'unsafe-inline'" not in page.meta['Content-Security-Policy']
 assert 'referrer' in page.meta
 assert "manifest-src 'self'" in page.meta['Content-Security-Policy']
 assert page.meta['apple-mobile-web-app-title']=='NAOYA WEB.'
 if filename=='404.html':assert page.meta['robots']=='noindex,follow'
 else:
  graph=page.ld[0]['@graph'];collection=graph[2]['mainEntity'];items=collection['itemListElement']
  assert collection['numberOfItems']==len(items)==len(page.headings)==12
  assert [item['item']['name'] for item in items]==page.headings
  assert [item['item']['description'] for item in items]==page.descriptions
  assert [item['position'] for item in items]==list(range(1,13))
  assert f'content:"全{len(items)}サイト"' in (ROOT/'site.css').read_text()
  for item in items:
   for filename in ['llms.txt','llms-full.txt']:
    assert item['item']['url'] in (ROOT/filename).read_text(),filename
    assert item['item']['description'] in (ROOT/filename).read_text(),filename
manifest=json.loads((ROOT/'site.webmanifest').read_text())
for icon in manifest['icons']:
 data=(ROOT/urlsplit(icon['src']).path.lstrip('/')).read_bytes();width,height=struct.unpack('>II',data[16:24]);assert icon['sizes']==f'{width}x{height}'
assert struct.unpack('>II',(ROOT/'og-image.png').read_bytes()[16:24])==(1200,630)
assert manifest['scope']=='/' and manifest['start_url']=='/'
assert manifest['display']=='browser' and manifest['display_override']==['minimal-ui','browser']
assert {icon['purpose'] for icon in manifest['icons']}=={'any','maskable'}
for purpose in ['any','maskable']:
 assert {i['sizes'] for i in manifest['icons'] if i['purpose']==purpose}=={'192x192','512x512'}
for screenshot in manifest['screenshots']:
 data=(ROOT/urlsplit(screenshot['src']).path.lstrip('/')).read_bytes()
 w,h=struct.unpack('>II',data[16:24]);assert screenshot['sizes']==f'{w}x{h}'
for name in ['apple-touch-icon.png','favicon-16.png','favicon-32.png','favicon-48.png']:
 expected=180 if name.startswith('apple') else int(name.split('-')[1].split('.')[0])
 assert struct.unpack('>II',(ROOT/name).read_bytes()[16:24])==(expected,expected)
ico=(ROOT/'favicon.ico').read_bytes();assert struct.unpack('<HHH',ico[:6])==(0,1,4)
assert {ico[6+16*i] for i in range(4)}=={16,32,48,64}
assert 'prefers-color-scheme:dark' in (ROOT/'favicon.svg').read_text()
ET.parse(ROOT/'favicon.svg');ET.parse(ROOT/'safari-pinned-tab.svg')
ET.parse(ROOT/'sitemap.xml')
assert 'Sitemap: https://djnaoyaman.github.io/sitemap.xml' in (ROOT/'robots.txt').read_text()
print('PASS: IDs, local assets, anchors, CSP, 404 noindex, 12-project JSON-LD/docs, manifest dimensions, OGP, sitemap')
