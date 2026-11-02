import test from 'node:test';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {sanitizeComicDiagram,validateQuestion} from '../dist/core.js';
import {renderComicDiagram} from '../dist/comic-diagram.js';
import {renderTeachingComic} from '../dist/teaching-comic.js';

test('Chinese chart labels and exact source counts survive validation in both reading views',()=>{
 for(const id of ['q-891','q-893']){
  const c=JSON.parse(readFileSync(new URL('../../docs/comics/'+id+'.json',import.meta.url)));
  for(const p of c.panels){
   assert.deepEqual(sanitizeComicDiagram(p.diagram),p.diagram);
   const html=renderComicDiagram(p.diagram);
   const py=execFileSync('python',['-c','import sys,json;sys.path.insert(0,"site/scripts");from comic_diagram import render_diagram;print(render_diagram(json.loads(sys.stdin.read())))'],{cwd:new URL('../..',import.meta.url),input:JSON.stringify(p.diagram),encoding:'utf8'});
   const visible=s=>s.replace(/<[^>]*>/g,'');
   assert.equal(visible(py).trim(),visible(html).trim());
   for(const item of p.diagram.items)assert.ok(html.includes(item.label));
  }
 }
});

test('diagram labels and captions escape markup and reject unsafe geometry values',()=>{
 const d={kind:'bars',title:'圖表',items:[{label:'<img src=x onerror=alert(1)>',value:32,tone:'blue'}]};
 const html=renderComicDiagram(d);assert.ok(!html.includes('<img'));assert.ok(html.includes('&lt;img'));
 for(const value of [-1,Infinity,NaN,'32; background:url(https://evil.test)',1e10]){
  assert.equal(sanitizeComicDiagram({...d,items:[{...d.items[0],value}]}),undefined);
 }
 assert.equal(sanitizeComicDiagram({...d,kind:'<script>'}),undefined);
 const data=JSON.parse(readFileSync(new URL('../dist/data.json',import.meta.url)));
 const q=structuredClone(data.questions.find(q=>q.teachingComic));
 q.teachingComic.panels[0].caption='<script>alert(1)</script>';
 const comic=validateQuestion(q).teachingComic;
 assert.equal(comic.panels[0].caption,q.teachingComic.panels[0].caption);
 assert.ok(renderTeachingComic(comic).includes('&lt;script&gt;'));
});
