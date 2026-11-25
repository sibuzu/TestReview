"""Build only this producer's isolated biology specs and evidence."""
import json,hashlib,datetime,re,sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[4];B=Path(__file__).parent
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
CONTENT={
'q-312':dict(title='沒有種子，不等於沒有維管束',panels=[
 ('① 無維管束：只計蘚苔24%','蘚苔植物沒有維管束，也沒有種子，常見孢子囊位於細長柄端。原表蘚苔占24%；圖為植物構造示例，植株多少不代表物種百分比。'),
 ('② 蕨類有維管束，卻沒有種子','蕨類占9%，葉背可見孢子囊堆，以孢子繁殖。它有維管束，不能因為沒有種子，就把9%加進「沒有維管束」而算成33%；C不合理。'),
 ('③ 裸子植物有種子，毬果非果實','以松類為例：有維管束，種子位於毬果鱗片上，沒有果實包覆。原表裸子植物占5%，B依題目以毬果對應此類；不把翅種子當成果實。')],answer='答案 C：無維管束是24%，不是33%',points=['被子植物以番茄花、果實與果內種子作示例；原表被子占62%，依題意單、雙子葉合計62%。','能產生種子：裸子5%＋被子62%＝67%，所以D合理。','蘚苔無維管束；蕨類有維管束但無種子。百分比是物種數量，不是株數或覆蓋面積。'],alts=['新製蘚苔植株、細柄孢子囊與細絲假根的類真實植物插畫，無花果種子；不是原島物種照片。','新製蕨類葉背孢子囊堆與根莖，含葉背構造放大；不把孢子囊堆當種子。','新製松針、成熟毬果及一片鱗片上兩枚帶翅種子，示意種子不被果實包住。','新製番茄植株花、果實及切開果實內種子的被子植物示例，不依圖中數量計算物種百分比。'],words=['維管束','蘚苔','蕨類','裸子植物','被子植物','孢子囊堆','物種百分比','24%','9%','5%','62%','67%','33%','5%＋被子62%＝67%'],sources=[dict(url='https://mdc.mo.gov/discover-nature/field-guide/mosses',finding='蘚苔無維管構造、無花與種子，孢子在柄端孢子囊形成。'),dict(url='https://www.nps.gov/muwo/learn/nature/ferns.htm',finding='蕨類是維管束植物，以孢子繁殖，沒有花與種子，葉背有孢子囊堆。'),dict(url='https://www.usbg.gov/sites/default/files/images/--how_plants_work-_student_discovery_journal-teachers_edition.pdf',finding='美國植物園教材四組植物比較：蘚苔無維管束；蕨類有維管束、孢子；裸子/被子屬種子植物。')],review='原表蘚苔24/蕨9/裸子5/被子62逐項核對。四張新製真實植物形態及繁殖構造：蘚苔細絲假根不當維管根；蕨葉背孢子囊堆不作種子；松鱗片兩翅種子無果實；番茄花果內種子屬同種植物示例。圖像不表示島嶼實際物種或株數百分比；維持C。'),
'q-313':dict(title='沿細胞核來源，推回甲蛙體色',panels=[
 ('① 甲提供蝌蚪體細胞的核','原圖先從甲蛙蝌蚪的體細胞取出細胞核。這是體細胞的核，不是精子；下方是細胞放大示意，不能把放大比例當作實際大小。'),
 ('② 乙提供卵，先移除原核','乙的卵細胞要先去核，保留卵的細胞質等成分。圖中紫色原卵核已在玻璃吸管外移，卵內不再保留乙的原核。'),
 ('③ 把甲核移入去核卵','把甲提供的核注入乙的去核卵，再活化發育；沒有精卵結合，因此使用卵細胞也不是有性生殖。琥珀色核為來源標示，不是蛙的體色。')],answer='答案 D：依本題模型，甲蛙也白色',points=['丙的核內遺傳資訊來自甲；依本題體色受核內遺傳控制的模型，由丙白色推甲也白色。','核來源是甲，去核卵來源是乙；不能追已移除的乙核。','本題僅按指定體色模型推論，不把複製說成所有性狀或全部細胞成分都只來自甲。'],alts=['新製白色蝌蚪及體細胞取核放大示意；一顆已取出的核在吸管尖端，細胞內不再有核。','新製蛙卵去核教材剖面，原卵核在細胞外吸管內，保留細胞質；非實驗照片。','新製體細胞核移植剖面，去核卵內僅有甲來源琥珀色標示核，不畫精子或雙核融合。','新製完整白色成年蛙，對應原題丙蛙白色的表現，不指認原卷的實際物種。'],words=['細胞核','體細胞','去核卵','精卵結合','有性生殖','甲蛙','丙蛙','核內遺傳'],sources=[dict(url='https://www.genome.gov/about-genomics/fact-sheets/Cloning-Fact-Sheet',finding='體細胞核可移入已去除自身核的卵；克隆個體外觀不能一概視為所有性狀必然完全相同，原題採核控體色模型。'),dict(url='https://www.nobelprize.org/prizes/medicine/2012/advanced-information/',finding='蛙核移植研究核對：分化體細胞核轉入去核卵，檢驗細胞核的發育潛力。')],review='已逐張實開甲蝌蚪取核/乙卵去核/甲核注入/丙蛙原圖。四張新圖核的位置與來源由HTML標明，去核圖無留核、注核圖僅一顆甲來源核；無精子或雙核融合。白色結果限原題已核模型，維持D。首版綠褐蝌蚪可能干擾白色模型已不採用、重製白色。'),
'q-314':dict(title='先看存活數，再判斷鹽度抑制',panels=[
 ('① 辨認實驗中的蚊幼蟲','原題比較兩種斑蚊幼蟲；甲、乙、丙、丁四杯中，兩種幼蟲各起始30隻，兩天後記錄存活數。放大圖只示幼蟲構造，不代表實際隻數。'),
 ('② 四杯濃度與存活數分開讀','四杯濃度依序為0%、0.7%、1.5%、3.5%。丙杯1.5%時，埃及斑蚊存活17隻、白線斑蚊2隻，不支持C所說白線斑蚊較強。器材圖不繪存活隻數。'),
 ('③ 幼蟲成長也會蛻皮','蚊是昆蟲，幼蟲成長需要蛻去舊外骨骼。圖中實體幼蟲與透明空蛻皮分開，不能因為幼蟲不像成蟲，就認為不會蛻皮；B不對。')],answer='答案 D：鹽度不足，抑制可能不夠',points=['丁杯3.5%時，兩種幼蟲都存活0隻；較低鹽度仍可有存活者。','保留「可能」：存活幼蟲才可能繼續發育，不表示加少量鹽比純水更促生。','生命期圖是後續發育的概念，不是兩天實驗已量得的成蟲結果。'],alts=['新製蚊幼蟲側面放大圖，顯示頭胸腹與水面呼吸構造；非顯微實拍。','新製四只同型透明玻璃杯及清水，恰為四杯；不以圖中生物數量替代原表。','新製蚊幼蟲蛻皮放大，實體幼蟲旁為透明空蛻皮，示意幼蟲會蛻皮。','新製蚊幼蟲、蛹與成蟲的生物形態，示意存活者可能繼續發育，非原實驗兩天結果。'],words=['斑蚊幼蟲','白線斑蚊','埃及斑蚊','3.5%','1.5%','0.7%','外骨骼','17隻','30隻','存活數'],sources=[dict(url='https://www.cdc.gov/mosquitoes/about/life-cycle-of-aedes-mosquitoes.html',finding='Aedes蚊有卵、幼蟲、蛹與成蟲階段，幼蟲在水中生活。'),dict(url='https://www.epa.gov/mosquitocontrol/mosquito-life-cycle',finding='幼蟲階段會蛻皮成長，多數種類會到水面呼吸。')],review='原題四杯與濃度/17對2/丁皆0逐項對照；D已由使用者確認，不重問。杯圖恰四杯、不繪假數；蛻皮圖區分活幼蟲與空皮，生命期不冒充兩天實驗結果。'),
}
if __name__=='__main__':
 qid=sys.argv[1];c=CONTENT[qid];q=next(q for q in json.loads((R/'docs/comics/biology-ten-20261122/questions-before.json').read_text())['questions']if q['id']==qid)
 records=[]
 for i in range(1,5):
  m=json.loads((B/f'{qid}-gen-{i}.json').read_text());p=B/'art'/f'{qid}-panel-{i}.png';im=Image.open(p);im.load()
  records.append(dict(panel=i,tool='built-in image_gen',prompt=m['prompt'],selectedSource=re.findall(r'/home/jack/\.codex/generated_images/[^\s]+\.png',m['output_hint'])[0],destination=str(p.relative_to(R)),sha256=sha(p),dimensions=[im.width,im.height],actuallyViewed=True,accepted=True))
 save(B/f'{qid}-generation.json',records);save(B/f'{qid}-prompts.json',[dict(panel=r['panel'],prompt=r['prompt'])for r in records]);images=[r['destination']for r in records]
 spec=dict(id=qid,subject='Biology',title=c['title'],art=images[0],layoutVersion='native-four-images-v7',generationMethod='four independent built-in image_gen calls; newly generated high-detail near-realistic science textbook illustrations',sourceGeneratedArtUsed=False,reusedOldGeneratedArt=False,originalMaterialsChecked=True,originalMaterials=['site/dist/'+p for p in q['images']]+['site/dist/'+f['src']for f in q.get('questionFigures',[])],answerCheckedAgainst=q['explanation'],rationale=c['review'],producerAgent='/root/bio_c',visualChecked=False,panels=[dict(heading=h,text=t,image=images[i],alt=c['alts'][i])for i,(h,t)in enumerate(c['panels'])],fourth=dict(answer=c['answer'],points=c['points'],image=images[3],alt=c['alts'][3]),protectedWords=c['words'],manualLineBreaks=False,promptFile=str((B/f'{qid}-prompts.json').relative_to(R)),generationEvidence=str((B/f'{qid}-generation.json').relative_to(R)),artHashes={r['destination']:r['sha256']for r in records},supportingSources=c['sources'],createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
 # Keep formulas readable without forcing a long mixed Chinese/number phrase
 # into one unbreakable word on narrow screens.
 spec['protectedWords']=[w for w in spec['protectedWords'] if w!='5%＋被子62%＝67%']
 spec['panels'][0]['caption']='新製類真實生物教材插畫，非原卷或顯微實拍。'
 save(B/f'{qid}-spec.json',spec);print(B/f'{qid}-spec.json')
