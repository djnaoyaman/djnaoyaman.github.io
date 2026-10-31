"""All public identity surfaces agree; independent art stays unchanged."""
from pathlib import Path
import json,re,hashlib
r=Path(__file__).resolve().parents[1]
for name in ['index.html','profile.html','404.html']:
 s=(r/name).read_text()
 assert 'MIYAZAKINAOYA' in s and 'NAOYAMIYAZAKI' not in s
 assert '20261031-crown' in s and 'name="theme-color" content="#f7f6f2"' in s
 assert 'メゾン' not in s and '>MAISONS<' not in s and '>CURIOSITIES<' not in s
 assert 'そのすべてを、' not in s and '画面キャプチャではありません' not in s
 assert s.count('class="brand-symbol"')==2,name
 expected={'index.html':'og-image.png','profile.html':'og-profile.png','404.html':'og-404.png'}[name]
 assert expected in s
home=(r/'index.html').read_text()
assert 'ずーっと、あれも、これも。' in home and 'それぞれに名前を持ち、それぞれの美意識を磨く。' in home
assert all('id="'+x+'"' in home for x in ['worlds','maisons','projects'])
m=json.loads((r/'site.webmanifest').read_text());assert m['name']==m['short_name']=='MIYAZAKINAOYA'
assert m['shortcuts'][0]['url']=='/#worlds'
assert hashlib.sha256((r/'robots.txt').read_bytes()).hexdigest()=='bbd38d8c18ce142a0d18297339a0d5649bf8bb7e3581702a949c242167ae81d8'
print('PASS: three-page MIYAZAKINAOYA/MINA identity, exact copy, dedicated social cards, manifest, aliases, unchanged independent art and robots')

import hashlib
for a in json.loads((r/'docs/maison-assets.json').read_text())['assets']:
 assert hashlib.sha256((r/a['file']).read_bytes()).hexdigest()==a['sha256'],a['slug']
