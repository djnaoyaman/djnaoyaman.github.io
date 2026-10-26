"""Render the site's vector/HTML source to deterministic browser assets.
Requires Python Playwright, Pillow, /usr/bin/chromium and Noto Sans CJK JP.
No external network requests, font downloads or image-generation dependencies.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(device_scale_factor=1)
 svg=(ROOT/'assets-source/mark.svg').read_text()
 for name,size in [('apple-touch-icon.png',180),('icon-192.png',192),('icon-512.png',512),('icon-maskable-192.png',192),('icon-maskable-512.png',512),('favicon-16.png',16),('favicon-32.png',32),('favicon-48.png',48)]:
  page.set_viewport_size({'width':size,'height':size})
  page.set_content('<style>html,body{margin:0;width:100%;height:100%;background:white}svg{width:100%;height:100%;display:block}</style>'+svg)
  page.screenshot(path=str(ROOT/name))
  # Encoding only; all creative content is the declarative SVG above.
  with Image.open(ROOT/name) as im:im.convert('RGB').save(ROOT/name,optimize=True)
 with Image.open(ROOT/'icon-512.png') as im:im.save(ROOT/'favicon.ico',sizes=[(16,16),(32,32),(48,48),(64,64)])
 page.set_viewport_size({'width':1200,'height':630})
 page.set_content((ROOT/'assets-source/share-card.html').read_text())
 page.evaluate('document.fonts.ready')
 page.screenshot(path=str(ROOT/'og-image.png'))
 with Image.open(ROOT/'og-image.png') as im:im.convert('RGB').save(ROOT/'og-image.png',optimize=True)
 browser.close()
print('Rendered 8 PNG icons, 4-size ICO and 1200×630 share card.')
