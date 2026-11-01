"""Behavioral checks for the lightweight WORLD network, run in CI."""
from pathlib import Path
from urllib.parse import urlsplit
import json,re,mimetypes,os,shutil
from playwright.sync_api import sync_playwright,expect
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parents[1];ORIGIN='https://djnaoyaman.github.io'
def serve(route):
 path=ROOT/(urlsplit(route.request.url).path.lstrip('/') or 'index.html')
 route.fulfill(status=200 if path.is_file() else 404,body=(path if path.is_file() else ROOT/'404.html').read_bytes(),content_type=mimetypes.guess_type(path)[0] or 'text/html')
items=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',(ROOT/'index.html').read_text(),re.S)[1])['@graph'][2]['mainEntity']['itemListElement']
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1280,'height':900});context.route('**/*',serve);page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(ORIGIN+'/');atlas=page.locator('.world-atlas');atlas.scroll_into_view_if_needed()
 assert page.locator('.world-node').count()==14
 assert [ORIGIN+x for x in page.locator('.world-node').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')]==[x['item']['url'] for x in items]
 expect(atlas).to_have_attribute('data-phase','complete',timeout=15000)
 assert page.locator('.world-edge').evaluate_all('(els)=>els.every(e=>getComputedStyle(e).strokeDasharray==="none")')
 (ROOT/'screenshots').mkdir(exist_ok=True)
 atlas.screenshot(path=str(ROOT/'screenshots/worlds-motion-complete.png'))
 page.locator('.world-node').first.focus()
 for i in range(14):
  assert page.locator('.world-node').nth(i).evaluate('(e)=>e===document.activeElement')
  if i<13:page.keyboard.press('Tab')
 first=page.locator('.world-node').first;first.focus();assert page.locator('#world-caption-name').inner_text()==items[0]['item']['name'];assert page.locator('.world-edge.is-connected').count()>0
 page.locator('.world-replay').click();assert atlas.get_attribute('data-phase')=='building'
 page.locator('footer').scroll_into_view_if_needed();expect(atlas).to_have_class(re.compile(r'.*is-paused.*'))
 t=page.locator('.world-signature').evaluate('(e)=>e.getAnimations()[0].currentTime');page.wait_for_timeout(200);assert abs(page.locator('.world-signature').evaluate('(e)=>e.getAnimations()[0].currentTime')-t)<35
 atlas.scroll_into_view_if_needed();expect(atlas).not_to_have_class(re.compile(r'.*is-paused.*'))
 page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'))");assert 'is-paused' in atlas.get_attribute('class')
 page.evaluate("Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'))")
 for width in [280,320,390,600,768,1280,1920]:
  page.set_viewport_size({'width':width,'height':900});page.wait_for_timeout(70);assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert page.locator('.world-hit').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().width>=43.5)'),width
 # Every visible point resolves to its own link despite responsive hit-area growth.
 for width,height in [(280,900),(390,844),(844,390),(1280,900)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(70)
  for i in range(14):
   point=page.locator('.world-point').nth(i);point.scroll_into_view_if_needed()
   assert point.evaluate('e=>{const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2).closest(".world-node")===e.closest(".world-node")}'),(width,i,'occluded link')
 # All links remain individually focusable; labels and the signature never collide.
 for width,height in [(280,900),(390,844),(844,390),(1280,900)]:
  page.set_viewport_size({'width':width,'height':height});page.wait_for_timeout(70)
  for i in range(14):
   node=page.locator('.world-node').nth(i);node.focus()
   assert atlas.get_attribute('data-active')==str(i)
   assert page.locator('#world-caption-name').inner_text()==items[i]['item']['name']
  assert page.locator('.world-number, .world-signature-name, .world-signature-note').evaluate_all("""els=>{
   const r=els.map(e=>e.getBoundingClientRect());
   return r.every((a,i)=>r.slice(i+1).every(b=>a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top));
  }"""), (width,height,'label collision')
 page.goto(ORIGIN+'/?theme=music#worlds');page.locator('.world-node').first.focus();page.locator('.world-node').first.press('Enter');assert page.url==items[0]['item']['url'];page.go_back();assert page.locator('.project:visible').count()==4
 reduced=browser.new_context(reduced_motion='reduce',viewport={'width':1280,'height':900});reduced.route('**/*',serve);q=reduced.new_page();q.goto(ORIGIN+'/');assert q.locator('.world-atlas').get_attribute('data-phase')=='complete';assert not q.locator('.world-replay').is_visible();assert q.locator('.world-signature').evaluate('(e)=>getComputedStyle(e).opacity')=='1'
 (ROOT/'screenshots').mkdir(exist_ok=True)
 q.locator('.world-atlas').screenshot(path=str(ROOT/'screenshots/worlds-desktop.png'))
 q.locator('.world-map').screenshot(path=str(ROOT/'screenshots/worlds-approved-integrated.png'))
 reference=browser.new_context(reduced_motion='reduce',viewport={'width':560,'height':800})
 ref=reference.new_page();ref.set_content('<style>body{margin:0}svg{display:block;width:560px;height:auto}</style>'+(ROOT/'assets/world-portrait-approved.svg').read_text())
 ref.locator('svg').screenshot(path=str(ROOT/'screenshots/worlds-approved-reference.png'))
 visual='els=>els.map(e=>{const s=getComputedStyle(e);return [s.fill,s.stroke,s.strokeWidth,s.strokeOpacity,s.opacity,s.fontFamily,s.fontSize,s.letterSpacing,s.textAnchor]})'
 for rs,cs in [('path.portrait-plane','.portrait-plane'),('svg>a>circle','.world-point'),('svg>a>text','.world-number'),('svg>text:nth-last-child(2)','.world-signature-name'),('svg>text:last-child','.world-signature-note')]:
  # Typography is relevant only to text; other shapes inherit unrelated page defaults.
  a=ref.locator(rs).evaluate_all(visual);b=q.locator(cs).evaluate_all(visual)
  if 'text' not in rs:a=[x[:5] for x in a];b=[x[:5] for x in b]
  assert a==b,(rs,a[:1],b[:1],'approved presentation changed')
 # Normalize only the screenshot origin to avoid fractional page-position crops.
 # Serialize actual computed presentation; do not redraw/simplify any geometry.
 normalized=q.locator('.world-map').evaluate("""svg=>{
  const clone=svg.cloneNode(true), source=[svg,...svg.querySelectorAll('*')], target=[clone,...clone.querySelectorAll('*')];
  const props=['fill','fill-opacity','fill-rule','stroke','stroke-width','stroke-opacity','stroke-dasharray','stroke-dashoffset','vector-effect','font-family','font-size','font-weight','font-style','letter-spacing','text-anchor','paint-order','opacity','visibility'];
  source.forEach((e,i)=>{const s=getComputedStyle(e);props.forEach(k=>target[i].style.setProperty(k,s.getPropertyValue(k)))});
  clone.style.cssText+=';display:block;width:560px;height:auto;margin:0;max-width:none';
  return clone.outerHTML;
 }""")
 aligned=reference.new_page();aligned.set_content('<style>body{margin:0}</style>'+normalized)
 aligned.locator('svg').screenshot(path=str(ROOT/'screenshots/worlds-approved-integrated-aligned.png'))
 a=Image.open(ROOT/'screenshots/worlds-approved-reference.png').convert('RGB')
 b=Image.open(ROOT/'screenshots/worlds-approved-integrated-aligned.png').convert('RGB')
 assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None,'approved portrait pixels changed'
 reference.close()
 q.set_viewport_size({'width':390,'height':844});q.locator('.world-atlas').screenshot(path=str(ROOT/'screenshots/worlds-mobile.png'))
 q.set_viewport_size({'width':844,'height':390});q.locator('.world-atlas').screenshot(path=str(ROOT/'screenshots/worlds-landscape.png'))
 q.locator('.world-directory summary').click();assert q.locator('.world-directory li a').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height>=44)')
 nojs=browser.new_context(java_script_enabled=False);nojs.route('**/*',serve);n=nojs.new_page();n.goto(ORIGIN+'/');assert n.locator('.world-node').count()==14;n.set_viewport_size({'width':390,'height':844});n.locator('.world-atlas').screenshot(path=str(ROOT/'screenshots/worlds-nojs-mobile.png')); assert not n.locator('.world-replay').is_visible();n.locator('.world-directory summary').click();assert n.locator('.world-directory li a:visible').count()==14
 assert not errors,errors
 browser.close()
print('PASS: 14 real WORLD links, sequence, replay, focus, offscreen/visibility pause, 7 sizes, touch targets, navigation/back, reduced motion, no-JS')
