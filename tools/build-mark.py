"""MINA seal: MIYAZAKI + NAOYA. Original four-letter vector, not font glyphs."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PAPER='#f7f6f2';INK='#282823'
# MI / NA: an original four-letter architectural seal. Each quadrant is optically
# balanced; shared proportions, open counters and broad strokes survive at 16px.
POLYGONS=[
 [(6,6),(11,6),(18,18),(25,6),(30,6),(30,29),(25,29),(25,15),(18,27),(11,15),(11,29),(6,29)],
 [(36,6),(58,6),(58,11),(50,11),(50,24),(58,24),(58,29),(36,29),(36,24),(44,24),(44,11),(36,11)],
 [(6,35),(11,35),(24,49),(24,35),(30,35),(30,58),(25,58),(12,44),(12,58),(6,58)],
 [(35,58),(43,35),(50,35),(59,58),(53,58),(47,41),(41,58)],
 [(40,49),(54,49),(54,54),(40,54)]
]
def polygons(tab=False):
 scale=1 if tab else .65
 return [[(32+(x-32)*scale,32+(y-32)*scale) for x,y in points] for points in POLYGONS]
def svg(tab=False,adaptive=False,pinned=False):
 style=f'<style>.paper{{fill:{PAPER}}}.ink{{fill:{INK}}}@media(prefers-color-scheme:dark){{.paper{{fill:{INK}}}.ink{{fill:{PAPER}}}}}</style>' if adaptive else ''
 paper='' if pinned else f'<rect class="paper" width="64" height="64" fill="{PAPER}"/>'
 shapes=''.join('<polygon class="ink" fill="'+INK+'" points="'+' '.join(f'{x:g},{y:g}' for x,y in p)+'"/>' for p in polygons(tab))
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{style}{paper}{shapes}</svg>'
if __name__=='__main__':
 for name,content in [('assets-source/mark.svg',svg()),('assets-source/tab-mark.svg',svg(tab=True)),('favicon.svg',svg(tab=True,adaptive=True)),('safari-pinned-tab.svg',svg(tab=True,pinned=True)),('assets-source/mark-inverse.svg',svg(tab=True).replace(PAPER,'TEMP').replace(INK,PAPER).replace('TEMP',INK))]:(ROOT/name).write_text(content+'\n')
