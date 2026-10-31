from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.assets=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'id'in a:self.ids.append(a['id'])
  for k in ['src','href']:
   u=a.get(k,'')
   if u.startswith('/') and not u.startswith('//'):self.assets.append(urlsplit(u).path)
p=Page();s=(R/'mina.html').read_text();p.feed(s);assert len(p.ids)==len(set(p.ids));assert all((R/(a.lstrip('/') or 'index.html')).exists() for a in p.assets);assert 'index,follow' in s and 'MINAは、MIYAZAKINAOYAのブランドシンボルです' in s
for f in (R/'assets/mina-study').glob('*.svg'):ET.parse(f)
assert 'eval(' not in (R/'mina.js').read_text()
print('PASS: MINA draft IDs, local assets, SVG validity, identity process status and non-eval controls')

import json,re
d=json.loads((R/'assets/mina-study/geometric-data.json').read_text());assert len(d['frames'])==101
assert d['frames'][0]==d['paths'][0] and d['frames'][50]==d['paths'][1] and d['frames'][100]==d['paths'][2]
assert not any(re.search('[CQAS]',x) for x in d['frames'])
assert 'monogram-02' not in s and 'ベジェ' not in s

# Adopted mark: no circular white counters and identical artwork master everywhere.
master=json.loads((R/'assets/mina-study/crown-master.json').read_text())
for name in ['assets-source/mark.svg','assets-source/tab-mark.svg','favicon.svg','safari-pinned-tab.svg']:
 text=(R/name).read_text();assert master['path'] in text;assert '<circle' not in text
assert 'MINA — ブランドシンボル' in (R/'index.html').read_text()
assert '/mina.html' in (R/'sitemap.xml').read_text()
