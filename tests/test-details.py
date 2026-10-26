"""Edge cases beyond the main UI test: python tests/test-details.py.
Requires Playwright, Chromium and Pillow. Screenshots stay outside the repo.
"""
from pathlib import Path
from urllib.parse import urlsplit
import json,math,mimetypes,os,shutil
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];ORIGIN='https://djnaoyaman.github.io'
requests=[]
def serve(route):
 u=urlsplit(route.request.url);requests.append(u.path)
 assert u.netloc=='djnaoyaman.github.io',route.request.url
 file=ROOT/(u.path.lstrip('/') or 'index.html')
 status=200 if file.is_file() else 404
 if status==404:file=ROOT/'404.html'
 route.fulfill(status=status,body=file.read_bytes(),content_type=mimetypes.guess_type(file)[0] or 'application/octet-stream')
# Validate the visible artwork itself, including Android's safe circle.
for filename in ['apple-touch-icon.png','icon-192.png','icon-512.png','icon-maskable-192.png','icon-maskable-512.png']:
 im=Image.open(ROOT/filename);assert im.mode=='RGB';n=im.width
 box=ImageChops.difference(im,Image.new('RGB',im.size,'white')).getbbox()
 assert box and abs((box[0]+box[2])/2-n/2)<n*.02,(filename,box)
 assert abs((box[1]+box[3])/2-n/2)<n*.02,(filename,box)
 if 'maskable' in filename:
  for y in range(n):
   for x in range(n):
    if min(im.getpixel((x,y)))<240:
     assert math.hypot(x+.5-n/2,y+.5-n/2)<n*.4,(filename,x,y)
 assert im.mode=='RGB'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':390,'height':844});context.route('**/*',serve)
 page=context.new_page();page.goto(ORIGIN+'/')
 assert not any(path.endswith('og-image.png') or path.startswith('/screenshots/') for path in requests),'Unnecessary preview preload'
 assert sum((ROOT/name).stat().st_size for name in ['index.html','site.css','site.js'])<40000
 # Inline scripts are really blocked by the shipped policy.
 page.evaluate("()=>{let s=document.createElement('script');s.textContent='window.untrustedRan=true';document.head.append(s)}")
 assert page.evaluate('window.untrustedRan') is None
 response=page.goto(ORIGIN+'/unknown/deep/path');assert response.status==404
 assert page.locator('link[rel="apple-touch-icon"]').count()==1
 assert page.locator('link[rel="manifest"]').count()==1
 # Busy controls must recover after restoration; old async results must stay discarded.
 page.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>new Promise(resolve=>{window.finishCopy=resolve})}});Object.defineProperty(navigator,'share',{value:async()=>{throw new DOMException('cancelled','AbortError')}})")
 page.goto(ORIGIN+'/');page.locator('#copy-link').click();assert page.locator('#copy-link').is_disabled()
 page.evaluate("dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))")
 assert page.locator('#copy-link').is_enabled()
 page.evaluate('window.oldCopy=window.finishCopy')
 page.locator('#copy-link').click();assert page.locator('#copy-link').is_disabled()
 page.evaluate('window.oldCopy()');page.wait_for_timeout(60)
 assert page.locator('#copy-link').is_disabled() and page.locator('#share-status').inner_text()==''
 page.locator('#native-share').click();page.evaluate('window.finishCopy()');page.wait_for_timeout(60)
 assert page.locator('#copy-link').is_enabled() and page.locator('#share-status').inner_text()==''
 # A dedicated audit context permits test-only spacing rules without relaxing production CSP.
 audit=browser.new_context(bypass_csp=True,viewport={'width':320,'height':740});audit.route('**/*',serve)
 a=audit.new_page();a.goto(ORIGIN+'/')
 a.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}')
 assert a.evaluate('document.documentElement.scrollWidth<=innerWidth'),'Text spacing overflow'
 for width,height in [(280,700),(320,740),(844,390),(1920,1080),(2560,1440)]:
  a.set_viewport_size({'width':width,'height':height})
  assert a.evaluate('document.documentElement.scrollWidth<=innerWidth'),(width,height)
 a.screenshot(path='/tmp/naoya-text-spacing.png',full_page=True)
 a.emulate_media(forced_colors='active');a.goto(ORIGIN+'/?theme=music#projects')
 button=a.locator('button[data-theme="music"]');assert button.get_attribute('aria-pressed')=='true'
 assert button.evaluate('(e)=>getComputedStyle(e).borderTopWidth')=='2px'
 # Adaptive favicon is rendered in both schemes; the raster Apple icon stays on opaque white.
 for scheme in ['light','dark']:
  a.emulate_media(color_scheme=scheme,forced_colors='none')
  a.goto(ORIGIN+'/favicon.svg')
  a.set_viewport_size({'width':64,'height':64});a.screenshot(path=f'/tmp/naoya-favicon-{scheme}.png')
 light=Image.open('/tmp/naoya-favicon-light.png').convert('RGB');dark=Image.open('/tmp/naoya-favicon-dark.png').convert('RGB')
 assert sum(light.getpixel((0,0)))>700 and sum(dark.getpixel((0,0)))<150
 # Review circle, rounded-square and pinned-tab masks as browser-rendered UI previews.
 a.set_viewport_size({'width':900,'height':300})
 a.goto(ORIGIN+'/')
 a.set_content('''<style>body{margin:0;padding:36px;background:#eee;display:flex;gap:40px;font:14px sans-serif}figure{margin:0;text-align:center}img{width:160px;height:160px;display:block;margin-bottom:18px}.circle{border-radius:50%}.rounded{border-radius:36px}</style><figure><img class="rounded" src="/apple-touch-icon.png">Apple Touch Icon</figure><figure><img class="circle" src="/icon-maskable-512.png">Android circle</figure><figure><img class="rounded" src="/icon-maskable-512.png">Android rounded square</figure><figure><img src="/safari-pinned-tab.svg">Safari pinned tab</figure>''')
 a.locator('img').evaluate_all('(els)=>Promise.all(els.map(e=>e.decode()))')
 a.screenshot(path='/tmp/naoya-icon-masks.png')
 browser.close()
print('PASS: centered opaque icons, Android safe circles, small core payload, no preview preload, enforced CSP, real 404, restored/racing shares, text spacing, 5 extra sizes, forced colors, adaptive favicon')
