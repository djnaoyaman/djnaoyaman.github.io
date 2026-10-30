"""Deterministic vector-to-raster identity exports; Pillow only, no network."""
from pathlib import Path
from PIL import Image,ImageDraw
import runpy
ROOT=Path(__file__).resolve().parents[1];mark=runpy.run_path(str(ROOT/'tools/build-mark.py'),run_name='__main__')
def raster(size,tab=False):
 im=Image.new('RGB',(size*8,size*8),mark['PAPER']);d=ImageDraw.Draw(im)
 for polygon in mark['polygons'](tab):d.polygon([(x*size*8/64,y*size*8/64) for x,y in polygon],fill=mark['INK'])
 return im.resize((size,size),Image.Resampling.LANCZOS)
for name,size in [('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512),('icon-maskable-192.png',192),('icon-maskable-512.png',512),('favicon-16.png',16),('favicon-32.png',32),('favicon-48.png',48)]:raster(size,name.startswith('favicon-')).save(ROOT/name,optimize=True)
raster(64,True).save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
runpy.run_path(str(ROOT/'tools/render-share-card.py'))
