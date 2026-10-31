"""Approved MINA crown. One polygonal master, optically sized exports."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];PAPER='#f7f6f2';INK='#282823'
MASTER=json.loads((ROOT/'assets/mina-study/crown-master.json').read_text())
def svg(tab=False,adaptive=False,pinned=False,inverse=False,maskable=False):
 ink,paper=(PAPER,INK) if inverse else (INK,PAPER)
 scale=.82 if maskable else 1.17 if tab else 1
 style=f'<style>.paper{{fill:{paper}}}.ink{{fill:{ink}}}@media(prefers-color-scheme:dark){{.paper{{fill:{ink}}}.ink{{fill:{paper}}}}}</style>' if adaptive else ''
 bg='' if pinned else f'<rect class="paper" width="200" height="200" fill="{paper}"/>'
 return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">{style}{bg}<g transform="translate(100 100) scale({scale}) translate(-100 -95)"><path class="ink" d="{MASTER["path"]}" fill="{ink}" fill-rule="evenodd"/></g></svg>'
if __name__=='__main__':
 for name,content in [('assets-source/mark.svg',svg()),('assets-source/tab-mark.svg',svg(tab=True)),('favicon.svg',svg(tab=True,adaptive=True)),('safari-pinned-tab.svg',svg(tab=True,pinned=True)),('assets-source/mark-inverse.svg',svg(inverse=True))]:(ROOT/name).write_text(content+'\n')
