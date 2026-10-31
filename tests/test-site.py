"""Run: python tests/test-site.py. Requires Playwright + Chromium.
Optional AXE_PATH points to a locally supplied axe-core 4 script.
"""
import json,os,re,mimetypes,shutil
from pathlib import Path
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
ORIGIN='https://djnaoyaman.github.io'

def route(request):
    path=urlparse(request.request.url).path
    local=ROOT/(path.lstrip('/') or 'index.html')
    if not local.is_file():
        request.fulfill(status=404,body=(ROOT/'404.html').read_bytes(),content_type='text/html')
    else:
        request.fulfill(body=local.read_bytes(),content_type=mimetypes.guess_type(local)[0] or 'application/octet-stream')

def audit(page):
    axe=os.environ.get('AXE_PATH')
    if axe:
        # Bypass the production CSP for the audit engine injection only.
        page.add_script_tag(content=Path(axe).read_text())
        violations=page.evaluate("async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})).violations")
        assert not violations,json.dumps(violations,ensure_ascii=False)

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox'])
    context=browser.new_context(viewport={'width':1280,'height':900})
    context.route('**/*',route)
    page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(ORIGIN+'/?utm_source=test#projects')
    assert page.locator('.project:visible').count()==14
    page.locator('button[data-theme="expression"]').click()
    assert page.locator('.project:visible').count()==3
    assert page.locator('#project-1minutes').is_visible()
    assert page.locator('#project-1minutes h3 a').get_attribute('href')=='/1minutes/'
    page.locator('button[data-theme="music"]').click()
    assert page.locator('.project:visible').count()==4
    assert page.locator('#project-premiumcuts').is_visible()
    assert 'utm_source=test' in page.url and 'theme=music' in page.url and page.url.endswith('#projects')
    page.locator('button[data-theme="life"]').click()
    assert page.locator('.project:visible').count()==3
    page.go_back();assert page.locator('button[data-theme="music"]').get_attribute('aria-pressed')=='true'
    page.reload();assert page.locator('.project:visible').count()==4
    page.emulate_media(media='print');assert page.locator('.project:visible').count()==14
    page.emulate_media(media='screen')
    page.goto(ORIGIN+'/?theme=%3Cscript%3E#projects');assert page.locator('.project:visible').count()==14
    for width in [320,375,390,600,768,1280]:
        page.set_viewport_size({'width':width,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        assert page.locator('.project-filter button').evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height>=44)')
    page.set_viewport_size({'width':390,'height':844})
    page.screenshot(path='/tmp/naoya-mobile-full.png',full_page=True)
    page.evaluate("scrollTo({top:document.querySelector('#projects').offsetTop-24,behavior:'instant'})");page.screenshot(path='/tmp/naoya-mobile-projects.png')
    page.emulate_media(reduced_motion='reduce')
    assert page.evaluate('getComputedStyle(document.documentElement).scrollBehavior')=='auto'
    page.goto(ORIGIN+'/');page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
    page.keyboard.press('Enter');assert page.locator('#main').evaluate('(e)=>e===document.activeElement')
    # Clipboard failures and native-share cancellation are expected user actions.
    page.add_init_script("Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.copied=text;if(window.failCopy)throw Error('denied')}}});Object.defineProperty(navigator,'share',{value:async data=>{window.shared=data;throw new DOMException('cancelled','AbortError')}})")
    page.reload();page.locator('#copy-link').click();page.wait_for_timeout(60)
    assert page.evaluate('window.copied')==ORIGIN+'/'
    assert 'コピーしました' in page.locator('#share-status').inner_text()
    page.evaluate('window.failCopy=true');page.locator('#copy-link').click();page.wait_for_timeout(60)
    assert ORIGIN+'/' in page.locator('#share-status').inner_text()
    page.locator('#native-share').click();assert page.locator('#share-status').inner_text()==''
    assert page.locator('#native-share').is_enabled()
    assert not errors,errors
    page.goto(ORIGIN+'/missing/deep/path?invalid=%3Cscript%3E');assert page.title().startswith('ページが見つかりません')
    assert page.locator('a[href="/#projects"]').count()==1
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    # A separate context allows axe injection without weakening the site's CSP.
    audit_context=browser.new_context(bypass_csp=True)
    audit_context.route('**/*',route)
    a=audit_context.new_page()
    for url in [ORIGIN+'/',ORIGIN+'/profile.html',ORIGIN+'/?theme=music#projects',ORIGIN+'/missing/']:
        a.goto(url);audit(a)
    nojs=browser.new_context(java_script_enabled=False);nojs.route('**/*',route)
    q=nojs.new_page();q.goto(ORIGIN+'/?theme=music');assert q.locator('.project:visible').count()==14
    assert not q.locator('.project-filter').is_visible()
    # The displayed collection and machine-readable collection must agree.
    data=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',(ROOT/'index.html').read_text(),re.S)[1])
    items=data['@graph'][2]['mainEntity']['itemListElement']
    assert len(items)==14
    q.goto(ORIGIN+'/')
    assert [item['item']['name'] for item in items]==q.locator('#project-list h3').all_text_contents()
    for node in q.locator('[src],link[href]').all():
        value=node.get_attribute('src') or node.get_attribute('href')
        if value.startswith('/'):
            assert (ROOT/urlparse(value).path.lstrip('/')).is_file(),value
    manifest=json.loads((ROOT/'site.webmanifest').read_text())
    for icon in manifest['icons']:assert (ROOT/urlparse(icon['src']).path.lstrip('/')).is_file()
    # The standalone profile must work without JavaScript, and remain readable at each width.
    q.goto(ORIGIN+'/profile.html')
    assert q.locator('h1').inner_text()=='宮崎 直哉'
    assert q.locator('.profile-works li').count()==0
    assert q.locator('a[href="/#worlds"]').count()>=1
    for width in [280,320,390,600,768,1280]:
        q.set_viewport_size({'width':width,'height':844})
        assert q.evaluate('document.documentElement.scrollWidth<=innerWidth'),('profile',width)
    q.locator('a[href="/"]').first.click()
    assert q.url==ORIGIN+'/'
    assert q.locator('a[href="/profile.html"]').count()>=1
    browser.close()
print('PASS: filters/history, 6 widths, 44px targets, print, reduced motion, keyboard, clipboard/share, no-JS, deep 404, metadata/assets'+(', axe WCAG AA' if os.environ.get('AXE_PATH') else ''))
