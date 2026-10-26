"""Outline the header's Arial-compatible bold N; no raster image editing.
Usage: python tools/build-mark.py /path/to/LiberationSans-Bold.ttf
The resulting SVGs are committed, so normal rendering needs no fontTools.
"""
import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
ROOT=Path(__file__).resolve().parents[1]
font=TTFont(sys.argv[1]);glyphs=font.getGlyphSet();name=font.getBestCmap()[ord('N')]
pen=SVGPathPen(glyphs);glyphs[name].draw(pen);path=pen.getCommands()
bounds=BoundsPen(glyphs);glyphs[name].draw(bounds);x0,y0,x1,y1=bounds.bounds

def mark(height,adaptive=False,pinned=False):
 scale=height/(y1-y0);tx=32-scale*(x0+x1)/2;ty=32+scale*(y0+y1)/2
 style='<style>.paper{fill:#fff}.ink{fill:#191919}@media(prefers-color-scheme:dark){.paper{fill:#191919}.ink{fill:#fff}}</style>' if adaptive else ''
 paper='' if pinned else '<rect class="paper" width="64" height="64" fill="#fff"/>'
 glyph=f'<path class="ink" fill="#191919" transform="matrix({scale:.8f} 0 0 {-scale:.8f} {tx:.8f} {ty:.8f})" d="{path}"/>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{style}{paper}{glyph}</svg>\n'
for name,content in [('assets-source/mark.svg',mark(36)),('assets-source/tab-mark.svg',mark(48)),('favicon.svg',mark(48,adaptive=True)),('safari-pinned-tab.svg',mark(48,pinned=True))]:(ROOT/name).write_text(content)
print('Outlined the same bold sans-serif N as the header, centered by glyph bounds.')
