from pathlib import Path
# Fixed coordinates make the three counterexamples visually comparable.
pos={0:76,1:176,2:276}
blue,orange,gray='#3676bc','#d78c21','#7a8373'
a_b=[(2,1),(1,2),(1,1)]
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360">']
for i,(a,b) in enumerate(a_b):
 s.append(f'<g transform="translate({360*i},0)"><rect width="360" height="360" fill="#f6f8ed"/><rect x="16" y="48" width="328" height="264" rx="22" fill="white" stroke="#d2ddc5" stroke-width="3"/>')
 s.append('<path d="M34 208H324" stroke="#9ca795" stroke-width="4"/><path d="M324 208l-12 -7v14Z" fill="#9ca795"/>')
 for n in range(3):s.append(f'<path d="M{pos[n]} 200V216" stroke="#b7c3ad" stroke-width="3"/>')
 # c=0 always stays left; a,b both to its right.
 s.append(f'<path d="M{pos[0]} 208V158" stroke="{gray}" stroke-width="3"/><circle cx="{pos[0]}" cy="146" r="12" fill="{gray}"/>')
 if a!=b:
  for v,color in [(a,blue),(b,orange)]:s.append(f'<path d="M{pos[v]} 208V158" stroke="{color}" stroke-width="4"/><circle cx="{pos[v]}" cy="146" r="14" fill="{color}"/>')
 else:
  x=pos[a]
  s.append(f'<path d="M{x-3} 208V160" stroke="{blue}" stroke-width="5"/><path d="M{x+3} 208V160" stroke="{orange}" stroke-width="5"/>')
  # Two half-discs share exactly one coordinate rather than side-by-side values.
  s.append(f'<path d="M{x} 131a15 15 0 0 0 0 30Z" fill="{blue}"/><path d="M{x} 131a15 15 0 0 1 0 30Z" fill="{orange}"/>')
 s.append('</g>')
s.append('</svg>')
Path('docs/comics/art/q-330.svg').write_text(''.join(s))
