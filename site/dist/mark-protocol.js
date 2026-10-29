export const MARK_KINDS = ['favorite', 'doubt', 'answered'];
export const MARK_FIELDS = {favorite:'favorites', doubt:'doubts', answered:'answered'};
export const CLOUD_MARKS_URL = 'https://weirugo.sibuzu.com/.netlify/functions/marks';
export const COMPANION_ORIGINS = [
  'https://monitor.sibuzu.com',
  ...['127.0.0.1', 'localhost'].flatMap(host => [4173, 5500, 8765].map(port => `http://${host}:${port}`)),
];
export function marksEndpointFor(href) {
  try {if (COMPANION_ORIGINS.includes(new URL(href).origin)) return CLOUD_MARKS_URL;} catch {}
  return '/.netlify/functions/marks';
}
export function allowedMarksOrigin(origin, requestURL) {
  return !origin || origin === new URL(requestURL).origin || COMPANION_ORIGINS.includes(origin);
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
