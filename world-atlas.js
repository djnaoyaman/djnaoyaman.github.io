'use strict';
(()=>{
// Wireframe geometry are fixed to the user-approved SVG; resize only changes hit areas.
const DATA={"nodes":[{"name":"gooooooooood expression","url":"/gooooooooood_expression/"},{"name":"Crate Diggin’","url":"/cratediggin/"},{"name":"Premium Cuts Listed","url":"/premiumcuts/"},{"name":"Earth Number","url":"/earthnumber/"},{"name":"my Chems","url":"/chems/"},{"name":"SUBURBIA CLASSICA","url":"/suburbia-classica/"},{"name":"鎌・くらんぽ","url":"/kuranpo/"},{"name":"一見坊の【日本妖怪学体系】","url":"/youkai/"},{"name":"花鳥風月、そして魚と虫。","url":"/sakanamushi/"},{"name":"酸冷交代浴","url":"/sanreikotaiyoku/"},{"name":"掌蹠膿疱症.com","url":"/ppp/"},{"name":"IL MASTRO","url":"/bookkeeping/"},{"name":"1minutes — ONE MINUTE FOREVER","url":"/1minutes/"},{"name":"OMOCHI TOUCH","url":"/omochi-touch/"}]};
const root=document.querySelector('.world-atlas');if(!root)return;
const stage=root.querySelector('.world-stage'),svg=root.querySelector('.world-map'),nodes=[...root.querySelectorAll('.world-node')],edges=[...root.querySelectorAll('.world-edge')],name=root.querySelector('#world-caption-name'),category=root.querySelector('#world-caption-category'),replay=root.querySelector('.world-replay');
const motion=matchMedia('(prefers-reduced-motion: reduce)');let inView=true;
// Invisible nearest-point cells prevent enlarged touch regions from covering a neighbour.
// The original visible SVG and every point position remain unchanged.
const NS='http://www.w3.org/2000/svg',defs=document.createElementNS(NS,'defs');svg.prepend(defs);
const points=nodes.map(node=>{const p=node.querySelector('.world-point');return [+p.getAttribute('cx'),+p.getAttribute('cy')];});
const cells=nodes.map((node,i)=>{const clip=document.createElementNS(NS,'clipPath'),polygon=document.createElementNS(NS,'polygon');clip.id='world-hit-cell-'+i;clip.setAttribute('clipPathUnits','userSpaceOnUse');clip.append(polygon);defs.append(clip);node.querySelector('.world-hit').setAttribute('clip-path','url(#'+clip.id+')');return polygon;});
const layout=()=>{const scale=svg.viewBox.baseVal.width/Math.max(svg.getBoundingClientRect().width,1),r=24*scale;
 nodes.forEach((node,i)=>{const [x,y]=points[i];let poly=[[x-r,y-r],[x+r,y-r],[x+r,y+r],[x-r,y+r]];
  points.forEach(([u,v],j)=>{if(i===j)return;const nx=u-x,ny=v-y,c=(u*u+v*v-x*x-y*y)/2,out=[];
   poly.forEach((a,k)=>{const b=poly[(k+1)%poly.length],da=a[0]*nx+a[1]*ny-c,db=b[0]*nx+b[1]*ny-c;
    if(da<=0)out.push(a);if((da<=0)!==(db<=0)){const t=da/(da-db);out.push([a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1])]);}});poly=out;});
  cells[i].setAttribute('points',poly.map(p=>p.join(',')).join(' '));node.querySelector('.world-hit').setAttribute('r',String(r));node.querySelector('.world-halo').setAttribute('r',String(14*scale));});root.dataset.layout=stage.clientWidth<620?'compact':'wide';};
const pause=()=>root.classList.toggle('is-paused',document.hidden||!inView);
const play=()=>{if(motion.matches){root.classList.remove('atlas-animate');root.dataset.phase='complete';replay.hidden=true;return;}root.classList.remove('atlas-animate');void svg.getBoundingClientRect();root.dataset.phase='building';root.classList.add('atlas-animate');replay.hidden=false;pause();};
nodes.forEach((node,i)=>{const select=()=>{root.dataset.active=String(i);name.textContent=DATA.nodes[i].name;category.textContent=String(i+1).padStart(2,'0')+' / WORLD';edges.forEach(edge=>edge.classList.toggle('is-connected',(edge.dataset.worlds||'').split(',').includes(String(i))));nodes.forEach(n=>n.classList.toggle('is-selected',n===node));};node.addEventListener('pointerenter',select);node.addEventListener('focus',select);node.addEventListener('pointerdown',select);});
root.querySelector('.world-signature').addEventListener('animationend',event=>{if(event.animationName==='worldResolve')root.dataset.phase='complete';});replay.addEventListener('click',play);document.addEventListener('visibilitychange',pause);window.addEventListener('pageshow',()=>{layout();pause();});if('ResizeObserver'in window)new ResizeObserver(layout).observe(stage);else window.addEventListener('resize',layout);if('IntersectionObserver'in window)new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;pause();},{threshold:.05}).observe(root);motion.addEventListener('change',()=>{root.classList.remove('atlas-animate');root.dataset.phase='complete';replay.hidden=motion.matches;});layout();play();
})();
