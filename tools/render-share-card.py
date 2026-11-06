"""Page-specific social cards from the same native-vector identity."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import runpy,io,cairosvg
ROOT=Path(__file__).resolve().parents[1];mark=runpy.run_path(str(ROOT/'tools/build-mark.py'))
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';SERIF=next(str(p) for p in [Path('/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf'),Path('/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf')] if p.is_file())
CARDS=[('og-image.png',['ずーっと、','あれも、これも。'],'音楽、表現、自然と文化、暮らしと学び。','djnaoyaman.github.io'),('og-profile.png',['好きなものを、','調べて、つくる。'],'音楽も、言葉も、日々の発見も。','djnaoyaman.github.io/profile.html'),('og-404.png',['ページが','見つかりません。'],'404 / NOT FOUND — それぞれの世界からお探しください。','djnaoyaman.github.io')]
CARDS.append(('og-mina.png',['点がつながり、','私の形になる。'],'M・I・N・A。点と線から、ひとつの形へ。','djnaoyaman.github.io/mina.html'))
for filename,lines,caption,url in CARDS:
 im=Image.new('RGB',(1200,630),mark['PAPER']);draw=ImageDraw.Draw(im)
 icon=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=mark['svg'](tab=True).encode(),output_width=42*4,output_height=42*4))).convert('RGB').resize((42,42),Image.Resampling.LANCZOS);im.paste(icon,(72,45))
 draw.text((132,46),'MINA',font=ImageFont.truetype(SERIF,34),fill=mark['INK'])
 for n,line in enumerate(lines):
  draw.text((72,167+n*107),line,font=ImageFont.truetype(FONT,72),fill=mark['INK'])
 draw.line((72,510,1128,510),fill='#d7d6ce',width=1);draw.text((72,535),caption,font=ImageFont.truetype(FONT,18),fill='#64655d');draw.text((72,578),url,font=ImageFont.truetype(SERIF,17),fill='#64655d');im.save(ROOT/filename,optimize=True)
