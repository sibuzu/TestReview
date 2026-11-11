import {escapeHTML as e,safeAsset} from './core.js';
import {wrapComicText} from './comic-wrap.js';
import {renderComicDiagram} from './comic-diagram.js';

function renderPanelImage(src,alt,index) {
 const single=index===undefined;
 return `<div class="comic-art${single?' comic-art-single':''}"><img src="${e(src)}" alt="${e(alt)}"${single?'':` style="--panel:${index}"`} loading="lazy"></div>`;
}

export function renderTeachingComic(c) {
 if(!c || !safeAsset(c.art))return '';
 const words=Array.isArray(c.protectedWords)?c.protectedWords:[];
 const cells=c.panels.map((p,i)=>{
  const image=safeAsset(p.image),diagram=image?'':renderComicDiagram(p.diagram);
  const visual=image?renderPanelImage(image,p.alt):diagram||renderPanelImage(c.art,p.alt,i);
  return `<section class="comic-cell${diagram?' has-diagram':''}">${p.caption?`<p class="comic-caption comic-text">${e(p.caption)}</p>`:''}${visual}<div class="comic-copy"><h4 class="comic-text">${e(p.heading)}</h4><p class="comic-text">${e(p.text)}</p></div></section>`;
 });
 const recapImage=safeAsset(c.fourth.image);
 const recap=`<h4 class="comic-text">④ ${e(c.title)}</h4><p class="comic-answer comic-text">${e(c.fourth.answer)}</p><ul>${c.fourth.points.map(t=>`<li class="comic-text">${e(t)}</li>`).join('')}</ul>`;
 cells.push(`<section class="comic-cell comic-recap${recapImage?' has-image':''}">${recapImage?renderPanelImage(recapImage,c.fourth.alt)+`<div class="comic-recap-copy">${recap}</div>`:recap}</section>`);
 return `<section class="native-comic" aria-label="${e(c.title)}" data-protected-words="${e(JSON.stringify(words))}"><div class="comic-grid">${cells.join('')}</div></section>`;
}

let comicObserver;
export function layoutTeachingComics(root=document) {
 comicObserver?.disconnect();
 const comics=[...root.querySelectorAll('.native-comic')];
 if(!comics.length)return;
 const ctx=document.createElement('canvas').getContext('2d');
 const originals=new WeakMap();
 function layout(comic) {
  if(!comic.isConnected || !comic.getBoundingClientRect().width)return;
  let protectedWords=[];
  try {
   const words=JSON.parse(comic.dataset.protectedWords||'[]');
   if(Array.isArray(words))protectedWords=words.filter(w=>typeof w==='string'&&w.length>=2&&w.length<=40).slice(0,50);
  } catch { /* Invalid optional metadata must not prevent readable layout. */ }
  for(const el of comic.querySelectorAll('.comic-text')) {
   if(!originals.has(el))originals.set(el,el.textContent);
   const original=originals.get(el),style=getComputedStyle(el);
   ctx.font=`${style.fontWeight} ${style.fontSize} ${style.fontFamily}`;
   const width=el.getBoundingClientRect().width;
   try {
    const lines=wrapComicText(original.replace(/\n/g,''),width,t=>ctx.measureText(t).width,protectedWords);
    el.innerHTML=lines.map(line=>`<span class="comic-line">${e(line)}</span>`).join('');
    delete el.dataset.wrapError;
   } catch {
    // If an unavailable font makes a phrase wider than the column, preserve readable text.
    el.textContent=original;el.dataset.wrapError='true';
   }
  }
 }
 comicObserver=new ResizeObserver(entries=>entries.forEach(({target})=>layout(target)));
 comics.forEach(c=>comicObserver.observe(c));
 document.fonts.ready.then(()=>comics.forEach(layout));
}
