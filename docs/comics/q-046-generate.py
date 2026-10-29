from pathlib import Path
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#45675b"/></marker></defs>']
def arrow(x1,y1,x2,y2):s.append(f'<path d="M{x1} {y1}L{x2} {y2}" stroke="#45675b" stroke-width="5" marker-end="url(#arrow)"/>')
# First: longitudinal schematic of a leg vein with open one-way leaflets pointing towards heart.
s.append('<g><rect width="360" height="360" fill="#f6faf4"/><path d="M115 40V320H245V40Z" fill="#e1f0f9"/><path d="M115 40V320M245 40V320" fill="none" stroke="#4f88a8" stroke-width="8"/>')
s.append('<path d="M115 225Q144 214 159 170Q167 201 164 237Q133 237 115 225M245 225Q216 214 201 170Q193 201 196 237Q227 237 245 225" fill="#b3d0de" stroke="#4f88a8" stroke-width="3"/>')
arrow(180,290,180,102);s.append('</g>')
# Second: a functional sequence, NOT anatomical spatial positioning or simultaneous valve-state depiction.
s.append('<g transform="translate(360,0)"><rect width="360" height="360" fill="#fbf7ef"/>')
for x,y,w,h,col in [(103,22,154,72,'#e8e5f2'),(80,141,200,95,'#e1e9dc'),(125,283,110,54,'#f1ddd8')]:
 s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{col}" stroke="#687b69" stroke-width="4"/>')
for y in [99,242]:
 s.append(f'<path d="M155 {y}L171 {y+24}M205 {y}L189 {y+24}" fill="none" stroke="#8a6d46" stroke-width="5" stroke-linecap="round"/>')
arrow(180,44,180,135);arrow(180,171,180,279);s.append('</g>')
# Third: hand artery segment has a thick wall and a patent lumen, without a venous valve.
s.append('<g transform="translate(720,0)"><rect width="360" height="360" fill="#fff9f2"/><path d="M108 40V320H252V40Z" fill="#f1d1ca"/><path d="M138 40V320H222V40Z" fill="#fff4ee"/><path d="M108 40V320M252 40V320" stroke="#b36d61" stroke-width="8"/>')
arrow(180,285,180,83);s.append('</g></svg>')
Path('docs/comics/art/q-046.svg').write_text(''.join(s))
