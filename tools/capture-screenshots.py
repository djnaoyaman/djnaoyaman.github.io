"""Explicitly refresh manifest previews after a visible design change."""
from pathlib import Path
from urllib.parse import urlsplit
import mimetypes,os,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def serve(route):
 path=ROOT/(urlsplit(route.request.url).path.lstrip('/') or 'index.html')
 route.fulfill(body=path.read_bytes(),content_type=mimetypes.guess_type(path)[0] or 'application/octet-stream')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 context=browser.new_context(device_scale_factor=1,reduced_motion='reduce');context.route('**/*',serve)
 page=context.new_page();(ROOT/'screenshots').mkdir(exist_ok=True)
 for label,width,height in [('mobile',390,844),('desktop',1280,720)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('https://djnaoyaman.github.io/')
  page.evaluate('document.fonts.ready');page.locator('img').evaluate_all('(els)=>Promise.race([Promise.all(els.map(e=>{e.loading="eager";return e.decode()})),new Promise((_,reject)=>setTimeout(()=>reject(new Error("Image decode timeout")),15000))])');page.screenshot(path=str(ROOT/f'screenshots/{label}.png'))
  for route,name in [('profile.html','profile'),('404.html','404')]:
   page.goto('https://djnaoyaman.github.io/'+route);page.evaluate('document.fonts.ready');page.screenshot(path=str(ROOT/f'screenshots/{name}-{label}.png'))
 browser.close()
print('Refreshed actual mobile/desktop install-preview screenshots.')
