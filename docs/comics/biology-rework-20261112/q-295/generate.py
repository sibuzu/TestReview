from pathlib import Path
import math,json,datetime,html
R=Path(__file__).resolve().parents[4];D=json.loads((R/'site/dist/data.json').read_text());q=next(q for q in D['questions'] if q['id']=='q-295')
C={'r':'#bf3f3f','g':'#32925c','b':'#3d65b3','ink':'#35564b'}
def txt(x,y,s,size=13,color=C['ink']):return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{color}">{html.escape(s)}</text>'
def ray(x,y,xx,yy,col,dash=False):
 a=math.atan2(yy-y,xx-x);return f'<path d="M{x} {y}L{xx} {yy}M{xx-8*math.cos(a-.5)} {yy-8*math.sin(a-.5)}L{xx} {yy}L{xx-8*math.cos(a+.5)} {yy-8*math.sin(a+.5)}" fill="none" stroke="{col}" stroke-width="3"'+(' stroke-dasharray="3 3"' if dash else '')+'/>'
def fish(cx,cy,col,scale=1):
 return f'<g transform="translate({cx},{cy}) scale({scale})"><path d="M-32 0L-58-23v46Z" fill="{col}" stroke="#35564b"/><ellipse rx="37" ry="24" fill="{col}" stroke="#35564b" stroke-width="1.5"/><path d="M-9-23L3-36l13 14M-9 23l12 12 13-13" fill="{col}" stroke="#35564b"/><circle cx="22" cy="-7" r="4" fill="#fff"/><circle cx="23" cy="-7" r="2" fill="#233b33"/><path d="M15-15q-8 16 0 30" fill="none" stroke="#35564b"/></g>'
def eye(x,y,s=1):return f'<g transform="translate({x},{y}) scale({s})"><path d="M-15 0q15-17 30 0q-15 17-30 0" fill="#fff" stroke="#35564b"/><circle r="5" fill="#294b44"/></g>'
def base(s,title):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240"><title>{html.escape(title)}</title><rect width="240" height="240" fill="#faf8ef"/>{s}</svg>'
frames=[]
s=fish(107,135,C['r'])+ray(35,48,97,104,C['r'])+ray(141,135,196,135,C['r'])+eye(216,135)+txt(38,32,'R',19,C['r'])+txt(175,113,'R',16,C['r']);frames.append((s,'紅光照來，紅色反射光朝觀察者眼睛，魚呈紅色'))
s=fish(107,135,'#282e2b')+ray(35,48,97,104,C['b'])+ray(141,135,196,135,'#bfc9c2',True)+eye(216,135)+txt(38,32,'B',19,C['b'])+txt(167,171,'≈ 0',16);frames.append((s,'藍光照來，朝眼睛的反射極弱，以灰虛線表示近零，魚暗黑'))
s=fish(111,150,C['r'])+ray(38,52,95,120,C['r'])+ray(173,52,127,120,C['g'])+ray(148,150,198,150,C['r'])+eye(217,150)+txt(37,33,'R',19,C['r'])+txt(174,33,'G',19,C['g'])+txt(180,130,'R',16,C['r']);frames.append((s,'額外採紅色物體模型時，紅綠同照仍主要反射紅，綠不畫成已知必然反射'))
s=fish(62,103,C['r'],.66)+fish(174,103,'#d4b341',.66)+ray(72,124,72,174,C['r'])+eye(72,196,.8)+ray(166,124,166,174,C['r'])+ray(180,124,180,174,C['g'])+eye(173,196,.8)+txt(59,43,'R',18,C['r'])+txt(173,43,'R + G',18)+txt(120,229,'?',18);frames.append((s,'第四圖條件比較：左主要反射紅可紅色；右若能以適當比例反射紅與綠可呈黃，不能由原題斷定綠光反射'))
paths=[]
for i,(s,title) in enumerate(frames):
 p=R/f'docs/comics/art/q-295-four-image-v2-panel-{i+1}.svg';p.write_text(base(s,title));paths.append(str(p.relative_to(R)))
texts=[('① 紅光下紅，表示能反射紅','左上R是入射紅光；魚將紅光反射進眼睛，所以看到紅色。物體顏色不能只看燈光，還要看反射能力。','R＝紅光，箭頭分別表示入射及朝眼睛反射。'),('② 藍光下黑，表示藍反射很弱','B是入射藍光，朝眼睛的灰虛線表示反射接近零。這只能判斷藍光反射弱，不能順便推出綠光也一定不反射。','B＝藍光；灰虛線為極弱反射，不代表黑色光。'),('③ 原卷採紅色物體模型選A','紅綠同照時，仍有魚能反射的紅光。依已確認的原卷預期模型，若主要反射紅、吸收綠，便呈紅色，選A。','R＝紅，G＝綠；本格另採紅色物體模型，並非新增原題已知。')]
spec=dict(id='q-295',subject=q['subject'],title='看入射光，也看魚能反射的光',art=paths[0],panels=[dict(heading=h,text=t,alt=frames[i][1],caption=c,image=paths[i]) for i,(h,t,c) in enumerate(texts)],fourth=dict(answer='原卷預期答案 A：紅色（已確認）',points=['第四圖左是主要反射紅的模型，符合原卷預期A。','右是另一可能：若也反射適當比例綠光，可能出現黃色等色調。','原題沒有給綠光單獨照射結果；保留這項已確認的條件限制，不重問。'],image=paths[3],alt=frames[3][1]),protectedWords=['紅光','藍光','綠光','反射','紅色物體','原卷預期','入射光'],generationMethod='four authored native SVG additive-light/reflectance ray diagrams',generatorFile=str(Path(__file__).relative_to(R)),sourceGeneratedArtUsed=False,originalMaterialsChecked=True,originalMaterials=['site/dist/'+x for x in q['images']]+['site/dist/'+f['src'] for f in q['questionFigures']],answerCheckedAgainst=q['question']+'\n'+q['answer']+'\n'+q['explanation'],rationale='原卷與附圖實開核對，保留使用者已確認A與綠光未交代限制。四張精確色光/光路示意分別表示紅反射、藍弱反射、教材預期模型、條件比較；不把紅綠燈混合必呈黃誤套到所有物體，也不將綠光吸收視為原題已知。',createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),visualChecked=False,productionReview=dict(reviewerAgent='/root',originalVisualChecked=True,answerAndExplanationChecked=True,sourceQuestionUnchanged=True,checks=['紅色入射/紅色反射分清，箭頭由光源至物體至眼睛','藍反射弱以灰虛線，不畫黑色光束','第三格將綠吸收明示額外模型','第四格黃為另一條件下可能結果，不改原卷A或重開確認']))
(R/'docs/comics/q-295.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n');(Path(__file__).parent/'production-review.json').write_text(json.dumps(spec['productionReview'],ensure_ascii=False,indent=2)+'\n')
print('q295 four ray diagrams ready; confirmed condition caveat retained')
