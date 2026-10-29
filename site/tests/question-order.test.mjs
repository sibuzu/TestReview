import test from 'node:test';
import assert from 'node:assert/strict';
import {QuestionOrder} from '../dist/question-order.js';

const questions=[
  {id:'q-002',date:'2026-10-20'},
  {id:'q-003',date:'2026-10-21'},
  {id:'q-001',date:'2026-10-20'},
  {id:'q-004',date:'2026-10-19'},
];
const ids=qs=>qs.map(q=>q.id);
test('date uses newest first with stable ID ties, without mutating input',()=>{
  const order=new QuestionOrder(),before=structuredClone(questions);
  assert.deepEqual(ids(order.order(questions)),['q-003','q-001','q-002','q-004']);
  assert.deepEqual(questions,before);
  order.shuffle(questions,()=>0);order.byDate();
  assert.deepEqual(ids(order.order(questions)),['q-003','q-001','q-002','q-004']);
});
test('Fisher–Yates preserves every question and the same relative order through filters and rerenders',()=>{
  const order=new QuestionOrder();let calls=0;
  order.shuffle(questions,()=>{calls++;return 0;});
  const expected=['q-003','q-001','q-004','q-002'];
  assert.deepEqual(ids(order.order(questions)),expected);
  assert.deepEqual(ids(order.order(questions)),expected);
  assert.deepEqual(ids(order.order(questions.filter(q=>['q-002','q-001'].includes(q.id)))),['q-001','q-002']);
  assert.equal(calls,questions.length-1,'no new random draws during rendering');
  order.shuffle(questions,()=>.9999);
  assert.deepEqual(ids(order.order(questions)),ids(questions),'another click performs a fresh shuffle');
});
test('back navigation restores an independent shuffle snapshot and new questions remain visible',()=>{
  const order=new QuestionOrder();order.shuffle(questions,()=>0);
  const saved=order.snapshot(),expected=ids(order.order(questions));
  order.byDate();order.restore(saved);saved.ids.reverse();
  assert.deepEqual(ids(order.order(questions)),expected);
  const restored=new QuestionOrder();restored.restore(order.snapshot());
  assert.deepEqual(ids(restored.order([...questions,{id:'q-new',date:'2026-10-22'}])),[...expected,'q-new']);
  restored.restore({mode:'bad',ids:[]});assert.equal(restored.mode,'shuffle');
});
