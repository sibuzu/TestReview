from pathlib import Path
# Equal scales in all three square panels. Labels/inequalities remain native HTML.
W=360
xmin,xmax=-15,7
f=lambda x:42+(x-xmin)/(xmax-xmin)*276
m9,m4=f(-9),f(4)
parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><filter id="shadow"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-opacity=".12"/></filter></defs>']
for n,(end,color,filled) in enumerate([(m9,'#3872b9',False),(m4,'#c68420',True),(m9,'#35865b',False)]):
 parts.append(f'<g transform="translate({n*W},0)"><rect width="360" height="360" fill="#f6f8ed"/><rect x="16" y="48" width="328" height="264" rx="22" fill="white" stroke="#d2ddc5" stroke-width="3" filter="url(#shadow)"/>')
 # Fixed left/right markers in all panels represent -9 and 4, described in HTML.
 for x in [m9,m4]:
  parts.append(f'<path d="M{x:.3f} 90V254" stroke="#c3cdbb" stroke-width="3" stroke-dasharray="6 8"/>')
 parts.append('<path d="M36 186H322" stroke="#8e998a" stroke-width="4"/><path d="M322 186l-10 -6v12Z" fill="#8e998a"/>')
 parts.append(f'<path d="M44 186H{end:.3f}" stroke="{color}" stroke-width="11"/><path d="M31 186l18 -12v24Z" fill="{color}"/>')
 parts.append(f'<circle cx="{end:.3f}" cy="186" r="12" fill="{color if filled else "white"}" stroke="{color}" stroke-width="6"/>')
 # Soft shading consistently extends only left of the condition endpoint.
 parts.append(f'<rect x="42" y="136" width="{end-42:.3f}" height="28" rx="12" fill="{color}" opacity=".12"/>')
 parts.append('</g>')
parts.append('</svg>')
Path('docs/comics/art/q-327.svg').write_text(''.join(parts))
