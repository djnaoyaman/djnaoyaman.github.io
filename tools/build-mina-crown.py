from pathlib import Path
import json,io
from shapely.geometry import Polygon,Point
from shapely.ops import unary_union
import cairosvg
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[1]; A=R/'assets/mina-study'; m=json.loads((A/'final-outline.json').read_text());P='#f7f6f2';K='#282823'
base=Polygon(m['contours'][0],m['contours'][1:]); pts=json.loads((A/'dot-junctions.json').read_text())['points']; radii=[13,15,13]
shape=unary_union([base]+[Point(*p).buffer(r,resolution=128) for p,r in zip(pts[:3],radii)])
assert shape.is_valid and shape.geom_type=='Polygon'
def path(poly):
 return ' '.join('M'+' L'.join(f'{x:.5f},{y:.5f}' for x,y in list(r.coords)[:-1])+' Z' for r in [poly.exterior,*poly.interiors])
D=path(shape)
def svg(inv=False,view='0 0 200 200'):
 ink,paper=(P,K) if inv else(K,P)
 dots=''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{paper}"/>' for x,y in pts[3:])
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}"><rect x="-200" y="-200" width="600" height="600" fill="{paper}"/><g transform="translate(0 5)"><path d="{D}" fill="{ink}" fill-rule="evenodd"/>{dots}</g></svg>'
(A/'dots-crown.svg').write_text(svg());(A/'dots-crown-inverse.svg').write_text(svg(True));(A/'crown-master.json').write_text(json.dumps({'path':D,'topRadii':radii,'points':pts,'translateY':5,'construction':'boolean union of precise polygon and 3 circular terminals; inner point counters remain'},indent=2))
board=Image.new('RGB',(1500,1000),P);d=ImageDraw.Draw(board);font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def label(x,y,s,n=22):d.text((x,y),s,font=ImageFont.truetype(font,n),fill=K)
def paste(s,x,y,w):board.paste(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=s.encode(),output_width=w,output_height=w))).convert('RGB'),(x,y))
label(50,30,'MINA  /  点がつながり、私の形になる。',28)
paste(svg(),20,100,670);paste(svg(True),730,120,410)
label(80,790,'上の3点を大きく。王冠の輪郭へ。',25)
label(80,840,'円と線をひとつの輪郭に統合。角の飛び出しを除いています。',19)
for x,n in [(790,16),(890,32),(1010,64)]:paste(svg(),x,620,n);label(x,710,str(n)+'px',14)
for x,view,title in [(1180,'28 30 34 42','左の接合'),(1180,'81 26 38 45','中央の接合')]:
 y=100 if '左' in title else 420
 paste(svg(False,view),x,y,250);label(x,y+260,title,18)
board.save('/tmp/MINA-crown-point-refinement.png')
print('valid union area',shape.area,'bounds',shape.bounds)
