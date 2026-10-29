from pathlib import Path
import json,math
# Simplified Taiwan-main-island outline for regional localization, not a surveyed coastline or travel-route map.
coast=[(121.54,25.30),(121.77,25.17),(121.91,25.11),(121.97,25.00),(121.84,24.79),(121.81,24.56),(121.70,24.34),(121.62,24.12),(121.59,23.89),(121.53,23.65),(121.47,23.40),(121.40,23.20),(121.28,22.99),(121.18,22.82),(121.08,22.62),(120.96,22.42),(120.88,22.18),(120.85,21.92),(120.74,21.96),(120.70,22.15),(120.63,22.30),(120.50,22.43),(120.32,22.57),(120.14,22.78),(120.05,23.01),(120.04,23.25),(120.15,23.48),(120.26,23.69),(120.43,23.90),(120.58,24.15),(120.72,24.41),(120.88,24.63),(121.04,24.83),(121.20,25.03),(121.37,25.18)]
pts={'shimen':(121.56,25.29),'yuanshan':(121.52,25.07),'shihsanhang':(121.40,25.16),'dapenkeng':(121.42,25.15),'changbin':(121.47,23.40)}
def full(p):return (105+(p[0]-120.0)*78,322-(p[1]-21.9)*85)
def north(p):return (40+(p[0]-121.2)*465,320-(p[1]-24.85)*510)
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="360" viewBox="0 0 1080 360"><defs><clipPath id="panel"><rect width="360" height="360"/></clipPath></defs>']
for i in range(3):
 s.append(f'<g transform="translate({360*i},0)" clip-path="url(#panel)"><rect width="360" height="360" fill="#edf6fa"/>')
 if i==1:
  path=[north(p) for p in coast];s.append('<path d="M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in path)+'Z" fill="#dfebd4" stroke="#81936e" stroke-width="2"/>')
  for name in ['yuanshan','shihsanhang','dapenkeng']:
   x,y=north(pts[name]);s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#517ba8" stroke="#fff" stroke-width="2"/>')
  x,y=north(pts['shimen']);s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#cf9748" stroke="#fff" stroke-width="3"/>')
 else:
  path=[full(p) for p in coast];s.append('<path d="M'+'L'.join(f'{x:.1f} {y:.1f}' for x,y in path)+'Z" fill="#dfebd4" stroke="#81936e" stroke-width="2"/>')
  x,y=full(pts['shimen']);s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#cf9748" stroke="#fff" stroke-width="2"/>')
  if i==0:s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="18" fill="none" stroke="#cf9748" stroke-width="3"/>')
  if i==2:
   x,y=full(pts['changbin']);s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#ae6759" stroke="#fff" stroke-width="2"/>')
 s.append('</g>')
s.append('</svg>');Path('docs/comics/art/q-583.svg').write_text(''.join(s))
lat=pts['shimen'][1];assert all(lat-pts[n][1]<.3 for n in ['yuanshan','shihsanhang','dapenkeng']);assert lat-pts['changbin'][1]>1.5
Path('docs/comics/q-583-location-validation.json').write_text(json.dumps({'id':'q-583','scope':'simplified Taiwan-main-island regional locator, not surveyed coastline/route map','approximateRepresentativeCoordinates':pts,'northSitesNearLat25':True,'changbinEasternTaiwanNearLat23Point4':True,'realDrivingDistancesOrTravelTimesShown':False,'noCulturalTimeRanking':True},ensure_ascii=False,indent=2)+'\n')
