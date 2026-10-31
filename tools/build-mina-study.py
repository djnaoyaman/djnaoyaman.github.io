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
