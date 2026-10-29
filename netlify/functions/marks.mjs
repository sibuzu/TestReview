import {getStore} from '@netlify/blobs';
import {handleMarks} from '../lib/shared-marks.mjs';
import {allowedMarksOrigin} from '../../site/dist/mark-protocol.js';

export default async request => {
  if(!allowedMarksOrigin(request.headers.get('Origin'),request.url))return new Response(JSON.stringify({error:'此入口的標記僅儲存在瀏覽器，不提供雲端標記存取。'}),{status:403,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','Vary':'Origin'}});
  try {
    return await handleMarks(request, getStore({name: 'testreview-shared-marks', consistency: 'strong'}));
  } catch {
    return new Response(JSON.stringify({error: '雲端暫時無法儲存，標記會保留在本機待重試。'}), {
      status: 503, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store'},
    });
  }
};
