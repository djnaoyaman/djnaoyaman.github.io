"""Buncho WORLD integration: exact logo, accessible links, mobile and live release."""
from pathlib import Path
from datetime import date
from urllib.parse import urlsplit
import hashlib,json,mimetypes,os,shutil,time,urllib.request,io
from PIL import Image
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[1];O='https://djnaoyaman.github.io';PUBLIC=os.environ.get('PUBLIC_QA')=='1';NAME='文鳥♬文鳥♬文鳥って嬉しいな♪'
RELEASE_DATE=date.fromisoformat(json.loads((R/'site-update.json').read_text())['date'])
RELEASE_LABEL=f'{RELEASE_DATE.year}年{RELEASE_DATE.month}月{RELEASE_DATE.day}日（JST）'
LOGO='/assets/world-logos/buncho-ureshi-refined04-transparent.webp';TARGET=O+'/buncho-ureshi/'
report={'mode':'public' if PUBLIC else 'candidate','cases':[],'external_requests_blocked':[]}
original=Image.open(R/'assets/world-logos/buncho-ureshi-refined04.webp').convert('RGB')
transparent=Image.open(R/LOGO.lstrip('/')).convert('RGBA')
assert transparent.size==original.size==(1120,645)
assert transparent.convert('RGB').tobytes()==original.tobytes(),'Original logo RGB must remain exact'
alpha=transparent.getchannel('A');assert alpha.getextrema()==(0,255)
assert sum(value==0 for value in alpha.getdata())/(1120*645)>.75
assert transparent.getpixel((790,100))[3]==255,'White bird must remain opaque'
assert all(v==0 for box in [(0,0,1120,1),(0,644,1120,645),(0,0,1,645),(1119,0,1120,645)] for v in alpha.crop(box).getdata())
report['alpha_and_original_rgb']='pass'
assert '/maisons.css?v=20261114-game' in (R/'index.html').read_text(),'Returning visitors must request untinted stylesheet' 

def read(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Cache-Control':'no-cache'}),timeout=25) as response:return response.status,response.read()
if PUBLIC:
 # Do not test an older Pages release or call an unchanged page proof of this commit.
 expected=(R/'index.html').read_bytes();deadline=time.monotonic()+180
 while True:
  status,body=read(O+'/?release='+os.environ.get('GITHUB_SHA','qa'))
  if status==200 and body==expected:break
  assert time.monotonic()<deadline,'Exact main HTML not deployed within 180 seconds'
  time.sleep(8)
 for url,expected in [(O+LOGO,(R/LOGO.lstrip('/')).read_bytes()),(TARGET+'brand/wordmark-04-transparent.webp',(R/LOGO.lstrip('/')).read_bytes())]+[(O+'/'+f,(R/f).read_bytes()) for f in ['maisons.css','world-atlas.js']]:
  status,body=read(url);assert status==200 and body==expected,url
 report['public_index_sha256']=hashlib.sha256((R/'index.html').read_bytes()).hexdigest();report['logo_sha256']=hashlib.sha256((R/LOGO.lstrip('/')).read_bytes()).hexdigest();report['public_assets_exact']=['Buncho logo','source-site logo','maisons.css','world-atlas.js']
def route(request):
 u=urlsplit(request.request.url);path=R/(u.path.lstrip('/') or 'index.html')
 if u.scheme!='https' or u.netloc!='djnaoyaman.github.io' or request.request.method not in ('GET','HEAD'):
  report['external_requests_blocked'].append(u.hostname);return request.abort()
 if PUBLIC:
  if path.is_file() or u.path.startswith('/buncho-ureshi/'):return request.continue_()
  return request.abort()
 request.fulfill(status=200 if path.is_file() else 404,body=(path if path.is_file() else R/'404.html').read_bytes(),content_type=mimetypes.guess_type(path)[0] or 'text/html')
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
 c=b.new_context(reduced_motion='reduce',service_workers='block');c.route('**/*',route);q=c.new_page();errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 (R/'screenshots').mkdir(exist_ok=True)
 for w,h in [(280,900),(320,844),(390,844),(844,390),(1280,900),(1920,1080)]:
  q.set_viewport_size({'width':w,'height':h});q.goto(O+'/',wait_until='networkidle');card=q.locator('#project-buncho-ureshi');card.scroll_into_view_if_needed();logo=card.locator('img');logo.evaluate('e=>e.decode()')
  assert q.locator('.maison.project').count()==17
  game=q.locator('#project-buncho-game')
  assert game.locator('h3').inner_text()=='おもちの文鳥ぐらし'
  assert game.locator('.visit').get_attribute('href')=='/buncho-ureshi/game/'
  assert game.evaluate('e=>e.previousElementSibling.id')=='project-buncho-ureshi'
  assert game.locator('img').get_attribute('src')=='/assets/world-logos/buncho-game.png'
  assert game.evaluate('e=>e.scrollWidth<=e.clientWidth')
  expect(q.locator('#world-caption-category')).to_have_text('17 WORLDS')
  assert card.locator('h3').inner_text()==NAME and logo.get_attribute('alt')==NAME
  assert logo.get_attribute('src')==LOGO
  frame=card.locator('.art-link');image=Image.open(io.BytesIO(frame.screenshot(scale='css'))).convert('RGB')
  pixels=logo.evaluate('''e=>{const r=e.getBoundingClientRect(),p=e.parentElement.getBoundingClientRect(),s=getComputedStyle(e);return {blend:s.mixBlendMode,background:getComputedStyle(e.parentElement).backgroundColor,points:[[r.x-p.x+2,r.y-p.y+2],[r.right-p.x-3,r.y-p.y+2],[r.x-p.x+2,r.bottom-p.y-3],[r.right-p.x-3,r.bottom-p.y-3]]}}''')
  assert pixels['blend']=='normal'
  assert logo.evaluate('e=>getComputedStyle(e).filter')=='none'
  expected=[int(x.strip()) for x in pixels['background'].removeprefix('rgb(').removesuffix(')').split(',')]
  for x,y in pixels['points']:
   actual=image.getpixel((int(x),int(y)));assert all(abs(a-b)<=2 for a,b in zip(actual,expected)),(w,actual,expected)
  assert q.locator('.world-logo:not(.logo-buncho-ureshi)').evaluate_all('els=>els.every(e=>getComputedStyle(e).mixBlendMode==="normal")')
  assert logo.evaluate('e=>[e.naturalWidth,e.naturalHeight]')==[1120,645]
  assert card.locator('.description').inner_text()=='文鳥のことを、子どもといっしょに学ぶ図鑑。写真やクイズで知り、ゲームやアートづくりも楽しめます。'
  assert card.evaluate('e=>e.scrollWidth<=e.clientWidth')
  assert card.locator('h3,.description').evaluate_all('els=>els.every(e=>e.scrollWidth<=e.clientWidth)')
  assert q.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert card.locator('.art-link').get_attribute('href')==card.locator('.visit').get_attribute('href')=='/buncho-ureshi/'
  assert card.locator('.source-link').get_attribute('href')=='https://github.com/djnaoyaman/buncho-ureshi'
  if w in (320,390,1280):card.screenshot(path=str(R/f'screenshots/buncho-{report["mode"]}-card-{w}.png'))
  q.locator('button[data-theme="life"]').click();assert card.is_visible() and q.locator('.project:visible').count()==5
  q.locator('button[data-theme="music"]').click();assert not card.is_visible() and q.locator('.project:visible').count()==4
  # Exercise keyboard focus without a stale mouse hover at the scroll destination.
  q.mouse.move(0,0)
  node=q.locator('.world-node[href="/buncho-ureshi/"]');node.focus();assert node.get_attribute('href')=='/buncho-ureshi/'
  expect(q.locator('#world-caption-name')).to_have_text(NAME)
  assert node.evaluate('e=>e===document.activeElement')
  assert q.locator('.world-edge.is-connected').count()>0
  report['cases'].append({'viewport':[w,h],'card_logo_title_filter_node':'pass'})
 q.goto(O+'/',wait_until='networkidle')
 with q.expect_response(lambda response: response.url==TARGET and response.request.resource_type=='document') as destination:
  q.locator('#project-buncho-ureshi .visit').click()
 assert q.url==TARGET
 if PUBLIC:assert destination.value.status==200
 if PUBLIC:
  q.wait_for_load_state('networkidle');assert NAME in q.title();report['live_destination']='HTTP200 confirmed by initial document and correct title'
 nojs=b.new_context(java_script_enabled=False,viewport={'width':390,'height':844});nojs.route('**/*',route);n=nojs.new_page();n.goto(O+'/');assert n.locator('#project-buncho-ureshi').is_visible();n.locator('.world-directory summary').click();assert n.locator('.world-directory a[href="/buncho-ureshi/"]').is_visible();assert n.locator('[data-site-updated]').inner_text()==RELEASE_LABEL;report['no_javascript']='pass'
 assert not errors,errors;b.close()
report['status']='pass';(R/f'screenshots/buncho-{report["mode"]}-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
