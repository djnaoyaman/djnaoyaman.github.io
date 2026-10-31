"""Deterministic crown exports. Build-time CairoSVG and Pillow; no browser runtime dependencies."""
from pathlib import Path
from PIL import Image
import runpy,io,cairosvg
ROOT=Path(__file__).resolve().parents[1];mark=runpy.run_path(str(ROOT/'tools/build-mark.py'),run_name='__main__')
def raster(size,tab=False,maskable=False):
 raw=cairosvg.svg2png(bytestring=mark['svg'](tab=tab,maskable=maskable).encode(),output_width=size*8,output_height=size*8)
 return Image.open(io.BytesIO(raw)).convert('RGB').resize((size,size),Image.Resampling.LANCZOS)
for name,size in [('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512),('icon-maskable-192.png',192),('icon-maskable-512.png',512),('favicon-16.png',16),('favicon-32.png',32),('favicon-48.png',48)]:raster(size,name.startswith('favicon-'),'maskable' in name).save(ROOT/name,optimize=True)
raster(64,True).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
runpy.run_path(str(ROOT/'tools/render-share-card.py'))
