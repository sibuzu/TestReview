import {checkedOperations, checkedSnapshot, markKey, marksEndpointFor, MARK_FIELDS, MARK_KINDS} from './mark-protocol.js';
import {DEFAULT_FAVORITE_COLOR} from './favorite-colors.js';

export const OUTBOX_KEY = 'test-review:mark-outbox:v1';

export class MarkSync {
  constructor({storage, getLocal, apply, status, fetcher = globalThis.fetch.bind(globalThis), endpoint = marksEndpointFor(globalThis.location?.href)}) {
    Object.assign(this, {storage, getLocal, apply, status, fetcher, endpoint});
    this.localOnly=endpoint===null;
    if(this.localOnly)this.available=false;
    this.pending = new Map();
    this.sequence = 0;
    this.snapshot = [];
    this.etag = '';
    if(this.localOnly){try{storage.removeItem(OUTBOX_KEY);}catch{}return;}
    try { for (const op of checkedOperations(JSON.parse(storage.getItem(OUTBOX_KEY)||'[]'))) this.pending.set(markKey(op), {...op, seq: ++this.sequence}); } catch {}
  }
  persist() {
    try {
      if (this.pending.size) this.storage.setItem(OUTBOX_KEY, JSON.stringify([...this.pending.values()].map(({seq,...op}) => op)));
      else this.storage.removeItem(OUTBOX_KEY);
    } catch {} // The in-memory outbox still retries when storage is unavailable.
  }
  queue(kind, id, on, color) {
    this.queueAll([{kind,id,on,...(color!==undefined?{color}:{})}]);
  }
  queueAll(operations) {
    if(this.localOnly){this.status('local');return;}
    for (const op of checkedOperations(operations)) this.pending.set(markKey(op), {...op, seq: ++this.sequence});
    this.persist();
    this.status(this.available===false?'local':'pending');
    if (this.available!==false) void this.refresh();
  }
  importLocalUnknown() {
    const remote = new Map(this.snapshot.map(op => [markKey(op), op]));
    const local = this.getLocal();
    for (const [kind, field] of Object.entries(MARK_FIELDS)) {
      for (const id of local[field]||[]) {
        if (!/^q-\d{3,6}$/.test(id)) continue;
        const color=kind==='favorite'?local.favoriteColors?.[id]:undefined;
        const op = {kind,id,on:true,...(color?{color}:{})}, key = markKey(op);
        const previous=remote.get(key);
        const missingColor=this.serverFavoriteColors&&previous?.on&&!previous.color&&color&&color!==DEFAULT_FAVORITE_COLOR;
        if ((!remote.has(key)||missingColor) && !this.pending.has(key)) this.pending.set(key, {...op,seq:++this.sequence});
      }
    }
    this.persist();
  }
  publish(extra = []) {
    const current = new Map(this.snapshot.map(op => [markKey(op), op]));
    for (const op of [...extra, ...this.pending.values()]) current.set(markKey(op), op);
    const result=Object.fromEntries(Object.entries(MARK_FIELDS).map(([kind,field])=>
      [field,[...current.values()].filter(op=>op.kind===kind&&op.on).map(op=>op.id).sort()]));
    if(this.getLocal().favoriteColors!==undefined||[...current.values()].some(op=>op.color&&op.color!==DEFAULT_FAVORITE_COLOR))result.favoriteColors=Object.fromEntries(
      [...current.values()].filter(op=>op.kind==='favorite'&&op.on).map(op=>[op.id,op.color||DEFAULT_FAVORITE_COLOR]));
    this.apply(result);
  }
  refresh() {
    if(this.localOnly){this.available=false;this.status('local');return Promise.resolve();}
    if (this.busy) {this.again = true; return this.busy;}
    this.busy = this.run().finally(() => {
      this.busy = null;
      if (this.again) {this.again = false; void this.refresh();}
    });
    return this.busy;
  }
  async request(options = {}) {
    if(this.localOnly)throw Error('This site stores marks locally only.');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 15000);
    try { return await this.fetcher(this.endpoint, {...options,cache:'no-store',signal:controller.signal}); }
    finally {clearTimeout(timeout);}
  }
  async run() {
    if(this.localOnly){this.available=false;this.status('local');return;}
    this.status('syncing');
    try {
      const response = await this.request({headers:this.etag?{'If-None-Match':this.etag}:{}});
      if (response.status === 404) {this.available=false; this.status('local'); return;}
      this.available=true;
      if (response.status !== 304) {
        if (!response.ok) throw Error('Cloud unavailable');
        const payload = await response.json();
        this.snapshot = checkedSnapshot(payload);
        // Until the updated Functions are deployed, old servers support only
        // favorite/doubt. Keep answered changes local without blocking those.
        this.serverKinds = Array.isArray(payload.kinds)
          ? payload.kinds.filter(kind=>MARK_KINDS.includes(kind)) : ['favorite','doubt'];
        this.serverFavoriteColors=payload.favoriteColors===true;
        this.etag = response.headers.get('ETag')||'';
      }
      this.importLocalUnknown();
      this.publish();
      while (this.pending.size) {
        const batch = [...this.pending.values()].filter(op=>(this.serverKinds||['favorite','doubt']).includes(op.kind)&&(!op.color||this.serverFavoriteColors)).slice(0,100);
        if (!batch.length) break;
        const sent = batch.map(({seq,...op})=>op);
        const saved = await this.request({method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({schemaVersion:1,operations:sent})});
        if (!saved.ok) throw Error('Cloud write failed');
        const ack = await saved.json();
        const applied = checkedOperations(ack.applied,100);
        if (JSON.stringify(applied)!==JSON.stringify(sent)) throw Error('Cloud acknowledgement mismatch');
        for (const op of batch) if (this.pending.get(markKey(op))?.seq===op.seq) this.pending.delete(markKey(op));
        const merged = new Map(this.snapshot.map(op=>[markKey(op),op]));
        for (const op of sent) merged.set(markKey(op),op);
        this.snapshot = [...merged.values()];
        this.etag = '';
        this.persist();
        this.publish();
      }
      this.status(this.pending.size?'pending':'synced');
    } catch {this.status('pending');}
  }
}
