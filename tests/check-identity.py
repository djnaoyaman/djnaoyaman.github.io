"""All public identity surfaces agree; independent art stays unchanged."""
from pathlib import Path
import json,re,hashlib
r=Path(__file__).resolve().parents[1]
for name in ['index.html','profile.html','404.html','mina.html']:
 s=(r/name).read_text()
 assert 'MINA' in s and not re.search(r'MIYAZAKI|NAOYA|宮崎\s*直哉',s)
 assert '20261031-crown' in s and 'name="theme-color" content="#f7f6f2"' in s
 assert 'メゾン' not in s and '>MAISONS<' not in s and '>CURIOSITIES<' not in s
 assert 'そのすべてを、' not in s and '画面キャプチャではありません' not in s
 assert s.count('class="brand-symbol"')==2,name
 expected={'index.html':'og-image.png','profile.html':'og-profile.png','404.html':'og-404.png','mina.html':'og-mina.png'}[name]
 assert expected in s
home=(r/'index.html').read_text()
assert 'ずーっと、あれも、これも。' in home and 'それぞれに名前を持ち、それぞれの美意識を磨く。' in home
assert all('id="'+x+'"' in home for x in ['worlds','maisons','projects'])
m=json.loads((r/'site.webmanifest').read_text());assert m['name']==m['short_name']=='MINA'
assert m['shortcuts'][0]['url']=='/#worlds'
assert hashlib.sha256((r/'robots.txt').read_bytes().replace(b'Sitemap: https://djnaoyaman.github.io/buncho-ureshi/sitemap.xml\n',b'')).hexdigest()=='0774290ac371fab4e63dd73309a471e0d177d7933be0c69e03a6791690986a20'
print('PASS: four-page MINA identity, exact copy, dedicated social cards, manifest, aliases, unchanged independent art and robots')

import hashlib
for a in json.loads((r/'docs/maison-assets.json').read_text())['assets']:
 assert hashlib.sha256((r/a['file']).read_bytes()).hexdigest()==a['sha256'],a['slug']

# Brand name is consistent in machine-readable data, install previews and share artwork.
for name in ['llms.txt','llms-full.txt','site.webmanifest','site.js','assets/world-portrait-approved.svg','assets-source/share-card.html','tools/render-share-card.py']:
 text=(r/name).read_text()
 assert not re.search(r'MIYAZAKI|NAOYA|宮崎\s*直哉',text),name
assert '<h1>MINA</h1>' in (r/'profile.html').read_text()
assert '<span>© 2026 MINA</span>' in home
assert 'M・I・N・Aの4文字から' in (r/'mina.html').read_text()
for page in ['index.html','profile.html','404.html','mina.html']:
 text=(r/page).read_text()
 assert '<meta name="application-name" content="MINA">' in text
 assert '<meta property="og:site_name" content="MINA">' in text
 assert '/site.webmanifest?v=20261106-mina' in text
 assert re.search(r'og-(image|profile|404|mina)\.png\?v=20261106-mina',text)
for screenshot in m['screenshots']:
 assert screenshot['label'].startswith('MINA — ')
 assert screenshot['src'].endswith('?v=20261106-mina')
print('PASS: MINA public copy, structured data, native share, app names and refreshed preview URLs')
