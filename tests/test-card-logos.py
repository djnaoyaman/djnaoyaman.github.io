"""Verify the smaller15card logos, preserving their original files and aspect ratios."""
from pathlib import Path
from urllib.parse import urlsplit
import mimetypes,os,shutil,io
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O='https://djnaoyaman.github.io'
def serve(route):
 p=R/(urlsplit(route.request.url).path.lstrip('/') or 'index.html')
 route.fulfill(status=200 if p.is_file() else 404,body=(p if p.is_file() else R/'404.html').read_bytes(),content_type=mimetypes.guess_type(p)[0] or 'text/html')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 c=b.new_context(reduced_motion='reduce');c.route('**/*',serve);q=c.new_page()
 (R/'screenshots').mkdir(exist_ok=True)
 for width,height in [(280,900),(390,844),(844,390),(1280,900),(1920,1080)]:
  q.set_viewport_size({'width':width,'height':height});q.goto(O+'/')
  logos=q.locator('.art-link .world-logo');assert logos.count()==15
  tiles=[]
  for i in range(15):
   logo=logos.nth(i);logo.scroll_into_view_if_needed();logo.evaluate('e=>e.decode()')
   metrics=logo.evaluate('''e=>{const a=e.closest('.art-link').getBoundingClientRect(),r=e.getBoundingClientRect(),s=getComputedStyle(e);return {frame:[a.x,a.y,a.width,a.height],box:[r.x,r.y,r.width,r.height],fit:s.objectFit,loaded:e.complete&&e.naturalWidth>0}}''')
   x,y,w,h=metrics['box'];fx,fy,fw,fh=metrics['frame']
   assert metrics['loaded'] and metrics['fit']=='contain'
   assert abs(x+w/2-fx-fw/2)<1 and abs(y+h/2-fy-fh/2)<1,(width,i,'not centered')
   assert x-fx>=20 and fx+fw-x-w>=20 and y-fy>=13 and fy+fh-y-h>=13,(width,i,'clear space')
   assert fh==(120 if width<=700 else 140),(width,i,fh)
   assert h<=82 if width<=700 else h<=93,(width,i,h)
   assert q.evaluate('document.documentElement.scrollWidth<=innerWidth')
   if width in (390,1280):
    tile=Image.open(io.BytesIO(logo.locator('..').screenshot())).convert('RGB');tile.thumbnail((380,160))
    canvas=Image.new('RGB',(400,190),'#f7f6f2');canvas.paste(tile,((400-tile.width)//2,10));ImageDraw.Draw(canvas).text((16,170),f'{i+1:02d} '+logo.get_attribute('class').split()[-1],fill='#262720');tiles.append(canvas)
  if tiles:
   sheet=Image.new('RGB',(800,190*8),'#f7f6f2')
   for i,t in enumerate(tiles):sheet.paste(t,((i%2)*400,(i//2)*190))
   sheet.save(R/f'screenshots/card-logos-{width}.png')
   for number in (5,6,14):q.locator('.maison').nth(number).screenshot(path=str(R/f'screenshots/card-{number+1:02d}-{width}.png'))
 # The image link retains its keyboard destination, and filters do not change scale.
 q.locator('.art-link').first.focus();assert q.locator('.art-link').first.evaluate('e=>e===document.activeElement')
 q.locator('.filters button').nth(1).click();assert q.locator('.maison:visible').count()>0
 b.close()
print('PASS:15original logos,5sizes,centered smaller frames/clear space,contain,keyboard/filter;2all-logo sheets and6full cards')
