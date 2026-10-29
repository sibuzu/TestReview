import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {validateQuestion,mergeData} from '../dist/core.js';
import {childMaterials} from '../dist/group-materials.js';
const bank=JSON.parse(readFileSync(new URL('../dist/data.json',import.meta.url),'utf8'));
function fixture(){
 const atomic=bank.questions.flatMap(q=>q.groupQuestions?.length?q.groupQuestions:[q]);
 const children=['q-029','q-031'].map(id=>structuredClone(atomic.find(q=>q.id===id)));
 return {...structuredClone(children[0]),groupQuestions:children};
}
test('group import retains all child questions, options, answers, original art and source provenance',()=>{
 const input=fixture(),out=validateQuestion(input);
 assert.equal(out.groupQuestions.length,2);
 for(let i=0;i<2;i++){
  const before=input.groupQuestions[i],after=out.groupQuestions[i];
  for(const key of ['id','sourceId','subject','date','question','answer','explanation','studentAnswer','correctOption','passage','images','questionFigures','teachingComic'])assert.deepEqual(after[key],before[key],key);
 }
 const merged=mergeData({schemaVersion:1,questions:[],sources:bank.sources},{schemaVersion:1,questions:[input],sources:bank.sources});
 assert.equal(merged.data.questions[0].groupQuestions.length,2);
});
test('group validation rejects duplicate, missing retained ID and nested members',()=>{
 let group=fixture();group.groupQuestions[1]=group.groupQuestions[0];assert.throws(()=>validateQuestion(group));
 group=fixture();group.id='q-999';assert.throws(()=>validateQuestion(group));
 group=fixture();group.groupQuestions[0].groupQuestions=[];assert.throws(()=>validateQuestion(group));
});
test('display removes only identical common material, retaining child additions and every snapshot',()=>{
 const table={headers:['x'],rows:[['1']]},figure={src:'assets/test.svg',alt:'共同圖'};
 const parent={passage:'共同材料。',tables:[table],questionFigures:[figure]};
 const child={passage:'共同材料。\n本題另加條件。',tables:[table,{headers:['y'],rows:[['2']]}],questionFigures:[figure,{...figure,caption:'子題特定標記'}]};
 const saved=structuredClone(child),display=childMaterials(child,parent);
 assert.equal(display.passage,'本題另加條件。');assert.equal(display.tables.length,1);assert.equal(display.questionFigures.length,0);assert.deepEqual(display.sharedFigureNotes,['子題特定標記']);assert.deepEqual(child,saved);
});
