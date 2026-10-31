"""Draft 02: explicit Bézier contours, not a trace of generated pixels."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
# Four readable contributions share one silhouette. The I is a spine; the
# N is the foreground ribbon; the arch and crossbar suggest M/A as a ligature.
parts={
'arch': 'M246 154 C246 68 298 36 345 36 C430 36 490 166 490 306 C490 405 459 464 416 464 C386 464 357 438 325 399 L161 202 C139 176 123 164 108 164 C82 164 70 197 70 244 L70 326 C70 402 91 437 133 450 C62 458 34 417 34 348 L34 247 C34 176 60 138 99 138 C129 138 154 160 180 192 L348 393 C376 427 395 446 416 446 C447 446 462 391 462 306 C462 185 409 54 344 54 C300 54 258 89 258 164 Z',
'spine': 'M273 154 L345 154 L345 158 C326 160 325 170 325 190 L325 435 C325 455 326 466 345 468 L345 472 L273 472 L273 468 C292 466 293 455 293 435 L293 190 C293 170 292 160 273 158 Z',
'left': 'M132 210 L160 244 L160 376 C160 399 162 407 178 412 L178 416 L114 416 L114 412 C130 407 132 399 132 376 Z',
'crossbar': 'M424 222 L436 227 L371 382 L359 377 Z M380 349 L448 349 L448 362 L375 362 Z',
}
# A constant 8-unit knockout defines every over/under crossing.
def shape(layered=False,inverse=False,gap=8):
 ink='#f7f6f2' if inverse else '#282823';paper='#282823' if inverse else '#f7f6f2'
 under=''.join(f'<path class="mina-part mina-{k}" data-part="{k}" d="{parts[k]}" fill="{ink}"/>' for k in ['spine','left','crossbar'])
 # Knockout is applied only to underlying strokes, never to the foreground ribbon.
 return under+f'<path d="{parts["arch"]}" fill="{paper}" stroke="{paper}" stroke-width="{gap}" stroke-linejoin="round"/><path class="mina-part mina-arch" data-part="arch" d="{parts["arch"]}" fill="{ink}"/>'
for name,inverse in [('monogram-02.svg',False),('monogram-02-inverse.svg',True),('monogram-02-small.svg',False)]:
 (R/'assets/mina-study'/name).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 528 528" role="img" aria-labelledby="title"><title id="title">MINA — sculptural monogram, draft 02</title>'+'<g transform="translate(60 65) scale(.78)">'+shape(inverse=inverse,gap=24 if 'small' in name else 8)+'</g>'+'</svg>\n')
if __name__=='__main__':print('Built precise editable study contours; not adopted as live identity.')
