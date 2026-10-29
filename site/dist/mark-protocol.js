export const MARK_KINDS = ['favorite', 'doubt', 'answered'];
export const MARK_FIELDS = {favorite:'favorites', doubt:'doubts', answered:'answered'};
export const CLOUD_MARKS_URL = 'https://weirugo.sibuzu.com/.netlify/functions/marks';
export const CLOUD_MARKS_ORIGIN = 'https://weirugo.sibuzu.com';
export function isCloudMarksSite(href){
  try{return new URL(href).origin===CLOUD_MARKS_ORIGIN;}catch{return false;}
}
export function isLocalOnlySite(href){
  return !isCloudMarksSite(href);
}
export function marksEndpointFor(href) {
  return isCloudMarksSite(href)?'/.netlify/functions/marks':null;
}
export function allowedMarksOrigin(origin, requestURL) {
  return isCloudMarksSite(requestURL)&&(!origin||origin===CLOUD_MARKS_ORIGIN);
}
export const markKey = operation => `${operation.kind}/${operation.id}`;
export function checkedOperations(value, limit = 10000) {
  if (!Array.isArray(value) || value.length > limit) throw Error('標記資料格式不正確。');
  return value.map(item => {
    if (!item || !MARK_KINDS.includes(item.kind) || !/^q-\d{3,6}$/.test(item.id) || typeof item.on !== 'boolean') throw Error('標記資料格式不正確。');
    return {kind: item.kind, id: item.id, on: item.on};
  });
}
export function checkedSnapshot(value) {
  if (value?.schemaVersion !== 1) throw Error('雲端標記版本不相容。');
  return checkedOperations(value.marks);
}
