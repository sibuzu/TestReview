from pathlib import Path
import json,hashlib,datetime
P=Path('docs/comics');q='q-960'
def n(label,detail=None,tone='blue'):
 x=dict(label=label,tone=tone)
 if detail:x['detail']=detail
 return x
art=P/'art'/f'{q}.svg'
art.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="2160" height="720" viewBox="0 0 2160 720"><rect width="2160" height="720" fill="#f4faf8"/>'+''.join(f'<g transform="translate({i*720} 0)"><rect x="110" y="55" width="500" height="160" rx="16" fill="#e0eef9" stroke="#416789" stroke-width="4"/><path d="M360 235v55m-18-18 18 18 18-18" stroke="#846328" stroke-width="7" fill="none"/><rect x="110" y="310" width="500" height="130" rx="16" fill="#fff0d2" stroke="#9b7430" stroke-width="4"/><path d="M360 460v55m-18-18 18 18 18-18" stroke="#846328" stroke-width="7" fill="none"/><rect x="110" y="535" width="500" height="130" rx="16" fill="#ddf2e9" stroke="#367f6c" stroke-width="4"/></g>' for i in range(3))+'</svg>')
panels=[
 dict(heading='① D：條件、理由、方向都一致',text='原文明說，這些食物鏈底層種類的食物來源豐富，數量相對較多，因此建議食用。D的對象、理由與選擇方向都對應本文。',diagram=dict(kind='flow',title='只按本文的推論鏈',items=[n('本文：食物鏈底層種類','如文蛤、牡蠣、鮑魚、九孔。'),n('食物來源豐富，數量相對多',tone='gold'),n('因此建議食用：對應D',tone='green')],arrow='本文條件→理由→選擇方向'),alt='中文逐步標出本文食物鏈底層、來源豐富與相對量多、建議食用D。'),
 dict(heading='② C：前半相似，例子卻放錯',text='本文說櫻花蝦用中層網，不接觸海底。C把它當成底拖漁網的例子，因此整句不能判對；先核漁法再核例子。',diagram=dict(kind='paths',title='漁法與例子分開核對',items=[n('櫻花蝦：中層網','本文：不會接觸海底。','green'),n('本文避免：底拖網海蝦','不能以櫻花蝦作此例。','gold')],target='C的例子不符本文',arrow='對照漁法及是否接觸海底'),alt='明標櫻花蝦中層網不接觸海底，與文中避免的底拖網海蝦分開。'),
 dict(heading='③ A、B：理由與數量也要核',text='A加上肉質鮮嫩、重金屬等本文沒提供的理由；B又把珊瑚礁定棲魚的數量較少反寫為較多。不能只見幾個相同字就選。',diagram=dict(kind='paths',title='兩種常見誤讀',items=[n('A：額外加入理由','肉質、重金屬：本文未提。','gold'),n('B：把數量方向反轉','本文說較少，選項說較多。','purple')],target='選項整句都要有本文依據',arrow='同時檢查理由與限定條件'),alt='A無據加入肉質和重金屬，B將數量較少改成較多，兩類錯誤直接中文標示。')]
rationale='本題教學為資訊一致性與漁法/例子對應，用全新可選取中文HTML精確標出條件、理由、數量方向及接觸海底關係；不畫未給數量的魚群統計，不把閱讀文的當時名單當現今消費建議。'
x=dict(id=q,subject='Chinese',title='選項要整句有依據，連例子也要核',art=str(art),layoutVersion='native-fluid-v6',panels=panels,fourth=dict(answer='答案 D：食物鏈底層，數量相對較多',points=['D的對象、理由、選擇方向都符合本文。','C把櫻花蝦的中層網錯套成底拖網。','A無據加理由，B反轉數量；相似字詞不等於整句正確。']),protectedWords=['食物鏈底層','食物來源','相對較多','文蛤','牡蠣','鮑魚','九孔','櫻花蝦','中層網','底拖網','海底','珊瑚礁','定棲魚','肉質鮮嫩','重金屬','限定條件'],sourceUrl='https://chatgpt.com/share/6aeb402e-c158-83ee-b603-6444a590bf27',originalMaterialsChecked=True,originalChecked=dict(path='docs/imports/new-gpt-20261104-c/lane3/originals/seafood-q2.png',visualChecked=True),sourceGeneratedArtUsed=False,generationMethod='new selectable native HTML reading-evidence and fishing-method diagrams with exact Chinese labels; deterministic SVG fallback; imagegenCalls=0',rationale=rationale,designFile=f'docs/comics/{q}-design.txt',artSHA256=hashlib.sha256(art.read_bytes()).hexdigest(),visualChecked=False)
(P/f'{q}-design.txt').write_text(rationale+'\n'+json.dumps(panels,ensure_ascii=False,indent=2)+'\n')
(P/f'{q}.json').write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
