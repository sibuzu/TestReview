from PIL import Image
from pathlib import Path
R=Path.cwd();B=R/'docs/imports/new-gpt-20261119-73/lane3'
boxes={1163:(7,(95,800,1055,1000)),1164:(8,(50,505,1065,850)),1165:(9,(10,920,1055,1185)),1166:(10,(10,365,1060,615)),1167:(11,(15,425,1065,640)),1168:(12,(15,535,1065,765))}
for q,(n,box) in boxes.items():Image.open(R/f'docs/source-pages/chatgpt-6aff02c8-{n}.jpg').crop(box).save(B/f'crops/q-{q}-original.png')
figures={1163:(7,(165,855,1020,992)),1165:(9,(820,920,1030,1140)),1166:(10,(760,355,1040,460)),1168:(12,(830,535,1040,710))}
for q,(n,box) in figures.items():Image.open(R/f'docs/source-pages/chatgpt-6aff02c8-{n}.jpg').crop(box).save(B/f'crops/q-{q}-figure.png')
im=Image.open(R/'docs/source-pages/chatgpt-6aff02c8-7.jpg').rotate(-7,expand=True,fillcolor='white');im.crop((155,830,1000,1065)).save(B/'crops/q-1163-original.png');im.crop((240,900,1000,1065)).save(B/'crops/q-1163-figure.png')
Image.open(R/'docs/source-pages/chatgpt-6aff02c8-12.jpg').crop((755,535,1050,710)).save(B/'crops/q-1168-figure.png')

# Tilted originals: retain each option's original pixels and full axes without adjacent q19 text.
p=B/'crops/q-1163-figure.png';im=Image.open(p);parts=[im.crop(box) for box in [(0,0,170,132),(180,0,365,138),(370,0,565,157),(570,0,760,165)]];out=Image.new('RGB',(sum(c.width for c in parts)+30,175),'white');x=0
for c in parts:out.paste(c,(x,0));x+=c.width+10
out.save(p)
