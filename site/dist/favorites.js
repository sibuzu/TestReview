export const FAVORITES_KEY='test-review:favorites:v1';
export const PREVIOUS_FAVORITES_KEY='mistake-review:favorites:v1';
export const LEGACY_KEY='mistake-review:v1';
const validId=id=>typeof id==='string'&&/^[\w-]{1,100}$/.test(id);
export function favoriteIDs(payload){
 const list=Array.isArray(payload)?payload:payload?.type==='favorites'&&payload.schemaVersion===1?payload.favorites:undefined;
 if(!Array.isArray(list)||list.length>10000||list.some(id=>!validId(id)))throw Error('請選擇有效的收藏備份 JSON。');
 return [...new Set(list)].sort();
}
export function legacyFavoriteIDs(payload){
 if(!Array.isArray(payload?.questions))throw Error('無法讀取舊版收藏。');
 return favoriteIDs(payload.questions.filter(q=>q.starred===true).map(q=>q.id));
}
export function loadFavorites(storage){
 const current=storage.getItem(FAVORITES_KEY),previous=storage.getItem(PREVIOUS_FAVORITES_KEY),legacy=storage.getItem(LEGACY_KEY);
 const ids=current!==null?favoriteIDs(JSON.parse(current)):previous!==null?favoriteIDs(JSON.parse(previous)):legacy!==null?legacyFavoriteIDs(JSON.parse(legacy)):[];
 if(previous!==null||legacy!==null){storage.setItem(FAVORITES_KEY,JSON.stringify(ids));storage.removeItem(PREVIOUS_FAVORITES_KEY);storage.removeItem(LEGACY_KEY);}
 return ids;
}
