import {escapeHTML as e,sanitizeComicDiagram} from './core.js';

export function renderComicDiagram(value) {
 const d=sanitizeComicDiagram(value);if(!d)return '';
 const text=(s,tag='span',cls='')=>`<${tag} class="comic-text ${cls}">${e(s)}</${tag}>`;
 const node=i=>`<div class="diagram-node tone-${i.tone}">${text(i.label,'strong')}${i.detail?text(i.detail,'span','diagram-detail'):''}</div>`;
 let content='';
 if(d.kind==='nested')content=`<div class="diagram-set tone-${d.items[0].tone}">${text(d.items[0].label,'strong')}<div class="diagram-set tone-${d.items[1].tone}">${text(d.items[1].label,'strong')}</div></div>`;
 if(d.kind==='flow')content=d.items.map((i,n)=>(n?text('↓ '+(d.arrow||'下一步'),'p','diagram-arrow'):'')+node(i)).join('');
 if(d.kind==='paths')content=`<div class="diagram-inputs">${d.items.map(node).join('')}</div>${text('↓ '+(d.arrow||'送交'),'p','diagram-arrow')}${node({label:d.target,tone:'blue'})}`;
 if(d.kind==='bars'){
  const max=Math.max(...d.items.map(i=>i.value));
  content=d.items.map(i=>`<div class="diagram-bar-row">${text(i.label+'：'+i.value+' 件','strong')}<div class="diagram-track"><div class="diagram-fill tone-${i.tone}" style="width:${100*i.value/max}%"></div></div></div>`).join('');
 }
 if(d.kind==='sum'){
  const total=d.items.reduce((a,i)=>a+i.value,0);
  content=`<div class="diagram-sum-segments">${d.items.map(i=>`<div class="diagram-summand tone-${i.tone}" style="flex:${i.value}">${text(i.shortLabel||i.label,'strong')}${text(i.value+' 件','span')}</div>`).join('')}</div><div class="diagram-legend">${d.items.map(i=>node({...i,detail:i.value+' 件'})).join('')}</div>${text(d.items.map(i=>i.value).join(' ＋ ')+' ＝ '+total+' 件','p','diagram-equation')}`;
 }
 if(d.kind==='change')content=d.items.map(i=>`<div class="diagram-change tone-${i.tone}">${text(i.label,'strong')}<div class="diagram-change-lines">${text('原本位置（虛線）','span','diagram-before')}${text('↓ 件數減少，線段下移','p','diagram-arrow')}${text('減少後位置（實線）','span','diagram-after')}</div></div>`).join('');
 return `<section class="comic-diagram diagram-${d.kind}" aria-label="${e(d.title)}">${text(d.title,'p','diagram-title')}${content}${d.note?text(d.note,'p','diagram-note'):''}</section>`;
}
