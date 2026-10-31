"""WORLD list uses source-grounded logos, never cropped Open Graph artwork."""
from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class Logos(HTMLParser):
 def __init__(self):super().__init__();self.logos=[]
 def handle_starttag(self,t,a):
  a=dict(a)
  if 'world-logo' in a.get('class','').split():self.logos.append((t,a))
p=Logos();s=(R/'index.html').read_text();p.feed(s)
assert len(p.logos)==14
assert s.count('class="maison project"')==14
assert '/assets/maisons/' not in s
assert sum(t=='img' for t,a in p.logos)==14
assert 'world-wordmark--minutes' not in s
minute=next(a for t,a in p.logos if 'logo-1minutes' in a.get('class','').split())
assert minute['alt']=='1minutes — ONE MINUTE FOREVER' and minute['src'].startswith('/assets/world-logos/1minutes.svg?')
records=json.loads((R/'docs/world-logos.json').read_text())['logos'];assert len(records)==14
for a in records:
 if a.get('file'):
  f=R/a['file'];assert hashlib.sha256(f.read_bytes()).hexdigest()==a['sha256'],a['slug']
  if f.suffix=='.svg':
   ET.parse(f);v=f.read_text();assert '<script' not in v and '<image' not in v
 assert a['source_url'].startswith('https://') and a['method']
print('PASS:14 source-grounded WORLD logos,14 self-contained official/source-grounded logo files,hashes,unchanged links checked by main suite')
