import {favoriteIDs,FAVORITES_KEY} from './favorites.js';
import {FAVORITE_COLOR_KEY,checkedFavoriteColors} from './favorite-colors.js';
export const DOUBTS_KEY='test-review:doubts:v1';
export const ANSWERED_KEY='test-review:answered:v1';
export function loadDoubts(storage){const raw=storage.getItem(DOUBTS_KEY);return raw===null?[]:favoriteIDs(JSON.parse(raw));}
export function loadAnswered(storage){const raw=storage.getItem(ANSWERED_KEY);return raw===null?[]:favoriteIDs(JSON.parse(raw));}
export function exportMarks(favorites,doubts){return {schemaVersion:1,type:'question-marks',favorites:favoriteIDs([...favorites]),doubts:favoriteIDs([...doubts])};}
export function parseMarks(payload){
 if(payload?.schemaVersion===1&&payload.type==='question-marks')return {favorites:favoriteIDs(payload.favorites),doubts:favoriteIDs(payload.doubts)};
 return {favorites:favoriteIDs(payload),doubts:null};
}
export function persistMarks(storage,favorites,doubts,answered,favoriteColors){
 const checked=exportMarks(favorites,doubts),keys=[FAVORITES_KEY,DOUBTS_KEY],values=[checked.favorites,checked.doubts];
 if(answered!==undefined){checked.answered=favoriteIDs([...answered]);keys.push(ANSWERED_KEY);values.push(checked.answered);}
 if(favoriteColors!==undefined){checked.favoriteColors=checkedFavoriteColors(favoriteColors);keys.push(FAVORITE_COLOR_KEY);values.push(checked.favoriteColors);}
 const previous=keys.map(key=>storage.getItem(key));
 try{for(const [i,key] of keys.entries())storage.setItem(key,JSON.stringify(values[i]));}
 catch(error){for(const [i,key] of keys.entries()){try{if(previous[i]===null)storage.removeItem(key);else storage.setItem(key,previous[i]);}catch{}}throw error;}
 return checked;
}
