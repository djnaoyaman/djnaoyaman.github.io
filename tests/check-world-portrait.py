"""Preserve the exact user-approved portrait, not a later approximation."""
from pathlib import Path
import hashlib,re,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];ns={'s':'http://www.w3.org/2000/svg'}
b=(R/'assets/world-portrait-approved.svg').read_bytes()
assert hashlib.sha256(b).hexdigest()=='6c0bbb6463d6b9a4f355218d2c2a217e6c23b0555d70c9c9364a04b33876505e'
a=E.fromstring(b)
h=(R/'index.html').read_text();c=E.fromstring(re.search(r'<svg[^>]*class="world-map world-portrait".*?</svg>',h,re.S)[0])
assert a.get('viewBox')==c.get('viewBox')=='360 0 840 1060'
for tag,attrs in [('path',['d','fill','fill-rule']),('polyline',['points']),('rect',['x','width','height','fill'])]:
 x=a.findall('.//s:'+tag,ns);y=c.findall('.//s:'+tag,ns)
 assert len(x)==len(y),(tag,len(x),len(y))
 assert [[e.get(k) for k in attrs] for e in x]==[[e.get(k) for k in attrs] for e in y],tag
assert len(c.findall('.//s:path[@class="portrait-plane"]',ns))==231
an=a.findall('s:a',ns);cn=c.findall('s:a',ns);assert len(an)==len(cn)==14
for i,(x,y) in enumerate(zip(an,cn)):
 assert x.get('href')==y.get('href')
 assert y.get('data-index')==str(i)
 xp=x.find('s:circle',ns);yp=y.find('s:circle[@class="world-point"]',ns)
 assert all(xp.get(k)==yp.get(k) for k in ['cx','cy','r','fill','stroke','stroke-width'])
 xt=x.find('s:text',ns);yt=y.find('s:text',ns)
 assert xt.text==yt.text==f'{i+1:02d}'
 assert all(xt.get(k)==yt.get(k) for k in xt.attrib)
for text in a.findall('s:text',ns):
 matches=[t for t in c.findall('.//s:text',ns) if t.text==text.text]
 assert len(matches)==1 and all(matches[0].get(k)==v for k,v in text.attrib.items())
assert not c.findall('.//s:image',ns)
print('PASS: approved SVG digest, all 231 plane paths, outline/clip, mesh,14 link points, numbers and signature preserved exactly; no raster embed')
