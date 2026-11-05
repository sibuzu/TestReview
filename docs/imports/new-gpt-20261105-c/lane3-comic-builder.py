from pathlib import Path
import json,hashlib,datetime,sys
P=Path('docs/comics');SOURCE='https://chatgpt.com/share/6aec94d2-678c-83ee-8f64-018320680b7a'
def n(label,detail=None,tone='blue'):
 x=dict(label=label,tone=tone)
 if detail:x['detail']=detail
 return x
def flow(title,items,arrow,note=None):
 x=dict(kind='flow',title=title,items=items,arrow=arrow)
 if note:x['note']=note
 return x
def paths(title,items,target,arrow):return dict(kind='paths',title=title,items=items,target=target,arrow=arrow)
def panel(heading,text,diagram,alt):return dict(heading=heading,text=text,diagram=diagram,alt=alt)
def spec(q,title,panels,answer,points,words,rationale,original):
 art=P/'art'/f'{q}.svg'
 art.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="720" viewBox="0 0 2160 720"><rect width="2160" height="720" fill="#f5faf8"/>'+''.join(f'<g transform="translate({720*i} 0)"><rect x="100" y="55" width="520" height="160" rx="16" fill="#e4eef9" stroke="#466e97" stroke-width="4"/><path d="M360 235v55m-20-20 20 20 20-20" fill="none" stroke="#9b732e" stroke-width="7"/><rect x="100" y="310" width="520" height="130" rx="16" fill="#fff0d2" stroke="#9b732e" stroke-width="4"/><path d="M360 460v55m-20-20 20 20 20-20" fill="none" stroke="#9b732e" stroke-width="7"/><rect x="100" y="535" width="520" height="130" rx="16" fill="#e0f3eb" stroke="#278574" stroke-width="4"/></g>' for i in range(3))+'</svg>')
 x=dict(id=q,subject='English',title=title,art=str(art),layoutVersion='native-fluid-v6',panels=panels,fourth=dict(answer=answer,points=points),protectedWords=words,sourceUrl=SOURCE,originalMaterialsChecked=True,originalChecked=dict(path=original,visualChecked=True),sourceGeneratedArtUsed=False,generationMethod='new selectable native HTML mathematics diagrams with exact formulas, Chinese roles, values, units and action arrows; deterministic SVG fallback; imagegenCalls=0',rationale=rationale,designFile=f'docs/comics/{q}-design.txt',artSHA256=hashlib.sha256(art.read_bytes()).hexdigest(),visualChecked=False)
 (P/f'{q}-design.txt').write_text(rationale+'\n原卷：'+original+'\n'+json.dumps(panels,ensure_ascii=False,indent=2)+'\n')
 (P/f'{q}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def reviewed(q,note):
 p=P/f'{q}.json';x=json.loads(p.read_text());x.update(visualChecked=True,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),previewValidation=f'docs/comics/{q}-preview-validation.json',visualReview=note);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def build(q):
 if q=='q-973':
  spec(q,'先找as原級結構，再看books',[
   panel('① as與as possible成對使用','本句的as ... as possible表示「盡可能……」，中間用原級。先辨清結構，不能把比較級more或最高級most直接放入空格。',flow('本題的句型骨架',[n('as ＋原級＋ ... ＋ as possible','意思：盡可能……。'),n('as many books as possible','把數量詞與books一起放入句型。','green')],'用原級表達盡可能的程度'),'精確英文as與as possible配對，完整呈現as many books as possible及中文語意。'),
   panel('② books是可數名詞複數','book可數，books是複數，要用many。much搭不可數名詞，不能直接修飾本題的books，所以B也不合。',paths('空格後的名詞決定數量詞',[n('books：可數名詞複數','本題所修飾的名詞。'),n('many：修飾可數名詞複數',tone='green')],'many books：結構與名詞皆符合','先看名詞，再選數量詞'),'中文明標books可數複數與many修飾關係，不拿more knowledge替換前半空格。'),
   panel('③ 後半的more不能直接搬來','後半more knowledge是「更多知識」，在原句該處正確。前半另有as ... as possible框架，須各依所在位置判斷。',paths('分清同一句中的兩個位置',[n('前半：as many books as possible','盡可能多的書；本空選A。','green'),n('後半：more knowledge','更多知識；原句用法正確。')],'前半填many，後半保留more','兩處的結構與修飾對象不同'),'精確對照前半many books與後半more knowledge，中文分別標結構角色。')
  ],'答案 A：many',['as many books as possible＝盡可能多的書。','books可數且為複數，用many，不能用much。','more、most不合此處as ... as possible的原級結構。'],['盡可能……','as ... as possible','as possible','as many books as possible','more knowledge','many books','books','book','many','much','more','most','knowledge','可數名詞','不可數名詞','比較級','最高級'],'本題教學重點是成對的as原級框架與books可數複數，精確可選取HTML語法角色/名詞關係對照比人物讀書情境更能解答選項差異；不增原題條件，後半more knowledge照留。','docs/imports/new-gpt-20261105-c/originals/english-07.png')
 elif q=='q-974':
  spec(q,'比較兩組差在哪裡，再填閱讀空格',[
   panel('① 兩組都未婚，只差有無孩子','本文先說未婚、有孩子的伴侶，81%受訪者認為是家庭；接著拿沒有孩子的情況比較，比例降到40%。改變的條件是孩子。',paths('受訪者認為是家庭的比例',[n('未婚、有孩子：81%',tone='green'),n('未婚、沒有孩子：40%',tone='gold')],'共同：未婚；差別：有無孩子','保留未婚條件，辨認兩句差別'),'直接中文標示兩組皆未婚，有孩子81%、沒有孩子40%，百分比意義為受訪者認為是家庭的比例。'),
   panel('② one回指a child，證據對上C','don\'t have one中的one代替前面的a child。兩句討論是否有孩子，所以第22格選having a child，不能只憑相愛等印象選A。',flow('由代名詞回到對比條件',[n('don\'t have one','one＝a child：沒有孩子。'),n('有孩子／沒有孩子','正是81%與40%比較的條件。','gold'),n('第22格：having a child','有孩子；對應C。','green')],'回指前文，再依證據填空'),'精確英文one指a child、兩句有無孩子對比及第22格C逐步明標。'),
   panel('③ 差距用百分點，結論限本文','81%減40%，差距是41個百分點。這是該研究受訪者如何認定家庭的資料，不能變成所有家庭都必須有孩子的規定。',flow('數據與解讀範圍',[n('81%－40%＝41個百分點','兩個比例之差，明寫百分點。','gold'),n('本題：依該研究的對比選C','不是替所有家庭定義必要條件。','green')],'區分比例差距與普遍結論'),'中文明示41個百分點而非41%，並將解讀限制於本文研究受訪者看法。')
  ],'答案 C：having a child',['兩組都未婚，婚姻不是這兩句改變的條件。','one＝a child；81%與40%對比有沒有孩子。','相差41個百分點；不推成所有家庭都必須有孩子。'],['having a child','loving each other','being married','living together','don\'t have one','a child','one','81%','40%','41個百分點','百分點','受訪者','有無孩子','未婚伴侶'],'精確中文HTML統計對照明列81%/40%的受訪者認同比例、兩組皆未婚與是否有孩子的差別；one回指原詞a child並鎖定C，41個百分點不誤標41%，不替未問21/23格填答案或將研究看法當家庭普遍定義。','docs/imports/new-gpt-20261105-c/originals/english-22-reading.png')
 else:raise ValueError(q)
if __name__=='__main__':build(sys.argv[1])
