// Display common material once, while leaving each complete child snapshot untouched.
export function childMaterials(child,parent){
 let passage=child.passage||'',common=parent.passage||'';
 if(passage&&common.includes(passage))passage='';
 else if(common&&passage.startsWith(common))passage=passage.slice(common.length).trim();
 const extra=(key)=>(child[key]||[]).filter(value=>!(parent[key]||[]).some(shared=>JSON.stringify(shared)===JSON.stringify(value)));
 const sharedFigureNotes=[];
 const questionFigures=(child.questionFigures||[]).filter(figure=>{
  const equivalent=(parent.groupMetadata?.commonFigureEquivalentSources||[]).find(row=>row.src===figure.src);
  const shared=(parent.questionFigures||[]).find(row=>row.src===figure.src||row.src===equivalent?.commonSrc);
  if(!shared)return true;
  if(figure.caption&&figure.caption!==shared.caption)sharedFigureNotes.push(figure.caption);
  return false;
 });
 return {...child,passage,tables:extra('tables'),questionFigures,sharedFigureNotes};
}
