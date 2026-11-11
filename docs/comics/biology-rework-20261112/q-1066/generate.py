"""Four independent vector illustrations of a known monetary shortfall, no invented total."""
from pathlib import Path
R=Path(__file__).resolve().parents[4]
OUT=R/'docs/comics/art'
HEAD='''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="640" viewBox="0 0 640 640" role="img">
<defs>
 <linearGradient id="paper" x2="0.7" y2="1"><stop stop-color="#fffaf0"/><stop offset="1" stop-color="#e9dfcb"/></linearGradient>
 <linearGradient id="gold" x2="0.8" y2="1"><stop stop-color="#ffe8a2"/><stop offset=".45" stop-color="#dfb250"/><stop offset="1" stop-color="#a76d27"/></linearGradient>
 <linearGradient id="box" x2="1" y2="1"><stop stop-color="#e89c82"/><stop offset="1" stop-color="#a64d43"/></linearGradient>
 <linearGradient id="wallet" x2="0.4" y2="1"><stop stop-color="#9e6443"/><stop offset="1" stop-color="#4d302b"/></linearGradient>
 <linearGradient id="teal" x2="1" y2="1"><stop stop-color="#72b6b1"/><stop offset="1" stop-color="#26716d"/></linearGradient>
 <filter id="shadow" x="-30%" y="-30%" width="170%" height="180%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#40382e" flood-opacity=".16"/></filter>
</defs><rect width="640" height="640" rx="32" fill="url(#paper)"/>
'''
def gift(x,y,s=1):
 return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#shadow)">
 <path d="M0 52H170V181H0Z" fill="url(#box)" stroke="#8d4d40" stroke-width="3"/>
 <path d="M170 52L194 34V163L170 181Z" fill="#a55749" stroke="#8d4d40" stroke-width="3"/>
 <path d="M0 52L24 34H194L170 52Z" fill="#f1baa1" stroke="#8d4d40" stroke-width="3"/>
 <path d="M68 52H96V181H68Z" fill="#f9e6a9"/><path d="M68 52L92 34H120L96 52Z" fill="#fff0c1"/>
 <path d="M83 40C31 31 35-8 63 4C80 10 87 31 83 40Z" fill="#f1cf79" stroke="#ab7d3b" stroke-width="3"/>
 <path d="M83 40C132 28 141-9 111 2C95 8 87 24 83 40Z" fill="#f8dfa0" stroke="#ab7d3b" stroke-width="3"/>
 <path d="M83 39L61 78L82 68L98 84L91 40Z" fill="#f1cf79" stroke="#ab7d3b" stroke-width="2"/>
 </g>'''
def wallet(x,y,s=1,empty=False):
 return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#shadow)">
 <path d="M0 15Q0 0 20 0H184Q198 0 198 16V117Q198 134 181 134H17Q0 134 0 117Z" fill="url(#wallet)" stroke="#4b3029" stroke-width="4"/>
 <path d="M14 17H180V116H14Z" fill="none" stroke="#d9ad7d" stroke-width="2" stroke-dasharray="5 5" opacity=".7"/>
 <path d="M142 48H208V91H142Q125 91 125 70Q125 48 142 48Z" fill="#8c573c" stroke="#4b3029" stroke-width="3"/>
 <circle cx="151" cy="70" r="7" fill="url(#gold)"/>
 </g>'''
def coin(x,y,r=26,ghost=False):
 if ghost:return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="#b2793a" stroke-width="3" stroke-dasharray="7 6"/>'
 return f'<g filter="url(#shadow)"><ellipse cx="{x}" cy="{y+4}" rx="{r}" ry="{r*.87}" fill="#a67531"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)" stroke="#b38335" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{r-6}" fill="none" stroke="#fff0b9" stroke-width="2" opacity=".8"/></g>'
def arrow(x1,y1,x2,y2,color='#467f7a',dash=False):
 return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="6" {"stroke-dasharray=\"10 9\"" if dash else ""} fill="none"/><path d="M{x2-13} {y2-10}L{x2} {y2}L{x2-13} {y2+10}" fill="none" stroke="{color}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
# No figures or labels encoding an invented gift price or cash balance.
art=[]
art.append('<ellipse cx="324" cy="541" rx="251" ry="32" fill="#8c7859" opacity=".12"/>'
 +'<path d="M48 413L592 413L566 450H71Z" fill="#d5bc95"/><path d="M71 450H566V559H71Z" fill="#c19c74"/>'
 +gift(313,166,1.12)+wallet(83,395,.94)
 +'<path d="M97 378Q111 323 172 307" stroke="#7a9e96" stroke-width="5" fill="none" stroke-dasharray="10 10"/>'
 +coin(213,359,26,True)+coin(213,359,12,True))
# Common endpoints, dashed deficit, no lengths represent actual amounts or ratios.
art.append(gift(81,42,.6)+wallet(87,465,.59)
 +'<g filter="url(#shadow)"><rect x="78" y="217" width="484" height="68" rx="12" fill="url(#teal)"/><rect x="78" y="345" width="342" height="68" rx="12" fill="url(#gold)"/></g>'
 +'<rect x="427" y="345" width="135" height="68" rx="12" fill="none" stroke="#a46a36" stroke-width="4" stroke-dasharray="10 8"/>'
 +'<path d="M78 200V433M562 200V433" stroke="#79948c" stroke-width="2" stroke-dasharray="6 8"/>'
 +'<path d="M428 447V464H561V447" stroke="#a46a36" stroke-width="4" fill="none"/>'
 +coin(495,518,27,True))
# Open receiving palm: a request, no completed loan or invented received amount.
art.append('<ellipse cx="326" cy="537" rx="251" ry="36" fill="#8c7859" opacity=".12"/>'
 +wallet(69,121,.82)
 +'<path d="M94 450L196 395Q242 369 288 379L351 398Q369 406 359 424Q351 433 330 427L290 417L378 430Q400 434 425 422L503 381Q524 370 532 387Q538 401 518 417L421 479Q397 495 363 495H257L184 536Z" fill="#edc29e" stroke="#aa7b5f" stroke-width="4"/>'
 +'<path d="M92 448L187 526L149 570L56 494Z" fill="url(#teal)" stroke="#3c7972" stroke-width="3"/>'
 +'<path d="M284 403L331 417" stroke="#c99879" stroke-width="3" fill="none"/>'
 +coin(360,239,35,True)+coin(438,239,35,True)
 +'<path d="M398 294V344M383 329L398 346L413 329" stroke="#a46a36" stroke-width="5" stroke-dasharray="8 8" fill="none"/>')
art.append(wallet(58,119,.81)+gift(387,97,.83)
 +'<path d="M77 404H563" stroke="#d1c3a8" stroke-width="14" stroke-linecap="round"/>'
 +'<path d="M77 404H384" stroke="#4e8e87" stroke-width="14" stroke-linecap="round"/>'
 +'<path d="M392 404H563" stroke="#b88443" stroke-width="14" stroke-dasharray="12 12"/>'
 +'<path d="M77 380V428M563 380V428" stroke="#476f68" stroke-width="4"/>'
 +'<path d="M394 448V468H562V448" stroke="#a46a36" stroke-width="4" fill="none"/>'
 +coin(477,526,29,True)
 +'<path d="M258 212H346M331 198L346 212L331 226" stroke="#79948c" stroke-width="5" fill="none"/>')
if __name__=='__main__':
 for i,a in enumerate(art,1):
  p=OUT/f'q-1066-four-image-v2-panel-{i}.svg';p.write_text(HEAD+a+'</svg>\n');print(p.relative_to(R))
