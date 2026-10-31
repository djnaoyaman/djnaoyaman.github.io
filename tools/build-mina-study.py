"""Requires Shapely for development only. Regenerates angular contours and 101 morph samples from eight corresponding segments; no runtime dependency."""
from pathlib import Path
import json
from shapely.geometry import LineString,box
from shapely.ops import unary_union

R=Path(__file__).resolve().parents[1];out=R/'assets/mina-study';out.mkdir(exist_ok=True)
# Matched segment topology: shared stems and diagonals move, rather than swap.
stages=[[[16,156,16,44],[16,44,72,100],[72,100,128,44],[128,44,128,156],[16,44,128,156],[128,156,156,44],[156,44,184,156],[136,124,176,124]],[[32,156,32,44],[32,44,98,100],[98,100,144,44],[144,44,144,156],[32,44,164,156],[88,156,144,44],[144,44,164,156],[104,124,159,124]],[[44,156,44,44],[44,44,100,100],[100,100,156,44],[156,44,156,156],[44,44,156,156],[44,156,100,44],[100,44,156,156],[58,128,142,128]]]
def outline(lines,width=9):
 groups=[[(lines[0][0],lines[0][1])]+[(lines[i][2],lines[i][3]) for i in range(4)],[(lines[4][0],lines[4][1]),(lines[4][2],lines[4][3])],[(lines[5][0],lines[5][1]),(lines[5][2],lines[5][3]),(lines[6][2],lines[6][3])],[(lines[7][0],lines[7][1]),(lines[7][2],lines[7][3])]]
 shape=unary_union([LineString(g).buffer(width/2,cap_style=2,join_style=2) for g in groups]).intersection(box(0,44,200,156))
 def ring(coords):return 'M'+'L'.join(f'{x:.4f},{y:.4f}' for x,y in list(coords)[:-1])+'Z'
 shapes=list(shape.geoms) if hasattr(shape,'geoms') else [shape]
 return ''.join(ring(p.exterior.coords)+''.join(ring(i.coords) for i in p.interiors if __import__('shapely').geometry.Polygon(i).area>=60) for p in shapes)
def svg(d,inv=False):
 ink,paper=('#f7f6f2','#282823') if inv else ('#282823','#f7f6f2')
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{paper}"/><path d="{d}" fill="{ink}" fill-rule="evenodd"/></svg>'
paths=[outline(s) for s in stages]
for i,d in enumerate(paths):
 (out/f'geometric-{i+1:02}.svg').write_text(svg(d)+'\n')
(out/'geometric-03-inverse.svg').write_text(svg(paths[2],True)+'\n')
frames=[]
for k in range(101):
 t=k/100*2;j=min(int(t),1);v=t-j;lines=[[a+(b-a)*v for a,b in zip(s,e)] for s,e in zip(stages[j],stages[j+1])];frames.append(outline(lines))
(out/'geometric-data.json').write_text(json.dumps({'stages':stages,'paths':paths,'frames':frames,'strokeWidth':9,'baseline':[44,156]},indent=2)+'\n')
# Keep the precomputed runtime frames and no-JS initial path synchronized.
import re
js=R/'mina.js'
if js.exists():
 source=js.read_text();tail=source[source.index(';\nconst controls='):];js.write_text("'use strict';\n(()=>{const FRAMES="+json.dumps(frames,separators=(',',':'))+tail)
html=R/'mina.html'
if html.exists():html.write_text(re.sub(r'(id="morph-shape"[^>]*d=")[^"]*',lambda m:m[1]+paths[0],html.read_text()))
# Final 03 is a deliberate polygon master, not the raw stroke union.
# The last ten percent changes matching outline vertices and applies the same
# micro-bevel progressively. The exact last frame uses the approved master.
master_file=out/'final-outline.json'
if master_file.exists():
 import math
 master=json.loads(master_file.read_text())
 oldrings=[]
 for part in paths[2].strip().split('M')[1:]:
  r=[[float(v) for v in pair.split(',')] for pair in part.rstrip('Z').split('L')]
  cleaned=[]
  for i,b in enumerate(r):
   a=r[i-1];c=r[(i+1)%len(r)];cross=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
   if abs(cross)>.001:cleaned.append(b)
  oldrings.append(cleaned)
 targets=json.loads(json.dumps(master['rings']));targets[1].insert(1,[130,120.1666666667]);targets[2]=targets[2][1:]
 assert [len(x) for x in oldrings]==[len(x) for x in targets]
 def beveled(r,d):
  if not d:return r
  result=[]
  for i,b in enumerate(r):
   for p in [r[i-1],r[(i+1)%len(r)]]:
    length=math.dist(b,p);distance=min(d,length*.24);result.append([b[k]+(p[k]-b[k])*distance/length for k in [0,1]])
  return result
 def rings_path(rings):return ''.join('M'+'L'.join(f'{x:.6f},{y:.6f}' for x,y in r)+'Z' for r in rings)
 frames=[]
 for k in range(101):
  if k<=90:
   j=0 if k<=50 else 1;v=k/50 if j==0 else (k-50)/40;lines=[[a+(b-a)*v for a,b in zip(s,e)] for s,e in zip(stages[j],stages[j+1])];frames.append(outline(lines))
  else:
   v=(k-90)/10;rings=[beveled([[a+(b-a)*v for a,b in zip(p,q)] for p,q in zip(old,new)],1.5*v) for old,new in zip(oldrings,targets)];frames.append(rings_path(rings))
 paths[2]=master['path'];frames[100]=master['path']
 (out/'geometric-03.svg').write_text(svg(paths[2])+'\n');(out/'geometric-03-inverse.svg').write_text(svg(paths[2],True)+'\n')
 (out/'geometric-data.json').write_text(json.dumps({'stages':stages,'paths':paths,'frames':frames,'strokeWidth':9,'baseline':[44,156],'finalMaster':'final-outline.json','cornerBevel':1.5},indent=2)+'\n')
 source=js.read_text();tail=source[source.index(';\nconst controls='):];js.write_text("'use strict';\n(()=>{const FRAMES="+json.dumps(frames,separators=(',',':'))+tail)
