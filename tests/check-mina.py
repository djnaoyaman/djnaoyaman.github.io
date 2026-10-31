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
p=Page();s=(R/'mina.html').read_text();p.feed(s);assert len(p.ids)==len(set(p.ids));assert all((R/(a.lstrip('/') or 'index.html')).exists() for a in p.assets);assert 'noindex,follow' in s and '現在のサイトアイコンは変更していません' in s
for f in (R/'assets/mina-study').glob('*.svg'):ET.parse(f)
assert 'eval(' not in (R/'mina.js').read_text()
print('PASS: MINA draft IDs, local assets, SVG validity, explicit draft status and non-eval controls')
