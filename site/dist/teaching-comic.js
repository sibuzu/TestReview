import {escapeHTML as e,safeAsset} from './core.js';
import {wrapComicText} from './comic-wrap.js';

export function renderTeachingComic(c) {
 if(!c || !safeAsset(c.art))return '';
 const words=Array.isArray(c.protectedWords)?c.protectedWords:[];
 return `<section class="native-comic" aria-label="${e(c.title)}" data-protected-words="${e(JSON.stringify(words))}"><div class="comic-grid">${c.panels.map((p,i)=>`<section class="comic-cell"><div class="comic-art"><img src="${e(c.art)}" alt="${e(p.alt)}" style="--panel:${i}" loading="lazy"></div><div class="comic-copy"><h4 class="comic-text">${e(p.heading)}</h4><p class="comic-text">${e(p.text)}</p></div></section>`).join('')}<section class="comic-cell comic-recap"><h4 class="comic-text">④ ${e(c.title)}</h4><p class="comic-answer comic-text">${e(c.fourth.answer)}</p><ul>${c.fourth.points.map(t=>`<li class="comic-text">${e(t)}</li>`).join('')}</ul></section></div></section>`;
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
