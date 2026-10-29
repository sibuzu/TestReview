from pathlib import Path
import json,math
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#9b7546"/></marker></defs>']
s.append('<g><rect width="360" height="360" fill="#f6f9ee"/><circle cx="85" cy="180" r="23" fill="#d5e9f4" stroke="#5d88a3" stroke-width="4"/><circle cx="248" cy="180" r="69" fill="#f4dfbf" stroke="#b38245" stroke-width="4"/><path d="M85 180H108M248 180H317" fill="none" stroke="#59665b" stroke-width="4"/><circle cx="85" cy="180" r="4" fill="#59665b"/><circle cx="248" cy="180" r="4" fill="#59665b"/></g>')
for i in [1,2]:
 s.append(f'<g transform="translate({i*360},0)"><rect width="360" height="360" fill="#f3f8fa"/><path d="M55 165H95V254H200V165H320V290H55Z" fill="#add4e6" stroke="#587c8c" stroke-width="4"/><rect x="55" y="153" width="40" height="12" fill="#c3c7c9" stroke="#626d75" stroke-width="3"/><rect x="200" y="153" width="120" height="12" fill="#c3c7c9" stroke="#626d75" stroke-width="3"/>')
 s.append('<path d="M75 62V141" stroke="#9b7546" stroke-width="6" marker-end="url(#arr)"/>')
 if i==1:s.append('<path d="M260 143V66" stroke="#9b7546" stroke-width="6" marker-end="url(#arr)"/>')
 else:s.append('<rect x="210" y="93" width="100" height="59" rx="4" fill="#e8bd87" stroke="#9f7748" stroke-width="4"/><path d="M226 108H294M226 137H294" stroke="#c19461" stroke-width="2"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-038.svg').write_text(''.join(s))
rsmall=23;rlarge=69;areaRatio=rlarge*rlarge/(rsmall*rsmall);force=30*areaRatio;assert areaRatio==9 and force==270
Path('docs/comics/q-038-force-validation.json').write_text(json.dumps({'id':'q-038','circleRadiiPx':[rsmall,rlarge],'radiusRatio':3,'areaRatio':areaRatio,'smallForceKgw':30,'largeSupportedForceKgw':force,'pistonCrossSectionWidths':[40,120],'pistonUndersideSameY':165,'closedLiquidConnection':True,'arrowLengthsIndicateMagnitude':False,'assumptions':'理想水壓機，忽略摩擦及活塞自重差；壓力增量相同，不把半徑比直接當施力比。'},ensure_ascii=False,indent=2)+'\n')
