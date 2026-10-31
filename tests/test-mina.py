"""Draft process-page QA. Does not alter the live identity."""
from pathlib import Path
from urllib.parse import urlsplit
import os,shutil,mimetypes,json
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[1];O='https://djnaoyaman.github.io'
def serve(route):
 p=R/(urlsplit(route.request.url).path.lstrip('/') or 'index.html')
 route.fulfill(status=200 if p.is_file() else 404,body=(p if p.is_file() else R/'404.html').read_bytes(),content_type=mimetypes.guess_type(p)[0] or 'text/html')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),args=['--no-sandbox']);c=browser.new_context(bypass_csp=True,reduced_motion='reduce');c.route('**/*',serve);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(O+'/mina.html')
 buttons=page.locator('.construction-controls button');assert buttons.count()==3
 for i in range(3):
  buttons.nth(i).click();expect(buttons.nth(i)).to_have_attribute('aria-pressed','true');expect(page.locator('.construction')).to_have_attribute('data-stage',str(i));assert page.locator('.construction-controls [aria-pressed=true]').count()==1
 buttons.nth(2).press('ArrowRight');expect(buttons.nth(0)).to_be_focused();buttons.nth(0).press('ArrowLeft');expect(buttons.nth(2)).to_be_focused();buttons.nth(2).press('Home');expect(buttons.nth(0)).to_be_focused();buttons.nth(0).press('End');expect(buttons.nth(2)).to_be_focused()
 assert page.locator('#morph-play').is_disabled();expect(page.locator('#morph-progress')).to_have_value('100');page.locator('#morph-reset').click();expect(page.locator('#morph-progress')).to_have_value('0')
 for width in [280,320,390,600,768,1280,1920]:
  page.set_viewport_size({'width':width,'height':900});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert buttons.evaluate_all('(els)=>els.every(e=>e.getBoundingClientRect().height>=44)')
  if width in [390,1280]:
   page.evaluate('scrollTo(0,0)');page.screenshot(path=str(R/f'screenshots/mina-{width}.png'),full_page=True)
 if os.environ.get('AXE_PATH'):
  page.add_script_tag(content=Path(os.environ['AXE_PATH']).read_text());v=page.evaluate("async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}})).violations");assert not v,json.dumps(v,ensure_ascii=False)
 nojs=browser.new_context(java_script_enabled=False);nojs.route('**/*',serve);q=nojs.new_page();q.goto(O+'/mina.html');assert not q.locator('.construction-controls').is_visible();assert q.locator('.progression-cards figure').count()==3;assert q.locator('.morph-svg').is_visible()
 normal=browser.new_context(viewport={'width':1280,'height':900});normal.route('**/*',serve);a=normal.new_page();a.goto(O+'/mina.html');progress=a.locator('#morph-progress');expect(progress).to_have_value('0');a.wait_for_timeout(150);expect(progress).to_have_value('0')
 a.locator('#morph-play').click();a.wait_for_timeout(300);v=int(progress.input_value());assert 0<v<100
 a.locator('#morph-play').click();v=progress.input_value();a.wait_for_timeout(200);expect(progress).to_have_value(v)
 progress.focus();progress.press('ArrowRight');assert int(progress.input_value())==int(v)+1
 a.locator('#morph-reset').click();a.locator('#morph-play').click();a.locator('footer').scroll_into_view_if_needed();a.wait_for_timeout(120);v=progress.input_value();a.wait_for_timeout(250);expect(progress).to_have_value(v)
 a.locator('.construction').scroll_into_view_if_needed();expect(progress).to_have_value('100',timeout=6000);expect(a.locator('#morph-play')).to_have_attribute('aria-pressed','false')
 data=json.loads((R/'assets/mina-study/geometric-data.json').read_text());assert a.locator('#morph-shape').get_attribute('d')==data['paths'][2]
 a.locator('#morph-play').click();a.wait_for_timeout(100);a.evaluate("dispatchEvent(new PageTransitionEvent('pagehide'))");v=progress.input_value();a.wait_for_timeout(150);expect(progress).to_have_value(v)
 assert not errors,errors;browser.close()
print('PASS: MINA left-to-right morph / play, pause, reset, offscreen and navigation interruption / three stages, keyboard, pressed state, seven widths, 44px targets, reduced motion, no-JS and axe')
