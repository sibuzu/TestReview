import {getStore} from '@netlify/blobs';
import {handleAccountMarks} from '../lib/account-marks.mjs';
import {accountCORS} from '../../site/dist/account-policy.js';

export default async request => {
  try {
    return await handleAccountMarks(request, getStore({name: 'testreview-shared-marks', consistency: 'strong'}));
  } catch {
    return accountCORS(new Response(JSON.stringify({error: '雲端暫時無法儲存，標記會保留在本機待重試。'}), {
      status: 503, headers: {'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store'},
    }),request.headers.get('Origin'));
  }
};
