from pathlib import Path
import json,hashlib,datetime,sys
P=Path('docs/comics');SOURCE='https://chatgpt.com/share/6aec9480-acd4-83ec-93b8-0728550cb2a2'
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
 x=dict(id=q,subject='Math',title=title,art=str(art),layoutVersion='native-fluid-v6',panels=panels,fourth=dict(answer=answer,points=points),protectedWords=words,sourceUrl=SOURCE,originalMaterialsChecked=True,originalChecked=dict(path=original,visualChecked=True),sourceGeneratedArtUsed=False,generationMethod='new selectable native HTML mathematics diagrams with exact formulas, Chinese roles, values, units and action arrows; deterministic SVG fallback; imagegenCalls=0',rationale=rationale,designFile=f'docs/comics/{q}-design.txt',artSHA256=hashlib.sha256(art.read_bytes()).hexdigest(),visualChecked=False)
 (P/f'{q}-design.txt').write_text(rationale+'\n原卷：'+original+'\n'+json.dumps(panels,ensure_ascii=False,indent=2)+'\n')
 (P/f'{q}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def reviewed(q,note):
 p=P/f'{q}.json';x=json.loads(p.read_text());x.update(visualChecked=True,checkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),previewValidation=f'docs/comics/{q}-preview-validation.json',visualReview=note);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def build(q):
 if q=='q-961':
  spec(q,'減2後整體平方，再依序運算',[
   panel('① 每一步都接續上一步的結果','減2後得到x－2，下一步的平方要作用在整個x－2，須加括號；不是只將2平方。',flow('原流程的前半段',[n('輸入：x'),n('減2：x－2',tone='gold'),n('平方：（x－2）²',tone='green')],'依序處理上一個結果'),'中文標示輸入x、減2後x－2、整體平方（x－2）²。'),
   panel('② 再乘5、減13，最後才展開','平方後乘5，再減13，得y＝5（x－2）²－13。展開時5要乘括號內每一項，中間項是－20x。',flow('原流程的後半段',[n('乘5：5（x－2）²'),n('減13：y＝5（x－2）²－13',tone='gold'),n('展開：y＝5x²－20x＋7',tone='green')],'接續運算，再整理代數式'),'精確HTML保留平方範圍、乘5、減13與展開的中間項。'),
   panel('③ 用x＝2檢查B的平方範圍','輸入2時，流程先得到0，最後輸出－13。B是5（x－2²）－13，代入卻是－23；C才與流程相符。',paths('同一個輸入，核對輸出',[n('依流程／選項C：－13','先減2後，整體平方。','green'),n('選項B：－23','B只把2平方，範圍不同。','gold')],'B不符；C符合原流程','都以x＝2代入比較'),'同輸入2時比較B輸出－23與原流程和C輸出－13。')
  ],'答案 C：y＝5x²－20x＋7',['平方的是減2後的整個結果。','（x－2）²＝x²－4x＋4，再全部乘5。','B把平方放在2上；不能因有括號就當成同一式。'],['原流程','平方範圍','整體平方','中間項','x＝2','x－2','（x－2）²','5（x－2）²','5x²－20x＋7','－20x','－13','－23'],'本題正是運算流程與代數範圍辨認，以可選取中文步驟和精確公式呈現整體平方/乘法分配/同值檢查，比人物裝飾或生成公式清楚；原題B指數在2上如實保留。','docs/imports/new-gpt-20261105-b/originals/page1-q7.png')
 elif q=='q-962':
  spec(q,'同一個x看高度，先辨交點左右',[
   panel('① 交點：相同x有相同函數值','P（2，－3）同時在兩線上；把x＝2代入兩個函數，結果都等於－3。因此A的等號正確，不是題目要找的錯誤。',flow('交點的確定條件',[n('P（2，－3）：x＝2'),n('L₁：2a＋b＝－3','L₂：2c＋d＝－3','gold'),n('所以2a＋b＝2c＋d',tone='green')],'同一交點，兩線高度相同'),'交點P的兩座標與兩線代入式直接中文標明，A等式成立。'),
   panel('② 交點右側：L₁在上方','圖中x＝3在交點右側，L₁的函數值較大，應為3a＋b＞3c＋d。B把符號寫成小於，所以B才是錯誤敘述。',paths('固定x＝3，比較兩線',[n('L₁的高度：3a＋b',tone='green'),n('L₂的高度：3c＋d',tone='gold')],'L₁較高：3a＋b＞3c＋d','由原圖右側的上下位置判斷'),'x＝3時兩線的函數式與L₁在上的大於關係直接標示，不猜個別斜率。'),
   panel('③ 交點左側：C、D也要核對','x＝0、x＝－1都小於2，此時L₁在L₂下方。分別代入，可知C、D的小於符號都正確。',flow('左側x＜2：L₁較低',[n('x＝0：b＜d','對應C：比較兩個y截距。'),n('x＝－1：－a＋b＜－c＋d','對應D：同樣比較左側高度。','green')],'代入同一個x，保留高低關係'),'中文標明左側x＜2、x＝0對應C與x＝－1對應D，兩者L₁較低。')
  ],'答案 B：x＝3時應為大於',['交點x＝2：兩線相等，A正確。','交點右側：L₁較高；左側：L₁較低。','題目問錯誤敘述，B的小於符號不符圖形。'],['函數值','交點右側','交點左側','y截距','P（2，－3）','x＝2','x＝3','x＝0','x＝－1','L₁','L₂','2a＋b＝2c＋d','3a＋b＞3c＋d','－a＋b＜－c＋d'],'以可選取HTML把原圖交點、同x高度、交點左右位置直接對應各代數選項；精確數據僅使用原圖P（2，－3），不杜撰兩條線的個別斜率或截距數值。','docs/imports/new-gpt-20261105-b/originals/page2-q16.png')
 elif q=='q-963':
  spec(q,'由起始間距與追上時間寫函數',[
   panel('① 先讀軸：y是兩車間距','橫軸x是時間，單位秒；縱軸y是兩車間距，單位公尺。剛開始相距10公尺，50秒時距離為0，表示甲追上乙。',flow('共圖的兩個確定點',[n('x＝0秒：y＝10公尺','座標（0，10）。'),n('x＝50秒：y＝0公尺','座標（50，0）：追上。','green')],'時間經過50秒，間距縮至0'),'橫軸秒與縱軸公尺直接標示起始點（0，10）及追上點（50，0）。'),
   panel('② 每秒的間距變化是負的','50秒內間距由10降到0，改變量為－10公尺。除以50秒，得到每秒－0.2公尺，也就是斜率－1/5。',flow('斜率＝間距變化÷時間變化',[n('間距變化：0－10＝－10公尺'),n('時間變化：50－0＝50秒',tone='gold'),n('斜率：－10÷50＝－1/5','單位：公尺／秒。','green')],'計算同一段時間的變化率'),'精確列出縱向變化－10公尺、時間50秒及負斜率－1/5公尺每秒。'),
   panel('③ 初值10，加上每秒變化','截距是開始時的10，故y＝－（1/5）x＋10。再把0秒、50秒代回，兩個端點都吻合，所以選B。',paths('回代驗證B',[n('x＝0：y＝10','對應一開始相距10公尺。'),n('x＝50：y＝0','對應50秒追上。','green')],'B：y＝－（1/5）x＋10','初值與追上時刻都要符合'),'B函數代入兩個已知時刻，逐一核對初始間距與追上時刻。')
  ],'答案 B：y＝－（1/5）x＋10',['間距逐漸縮短，所以斜率為負。','一開始相距10公尺，所以截距為正10。','此圖描述追上前0至50秒，y不是任何一車的路程。'],['兩車間距','追上時間','變化率','橫軸','縱軸','初始間距','公尺／秒','（0，10）','（50，0）','－1/5','y＝－（1/5）x＋10'],'以精確中文HTML標示原共圖的兩軸單位、兩個端點和斜率/截距，逐步形成負斜率函數並代回驗證；不把乙車速率2當間距斜率，不延伸成追上後負距離。','docs/imports/new-gpt-20261105-b/originals/page2-q17-18-common.png')
 elif q=='q-964':
  spec(q,'間距縮短速率，加回乙車速率',[
   panel('① 50秒追上，先求相對速率','甲原本落後乙10公尺，經過50秒追上。每秒縮短10÷50＝0.2公尺，表示甲每秒比乙多走0.2公尺。',flow('原共圖提供的追及條件',[n('初始間距：10公尺'),n('追上時間：50秒',tone='gold'),n('相對速率：10÷50＝0.2公尺／秒','這是速率差，不是甲的速率。','green')],'初始間距÷追上時間'),'中文明標10公尺、50秒及0.2公尺每秒是相對速率差。'),
   panel('② 乙每秒2公尺，甲要再快0.2','甲在後面且能追上，速率必須比乙大。將乙的2加上速率差0.2，甲的速率就是2.2公尺／秒。',paths('分清兩車與相對速率',[n('乙的速率：2公尺／秒'),n('甲比乙快：0.2公尺／秒',tone='gold')],'甲的速率：2＋0.2＝2.2公尺／秒','乙速率＋甲乙速率差'),'乙車2與速率差0.2相加得到甲車2.2，角色、單位、相加動作均明示。'),
   panel('③ 求甲自A點走的路程','甲的速率乘30秒，得2.2×30＝66公尺。另可核對：乙在距A點70公尺處，兩車還差4公尺，甲便在70－4＝66公尺處。',paths('30秒時，以兩種方式核對',[n('甲的路程：2.2×30＝66公尺',tone='green'),n('由乙的位置回推：70－4＝66公尺','乙位置10＋2×30＝70；間距10－0.2×30＝4。')],'甲自A點移動66公尺：D','速率×時間，或位置減間距'),'完整標示甲路程66、乙距A點位置70及剩餘間距4，兩種計算互核。')
  ],'答案 D：66公尺',['0.2是兩車的速率差，不能直接當甲速率。','甲速率2.2公尺／秒，30秒走66公尺。','乙移動60公尺與兩車間距4公尺，皆非本題所問。'],['相對速率','追上時間','速率差','甲的速率','乙的速率','甲車路程','A點','10公尺','50秒','30秒','0.2公尺／秒','2.2公尺／秒','66公尺','70公尺','4公尺'],'精確中文HTML分出乙速率、甲乙速率差、甲速率與甲路程，全部標單位及加法箭頭；用30秒的乙位置/剩餘間距交叉驗算，避免無標車圖讓讀者猜2與0.2分屬何量。','docs/imports/new-gpt-20261105-b/originals/page2-q17-18-common.png')
 else:raise ValueError(q)
if __name__=='__main__':build(sys.argv[1])
