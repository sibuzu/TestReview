from pathlib import Path
# These are landform concepts, without invented altitude numbers or real-site geometry.
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#cdeaf7"/><stop offset="1" stop-color="#f7fbf0"/></linearGradient><linearGradient id="soil" x2="0" y2="1"><stop stop-color="#c3a47c"/><stop offset="1" stop-color="#8e7151"/></linearGradient></defs>']
for i,path in enumerate(['M20 286L86 282L118 144L242 144L274 282L340 286','M20 242Q90 235 158 241T280 240L340 242']):
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="url(#sky)"/><path d="M{40+i*20} 67q20 -23 42 0q25 -14 37 7H{40+i*20}Z" fill="white" opacity=".8"/>')
 s.append(f'<path d="{path}L340 340H20Z" fill="url(#soil)"/><path d="{path}" fill="none" stroke="#659353" stroke-width="12" stroke-linejoin="round"/><path d="M20 340H340" stroke="#71816a" stroke-width="2"/></g>')
s.append('<g transform="translate(720,0)"><rect width="360" height="360" fill="#f5f8ed"/>')
for i in range(5):
 x,y=27+i*8,70+i*8
 width,height=306-16*i,220-16*i
 s.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{50-i*5}" fill="{["#d5ddad","#d9e3b9","#dce8c2","#dfedca","#e4f1d3"][i]}" stroke="#887749" stroke-width="3"/>')
s.append('</g></svg>')
Path('docs/comics/art/q-664.svg').write_text(''.join(s))
