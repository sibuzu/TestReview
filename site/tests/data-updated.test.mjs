import test from 'node:test';
import assert from 'node:assert/strict';
import {formatDataUpdatedAt} from '../dist/data-updated.js';

test('dataset timestamp displays in Taiwan time with seconds',()=>{
 assert.equal(formatDataUpdatedAt('2026-10-29T01:19:14Z'),'2026/10/29 09:19:14');
 assert.equal(formatDataUpdatedAt('2026-10-29T09:19:14+08:00'),'2026/10/29 09:19:14');
});
test('Taiwan midnight uses the correct day and 00 hour',()=>{
 assert.equal(formatDataUpdatedAt('2026-10-28T16:00:00Z'),'2026/10/29 00:00:00');
});
test('absent or invalid publication time does not invent a current timestamp',()=>{
 for(const value of [undefined,null,'','invalid','2026-10-29 09:19:14'])assert.equal(formatDataUpdatedAt(value),'');
});
