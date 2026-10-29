// Compatibility entry for the raster/SVG preview scripts.
// Word-aware, measured paragraph wrapping. No character-by-character fallback.
function wrapComicText(text, maxWidth, measure, protectedWords=[]) {
 const segmenter=new Intl.Segmenter('zh-Hant',{granularity:'word'});
 const protectedTerms=text.match(/\b[A-Za-z0-9]{1,3}／(?:\([A-Za-z0-9＋－+\-]+\)|[A-Za-z0-9]{1,3})[²³]?(?![A-Za-z0-9])|\d+(?:\.\d+)?(?:cm|mm|km|mL|ml|kg|g|L|m)[²³]?(?![A-Za-z])|\([A-Za-z0-9＋－+\-]{1,12}\)[²³]?|[△∠][A-Z]{2,4}|[A-Z]{2,4}|\d+(?:[／：]\d+)+|[A-Za-z]+(?:['’][A-Za-z]+)+|\d+(?:\.\d+)?[%％]|[−－-]\d+(?:\.\d+)?(?:[／/]\d+)?(?:[A-Za-z][²³]?)?/g)||[];
 const protect=[...new Set(['喪偶式','理所當然','生育功能','工作','本來就是','缺席','責任','性別刻板印象','家庭照顧','責任承擔','邦加羅爾','德干高原','等高線','20公尺','譽滿杏林','師鐸獎','春風化雨','作育英才','繞梁三日','舌燦蓮花','里仁為美','居無定所','工作年齡','非工作年齡','扶養比','總排水體積','排水總體積','泄冶','曹羈','曹君','陳靈公',...protectedTerms,...protectedWords])].sort((a,b)=>b.length-a.length);
 const raw=[];let pos=0;
 // Retain actual text: protected vocabulary only changes permitted break positions.
 while(pos<text.length){const special=protect.find(w=>text.startsWith(w,pos));if(special){raw.push(special);pos+=special.length;continue;}let end=pos+1;while(end<text.length&&!protect.some(w=>text.startsWith(w,end)))end++;for(const s of segmenter.segment(text.slice(pos,end)))raw.push(s.segment);pos=end;}
 const tokens=[];let prefix='';
 for(const token of raw){if(/^[「『（【《〈“‘(]+$/u.test(token)){prefix+=token;continue;}if(/^[，。！？；：、,.!?;:」』）】》〉”’)]+$/u.test(token)&&tokens.length){tokens[tokens.length-1]+=token;continue;}tokens.push(prefix+token);prefix='';}
 if(prefix){if(tokens.length)tokens[tokens.length-1]+=prefix;else tokens.push(prefix);}
 const n=tokens.length,dp=Array(n+1).fill(Infinity),next=Array(n+1).fill(-1);dp[n]=0;
 for(let i=n-1;i>=0;i--){let candidate='';for(let j=i+1;j<=n;j++){candidate+=tokens[j-1];const line=candidate.trim(),width=measure(line);if(width>maxWidth-.5)break;if(!line||/^[，。！？；：、」』）】》〉]/u.test(line)||/[「『（【《〈]$/u.test(line))continue;
 const count=[...line.replace(/[\p{P}\p{Z}\s]/gu,'')].length;
 const short=(count<4&&i>0)?10000:0;const ragged=80*(1-width/maxWidth)**2;
 const boundary=(j<n&&!/[，。！？；：、,;:!?]$/u.test(line))?4:0;
 const score=1000+ragged+short+boundary+(j<n&&/[是的與把將讓和或]$/u.test(line)?180:0)+dp[j];if(score<dp[i]){dp[i]=score;next[i]=j;}
 }}
 if(next[0]<0&&n)throw new Error('A word or phrase exceeds available width; revise copy or layout.');
 const lines=[];for(let i=0;i<n;){const j=next[i];if(j<=i)throw new Error('Unable to wrap paragraph.');lines.push(tokens.slice(i,j).join('').trim());i=j;}
 return lines;
}
if(typeof module!=='undefined')module.exports={wrapComicText};
if(typeof globalThis!=='undefined')globalThis.wrapComicText=wrapComicText;
