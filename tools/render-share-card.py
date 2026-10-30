"""Page-specific social cards from the same native-vector identity."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import runpy
ROOT=Path(__file__).resolve().parents[1];mark=runpy.run_path(str(ROOT/'tools/build-mark.py'))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';SERIF='/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf'
CARDS=[('og-image.png',['ずーっと、','あれも、これも。'],'音楽、表現、自然と文化、暮らしと学び。','djnaoyaman.github.io'),('og-profile.png',['宮崎 直哉','NAOYA MIYAZAKI'],'マーケティングとブランディング。音楽、文章、Web、地域。','djnaoyaman.github.io/profile.html'),('og-404.png',['ページが','見つかりません。'],'404 / NOT FOUND — それぞれの世界からお探しください。','djnaoyaman.github.io')]
for filename,lines,caption,url in CARDS:
 im=Image.new('RGB',(1200,630),mark['PAPER']);draw=ImageDraw.Draw(im)
 for polygon in mark['polygons'](True):draw.polygon([(72+x*.65,45+y*.65) for x,y in polygon],fill=mark['INK'])
 draw.text((132,46),'MIYAZAKINAOYA',font=ImageFont.truetype(SERIF,34),fill=mark['INK'])
 for n,line in enumerate(lines):
  latin=line=='NAOYA MIYAZAKI';draw.text((72,167+n*107),line,font=ImageFont.truetype(SERIF if latin else FONT,54 if latin else 72),fill=mark['INK'])
 draw.line((72,510,1128,510),fill='#d7d6ce',width=1);draw.text((72,535),caption,font=ImageFont.truetype(FONT,18),fill='#64655d');draw.text((72,578),url,font=ImageFont.truetype(SERIF,17),fill='#64655d');im.save(ROOT/filename,optimize=True)
