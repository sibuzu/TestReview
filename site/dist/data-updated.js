// Dataset publication time, independent of the viewer's device timezone.
export function formatDataUpdatedAt(value){
 if(typeof value!=='string'||!/(Z|[+-]\d{2}:\d{2})$/i.test(value))return '';
 const date=new Date(value);if(!Number.isFinite(date.getTime()))return '';
 const parts=new Intl.DateTimeFormat('en-GB',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(date);
 const part=type=>parts.find(p=>p.type===type).value;
 return `${part('year')}/${part('month')}/${part('day')} ${part('hour')}:${part('minute')}:${part('second')}`;
}
