from pathlib import Path
from PIL import Image
R=Path.cwd();B=R/'docs/imports/new-gpt-20261119-73/lane3'
boxes={1163:(7,(135,765,1015,1010)),1164:(8,(50,505,1065,835)),1165:(9,(10,910,1055,1215)),1166:(10,(10,350,1060,615)),1167:(11,(15,445,1065,765)),1168:(12,(15,535,1065,765))}
for q,(n,box) in boxes.items():Image.open(R/f'docs/source-pages/chatgpt-6aff02c8-{n}.jpg').crop(box).save(B/f'crops/q-{q}-original.png')
