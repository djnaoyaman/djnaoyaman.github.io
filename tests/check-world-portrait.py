"""Preserve the exact user-approved wireframe, not a tonal portrait or redraw."""
from pathlib import Path
import hashlib,re,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];ns={'s':'http://www.w3.org/2000/svg'}
b=(R/'assets/world-portrait-approved.svg').read_bytes()
assert hashlib.sha256(b).hexdigest()=='db91d21cc1014ce306e7964f15c3c30e3a02c09512e0cbc1532b8a2c93821a7a'
a=E.fromstring(b)
h=(R/'index.html').read_text();c=E.fromstring(re.search(r'<svg[^>]*class="world-map world-portrait".*?</svg>',h,re.S)[0])
assert a.get('viewBox')==c.get('viewBox')=='260 -105 600 735'
for tag,attrs in [('path',['d','stroke','stroke-width','data-from','data-to']),('rect',['x','y','width','height','fill'])]:
 x=a.findall('.//s:'+tag,ns);y=c.findall('.//s:'+tag,ns)
 assert len(x)==len(y),(tag,len(x),len(y))
 assert [[e.get(k) for k in attrs] for e in x]==[[e.get(k) for k in attrs] for e in y],tag
assert len(c.findall('.//s:path',ns))==90
ag=a.findall('s:g',ns);cg=c.findall('s:g',ns)
for x,y in zip(ag,cg):
 assert all(y.get(k)==v for k,v in x.attrib.items())
 assert y.get('aria-hidden')=='true'
assert len(ag[1])==len(cg[1])==35
for x,y in zip(ag[1],cg[1]):assert x.attrib==y.attrib
assert len({p.get('data-from') for p in c.findall('.//s:path',ns)}|{p.get('data-to') for p in c.findall('.//s:path',ns)})==49
an=a.findall('s:a',ns);cn=c.findall('s:a',ns);assert len(an)==len(cn)==14
for i,(x,y) in enumerate(zip(an,cn)):
 assert x.get('href')==y.get('href') and x.get('aria-label')==y.get('aria-label')
 assert y.get('data-index')==str(i)
 xp=x.find('s:circle',ns);yp=y.find('s:circle[@class="world-point"]',ns)
 assert all(xp.get(k)==yp.get(k) for k in xp.attrib)
 xt=x.find('s:text',ns);yt=y.find('s:text',ns)
 assert xt.text==yt.text==f'{i+1:02d}'
 assert all(xt.get(k)==yt.get(k) for k in xt.attrib)
for text in a.findall('s:text',ns):
 matches=[t for t in c.findall('.//s:text',ns) if t.text==text.text]
 assert len(matches)==1 and all(matches[0].get(k)==v for k,v in text.attrib.items())
assert not c.findall('.//s:image',ns) and not c.findall('.//s:polygon',ns)
assert c.find('s:g[@class="world-edges"]',ns).get('fill')=='none'
print('PASS: approved wireframe digest,49 vertices/90 edges,35 noninteractive support points,14 link points/numbers/full accessible labels/signature preserved; no tonal fills or raster')
