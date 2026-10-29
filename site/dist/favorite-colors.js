export const FAVORITE_COLOR_KEY='test-review:favorite-colors:v1';
export const DEFAULT_FAVORITE_COLOR='yellow';
export const FAVORITE_COLORS=Object.freeze({
 red:{label:'紅',hex:'#ef0808'},blue:{label:'藍',hex:'#2166c4'},
 orange:{label:'橘',hex:'#ff8000'},green:{label:'青',hex:'#50df00'},
 yellow:{label:'黃',hex:'#ffe900'},
});
export const FAVORITE_COLOR_IDS=Object.keys(FAVORITE_COLORS);
export function checkedFavoriteColors(value){
 if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).length>10000)throw Error('收藏顏色格式不正確。');
 const entries=Object.entries(value);
 if(entries.some(([id,color])=>!/^q-\d{3,6}$/.test(id)||!FAVORITE_COLOR_IDS.includes(color)))throw Error('收藏顏色格式不正確。');
 return Object.fromEntries(entries.sort(([a],[b])=>a.localeCompare(b)));
}
export function loadFavoriteColors(storage){const raw=storage.getItem(FAVORITE_COLOR_KEY);return raw===null?{}:checkedFavoriteColors(JSON.parse(raw));}
