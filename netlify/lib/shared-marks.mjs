import {createHash} from 'node:crypto';
import {checkedOperations, markKey, allowedMarksOrigin, MARK_KINDS} from '../../site/dist/mark-protocol.js';

const json = (data, status = 200, extra = {}) => new Response(JSON.stringify(data), {
  status, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff', ...extra},
});

export async function handleMarks(request, store) {
  const origin = request.headers.get('Origin');
  if (!allowedMarksOrigin(origin, request.url)) return json({error: '請從本網站或進度監看頁更新標記。'}, 403);
  const response = request.method === 'OPTIONS'
    ? new Response(null, {status: 204, headers: {'Cache-Control': 'no-store'}})
    : await handleRequest(request, store);
  if (origin) {
    response.headers.set('Access-Control-Allow-Origin', origin);
    response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    response.headers.set('Access-Control-Allow-Headers', 'Content-Type, If-None-Match');
    response.headers.set('Access-Control-Expose-Headers', 'ETag');
    response.headers.set('Vary', 'Origin');
  }
  return response;
}

async function handleRequest(request, store) {
  if (request.method === 'GET') {
    const {blobs} = await store.list({prefix: 'v1/'});
    const keys = blobs.map(b => b.key).filter(k => /^v1\/(favorite|doubt|answered)\/q-\d{3,6}$/.test(k));
    const marks = [];
    // Limit parallel requests; each flag is independent, so two devices changing
    // different questions or different flags cannot overwrite each other's data.
    for (let start = 0; start < keys.length; start += 20) {
      const rows = await Promise.all(keys.slice(start, start+20).map(async key => {
        const value = await store.get(key, {type: 'json', consistency: 'strong'});
        if (!value || typeof value.on !== 'boolean') return null;
        const [,kind,id] = key.split('/');
        return {kind, id, on: value.on};
      }));
      marks.push(...rows.filter(Boolean));
    }
    marks.sort((a,b) => markKey(a).localeCompare(markKey(b)));
    const payload = {schemaVersion: 1, kinds: MARK_KINDS, marks};
    const etag = '"'+createHash('sha256').update(JSON.stringify(payload)).digest('hex')+'"';
    if (request.headers.get('If-None-Match') === etag) return new Response(null, {status: 304, headers: {'ETag': etag, 'Cache-Control': 'no-store'}});
    return json(payload, 200, {'ETag': etag});
  }
  if (request.method !== 'POST') return json({error: '只接受GET或POST。'}, 405, {'Allow': 'GET, POST'});
  if (!request.headers.get('Content-Type')?.startsWith('application/json')) return json({error: '請使用JSON格式。'}, 415);
  let operations;
  try {
    const text = await request.text();
    if (text.length > 16384) return json({error: '單次標記資料過大。'}, 413);
    const body = JSON.parse(text);
    if (body.schemaVersion !== 1) throw Error('版本不相容。');
    operations = checkedOperations(body.operations, 100);
    if (!operations.length) throw Error('沒有標記變更。');
  } catch { return json({error: '標記資料格式不正確。'}, 400); }
  const unique = [...new Map(operations.map(op => [markKey(op), op])).values()];
  for (const op of unique) {
    // Keep OFF records as tombstones. An old browser's first sync must not
    // resurrect a mark that another device has already removed.
    await store.setJSON('v1/'+markKey(op), {on: op.on});
  }
  return json({schemaVersion: 1, applied: unique});
}
