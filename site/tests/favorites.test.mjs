import test from 'node:test';
import assert from 'node:assert/strict';
import {favoriteIDs,legacyFavoriteIDs,loadFavorites,FAVORITES_KEY,LEGACY_KEY,PREVIOUS_FAVORITES_KEY} from '../dist/favorites.js';
const storage=entries=>{const map=new Map(entries);return {map,getItem:k=>map.get(k)??null,setItem:(k,v)=>map.set(k,v),removeItem:k=>map.delete(k)};};
test('favorites contain unique question IDs only',()=>{
 assert.deepEqual(favoriteIDs({schemaVersion:1,type:'favorites',favorites:['q-044','q-016','q-044']}),['q-016','q-044']);
 for(const bad of [{questions:[]},['../bad'],[{}],{schemaVersion:1,type:'favorites',favorites:'q-016'}])assert.throws(()=>favoriteIDs(bad));
});
test('legacy storage migrates favorites and removes question content, progress and notes',()=>{
 const old={revision:'old',questions:[{id:'q-016',starred:true,status:'mastered',notes:'private note',answer:'old answer'},{id:'q-044',starred:false}],sources:[{url:'old source'}]};
 const s=storage([[LEGACY_KEY,JSON.stringify(old)]]);assert.deepEqual(loadFavorites(s),['q-016']);
 assert.deepEqual([...s.map],[[FAVORITES_KEY,'["q-016"]']]);
 assert.deepEqual(legacyFavoriteIDs(old),['q-016']);
});
test('current favorite choices take precedence over old data',()=>{
 const s=storage([[FAVORITES_KEY,'["q-044"]'],[LEGACY_KEY,JSON.stringify({questions:[{id:'q-016',starred:true}]})]]);
 assert.deepEqual(loadFavorites(s),['q-044']);assert.equal(s.getItem(LEGACY_KEY),null);
});
test('a fresh browser starts without writing question data',()=>{const s=storage([]);assert.deepEqual(loadFavorites(s),[]);assert.equal(s.map.size,0);});

test('renamed project migrates existing favorites without storing question content',()=>{const s=storage([[PREVIOUS_FAVORITES_KEY,'["q-016","q-044"]']]);assert.deepEqual(loadFavorites(s),['q-016','q-044']);assert.deepEqual([...s.map],[[FAVORITES_KEY,'["q-016","q-044"]']]);});
test('renamed project keeps current choices over previous project favorites',()=>{const s=storage([[FAVORITES_KEY,'[]'],[PREVIOUS_FAVORITES_KEY,'["q-016"]']]);assert.deepEqual(loadFavorites(s),[]);assert.equal(s.getItem(PREVIOUS_FAVORITES_KEY),null);});
