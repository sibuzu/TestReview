from pathlib import Path
from html import escape
import json
P=Path('docs/imports/new-gpt-20261029-a/agent3-english');D=Path('docs/comics/art')
def text(x,y,s,z=13):return f'<text x="{x}" y="{y}" font-size="{z}" text-anchor="middle" fill="#29483e">{escape(s)}</text>'
def rect(x,y,w,h,c='#c8d9bb'):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c}"/>'
def line(x,y,xx,yy):return f'<path d="M{x} {y}L{xx} {yy}" stroke="#73928a" stroke-width="2" fill="none"/>'
def svg(n,p):
 s='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="200" viewBox="0 0 600 200"><style>text{font-family:"Noto Sans CJK TC","Noto Sans",sans-serif}</style>'
 for i,c in enumerate(p):s+=f'<g transform="translate({i*200})">'+rect(1,1,198,198,'#f5f4ec')+c+'</g>'
 (D/f'q-{n}.svg').write_text(s+'</svg>')
svg(864,[text(100,20,'兩地之間的距離')+'<path d="M16 82L42 60L68 82V119H16Z" fill="#c8d9bb"/>'+rect(137,70,48,50,'#b8d0dc')+text(42,142,'home')+text(161,142,'post office',11)+line(69,100,134,100)+text(101,87,'?',24)+text(100,176,'How far ... from ... to ...?',11),text(100,20,'騎車時間描述路程')+'<circle cx="55" cy="118" r="20" fill="none" stroke="#719085" stroke-width="3"/><circle cx="141" cy="118" r="20" fill="none" stroke="#719085" stroke-width="3"/><path d="M55 118l28-42l25 42H55l37-25l49 25l-24-56h-17M76 76h18" fill="none" stroke="#719085" stroke-width="3"/>'+text(100,165,'5 minutes by bike',14)+text(100,188,'沒有另編公里數',10),text(100,20,'看完整句型再判斷')+rect(16,44,168,36,'#bcd8ce')+text(100,67,'How far is it ...?',14)+line(100,82,100,104)+rect(13,106,174,44,'#ded1b1')+text(100,125,'How long does it take',11)+text(100,142,'...?',13)+text(100,179,'距離問法 ≠ 只找minutes',11)])
# Market preference is an explicit name-by-name count, not generated people.
svg(866,[text(100,20,'先逐人辨偏好')+''.join(rect(15,38+i*36,170,28,'#c9ddc1' if i<3 else '#eadac4')+text(100,57+i*36,s,12) for i,s in enumerate(['Jenny：supermarket','Ben：supermarket','Linda：supermarket','Tom：traditional'])),text(100,20,'三條線索指向超市')+''.join(f'<circle cx="35" cy="{62+i*46}" r="8" fill="#91b480"/>'+line(45,62+i*46,65,62+i*46)+text(124,67+i*46,s,11) for i,s in enumerate(['better','more','more convenient'])),text(100,20,'只把符合者放進集合')+''.join(f'<circle cx="{x}" cy="{y}" r="26" fill="#c0d6b3"/>'+text(x,y+4,s,11) for x,y,s in [(49,66,'Jenny'),(143,66,'Ben'),(97,130,'Linda')])+text(100,183,'集合內共3人；Tom不在內',11)])
# Keep units explicit; don't invent exact dates or turn every month into exactly four weeks.
svg(868,[text(100,20,'基準：Ben 每週2次')+rect(28,49,144,105,'#e2e7db')+line(28,80,172,80)+''.join(line(28+20*i,80,28+20*i,154) for i in range(1,7))+text(100,69,'一週示意',12)+''.join(f'<circle cx="{x}" cy="116" r="8" fill="#82a8bb"/>' for x in [69,129])+text(100,181,'不捏造原文沒說的日期',10),text(100,20,'Linda：每週六1次')+rect(28,49,144,105,'#e2e7db')+line(28,80,172,80)+''.join(line(28+20*i,80,28+20*i,154) for i in range(1,7))+text(100,69,'一週示意',12)+'<circle cx="149" cy="116" r="8" fill="#9fb889"/>'+text(100,181,'每週1次 ＜ 每週2次',12),text(100,20,'Tom：每月2次')+rect(28,45,144,114,'#e7dfcd')+''.join(line(28,45+i*28,172,45+i*28) for i in range(1,4))+text(100,69,'一整月',13)+''.join(f'<circle cx="{x}" cy="{y}" r="8" fill="#bf9b64"/>' for x,y in [(68,104),(135,139)])+text(100,181,'兩點只表次數，非真實日期',9)])
def make(n,title,panels,answer,points,words):
 q=json.loads((P/'questions'/f'q-{n}.json').read_text());s={'id':q['id'],'subject':'English','title':title,'art':f'docs/comics/art/q-{n}.'+('png' if n in [862,870] else 'svg'),'layoutVersion':'native-fluid-v6','panels':[{'heading':h,'text':t,'alt':a} for h,t,a in panels],'fourth':{'answer':answer,'points':points},'protectedWords':words,'sourceUrl':'https://chatgpt.com/share/6ae35c92-ac3c-83ee-a1b2-d202f452dd1d','originalMaterialsChecked':True,'rationale':'實看原卷全文四選及所需閱讀材料，依完整句法/文意逐項核答。新圖不沿來源AI圖，不因同頁誤合15與16，35與36才依同文合組。','generationMethod':'new built-in imagegen wordless context + HTML' if n in [862,870] else 'new exact SVG relation/calendar/count diagram + HTML'}
 if n in [862,870]:s['promptPath']=str(P/'comics'/f'q-{n}-prompt.txt')
 Path(f'docs/comics/q-{n}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n');(P/'comics'/f'q-{n}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
make(862,'it回指房間，was配合過去敘事',[
('① 先找被描述的房間','Jessie進房間後驚訝，下一句解釋房間裡充滿玫瑰。圖只是故事情境，沒有新增送花者或任何原文沒說的事件。','新製Jessie推門看到玫瑰房間的情境，未新增送花者或戀愛情節。'),
('② 單數room，用it回指','her room是單數事物，用it作主詞；過去敘事用was，連成it was full of ...，選C。不能只因花很多便把主詞改成they。','新製同一間滿是花瓶玫瑰的房間，精確代名詞由HTML說明。'),
('③ roses在of後，不是這句主詞','many beautiful roses屬於of後的片語內容。be full of是充滿的結構；there was或there were不能直接塞進空格取代it was。','新製玫瑰花瓶近景，以多朵花對比單數房間；不把花當代名詞先行詞。')],
'答案 C：it was',['it → her room，單數。','was配合前文過去敘事。','full of後的roses不決定主詞單複數。'],['Jessie','her room','it was','full of','roses'])
make(864,'兩地距離問How far，別只抓minutes',[
('① from A to B，先看兩地關係','原句問從家到郵局多遠，How far is it from A to B?是本題句型，選B。小圖只表示兩地，不虛構路線或實際公里數。','新製住家與郵局兩端距離關係圖，未另加距離。'),
('② 5分鐘騎車，可描述路程遠近',"It's 5 minutes by bike是以交通時間描述路程。不能見到minutes便一律填How long，仍要看前後完整問句與情境。",'新製自行車與原句5分鐘標籤，沒有編造行車速度或距離。'),
('③ How long通常配交通時間句型','要問花多久，常說How long does it take ...?；How soon問多久後發生，How often問多常，都不合本題兩地距離問法。','新製兩種問句結構對照，不把所有時間回答都限成How long。')],
'答案 B：How far',['地點間距離：How far is it from ... to ...?','騎車5分鐘可用來描述路程。','判整個句型，不只認一個單字。'],['How far','How long','How soon','How often','by bike','minutes'])
make(866,'逐人核對偏好，再數符合者',[
('① 四個人，不是四人都選同一處','Jenny、Ben、Linda偏好超市；Tom比較喜歡傳統市場。名單示意逐人分類，不用生成圖片的人頭數當答案。','新製四名角色到購物偏好的明確對應表，內容可校對。'),
('② 不同說法，也能表達偏好','Jenny的better、Ben的more、Linda的more convenient都是線索。Linda說超市對上班族較方便，不能因沒用like就漏算她。','三條分開的偏好語句線索圖，未把字面說法不同當不喜歡。'),
('③ 只有集合中的三人符合','把Jenny、Ben、Linda放進偏好超市的集合，Tom排除，總共三人，選C。Tom有去超市，不代表他比較喜歡超市。','三個清楚分開、具姓名的圓點集合，精確計數3，不用AI人物數量判題。')],
'答案 C：Three.',['Jenny、Ben、Linda，共三人。','better／more／more convenient都要讀到。','有去超市，不等於比較喜歡超市。'],['Jenny','Ben','Linda','Tom','better','more convenient','Three'])
make(868,'頻率要比期間，Linda和Tom都較少',[
('① 比較基準是Ben每週兩次','先圈Ben的twice a week；後面每一個人都要與這個頻率比。示意日曆兩點只表示次數，不新增他實際購物的星期幾。','一週框中恰兩點，清楚表示Ben每週兩次，沒有虛構具體日期。'),
('② Linda週六去，一般每週一次','on Saturdays表示通常每逢週六去超市，等於本題所需的每週一次，比Ben每週兩次少。因此不能只選Tom。','同一週框中一個週六點，表示Linda比Ben頻率少。'),
('③ Tom是每月兩次，期間不同','Tom的twice a month與Ben的twice a week雖然都有two，但期間不同；Tom也較少。Jenny每週三、四次反而較多，故選D。','月框中兩點只表每月兩次，不冒稱每月剛好四週或特定購物日期。')],
'答案 D：Linda and Tom.',['Ben：每週2次。','Linda：每週1次；Tom：每月2次。','Jenny每週3～4次，不屬於較少者。'],['Linda','Tom','Ben','Jenny','twice a week','twice a month','on Saturdays'])
make(870,'avoid要連原因與後文一起讀',[
('① 太吵，因而避免帶Mary前往','Lucy說超市對Mary太吵，所以avoid taking Mary to supermarkets表示避免帶她去這類嘈雜環境，不是享受或開始去。','新製兩名家人在繁忙超市入口觀察的平靜情境，不替人物貼診斷或畫驚恐失控。'),
('② 避開環境，不是在排斥Mary','avoid在此是避免、避開，對應A To keep away from。圖示兩人一起離開不合適的場所，並不是一人躲開另一個人。','同兩人一起轉向較安靜路徑的新情境，沒有排斥他人或把障礙當危險。'),
('③ 安靜時段，又願意帶她去','後文Lucy要在週三安靜時段帶Mary去購物，支持前面是為避開噪音。avoid後接taking這個V-ing形式，也應一起記住。','新製兩人在較安靜超市自在購物的情境，不用模型寫星期或醫療說明。')],
'答案 A：To keep away from.',['too noisy是避免前往的原因。','安靜時段願意再去，前後文互證。','avoid doing：避免做某事。'],['avoid','Mary','Lucy','To keep away from','taking','V-ing'])
print('5 English comic specs prepared')
