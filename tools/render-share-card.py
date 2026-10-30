"""Render the neutral typographic sharing card without external assets or network."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SERIF='/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf'
im=Image.new('RGB',(1200,630),'#f7f6f2');draw=ImageDraw.Draw(im)
draw.text((72,54),'NAOYAMIYAZAKI',font=ImageFont.truetype(SERIF,34),fill='#282823')
draw.text((72,167),'ずーっと、',font=ImageFont.truetype(FONT,72,index=0),fill='#282823')
draw.text((72,274),'あれも、これも。',font=ImageFont.truetype(FONT,72,index=0),fill='#282823')
draw.line((72,510,1128,510),fill='#d7d6ce',width=1)
draw.text((72,540),'音楽、表現、自然と文化、暮らしと学び。',font=ImageFont.truetype(FONT,19,index=0),fill='#64655d')
draw.text((885,545),'djnaoyaman.github.io',font=ImageFont.truetype(SERIF,20),fill='#64655d')
im.save(ROOT/'og-image.png',optimize=True)
print('Rendered NAOYAMIYAZAKI share card with current tagline')
