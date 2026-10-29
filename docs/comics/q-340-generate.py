from pathlib import Path
import json,hashlib,math
from datetime import datetime
from zoneinfo import ZoneInfo
s=['<svg xmlns="http://www.w3.org/2000/svg" width="540" height="180" viewBox="0 0 540 180"><defs><marker id="a" markerWidth="5" markerHeight="5" refX="4" refY="2.5" orient="auto"><path d="M0 0L5 2.5L0 5Z" fill="#598f91"/></marker></defs>']
for i in range(3):
 o=i*180
 def t(x,y,z,n=11,c='#335856'):s.append(f'<text x="{o+x}" y="{y}" text-anchor="middle" font-size="{n}" fill="{c}">{z}</text>')
 def r(x,y,w,h,c):s.append(f'<rect x="{o+x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{c}"/>')
 s.append(f'<rect x="{o}" width="180" height="180" fill="{["#f7efe2","#edf2e8","#eaf0f4"][i]}"/><g font-family="sans-serif">')
 if i==0:
  t(90,19,'埃及當地：2021/3/23',10)
  r(12,35,156,42,'#e1dfd2');t(90,52,'約 07:40',13);t(90,69,'貨輪擱淺：事件背景',10)
  r(12,99,156,45,'#cbdeb9');t(90,118,'08:00',16);t(90,136,'宣布消息：本題換算起點',9)
  t(90,171,'別拿 07:40 當作公告時間',9)
 elif i==1:
  t(90,19,'當日兩地的 UTC 時差',10)
  for j,(a,b) in enumerate([('UTC+0','06:00'),('埃及 UTC+2','08:00'),('臺灣 UTC+8','14:00')]):
   y=34+j*32;r(8,y,164,27,'#d8e5ce');t(60,y+18,a,10);t(139,y+19,b,13)
  t(90,155,'8 − 2 = 6 小時',15);t(90,175,'上面三列是同一時刻',9)
 elif i==2:
  t(90,19,'同時：埃及 8 時，臺灣 14 時',9)
  for cx,hour,name in [(43,8,'埃及'),(137,14,'臺灣')]:
   t(cx,48,name,11);s.append(f'<g data-clock-hour="{hour}" data-center="{o+cx},88"><circle cx="{o+cx}" cy="88" r="27" fill="#fffef7" stroke="#668e8c" stroke-width="2"/>')
   for n in range(12):
    rad=n*math.pi/6;x1=o+cx+23*math.sin(rad);y1=88-23*math.cos(rad);x2=o+cx+25*math.sin(rad);y2=88-25*math.cos(rad);s.append(f'<path d="M{x1:.4f} {y1:.4f}L{x2:.4f} {y2:.4f}" stroke="#9ab0a8"/>')
   rad=(hour%12)*math.pi/6;x=o+cx+15*math.sin(rad);y=88-15*math.cos(rad)
   s.append(f'<path data-hand="minute" d="M{o+cx} 88V67" stroke="#335856" stroke-width="2"/><path data-hand="hour" d="M{o+cx} 88L{x:.4f} {y:.4f}" stroke="#b48457" stroke-width="3"/><circle cx="{o+cx}" cy="88" r="2" fill="#335856"/></g>')
   t(cx,135,f'{hour:02}:00',14)
  t(90,78,'+6',10);s.append(f'<path d="M{o+74} 90H{o+106}" stroke="#598f91" stroke-width="2" marker-end="url(#a)"/>')
  t(90,162,'08:00 + 6 小時 = 14:00',12);t(90,178,'同日，下午二時',9)
 s.append('</g>')
s.append('</svg>');a=Path('docs/comics/art/q-340.svg');a.write_text(''.join(s))
x=datetime(2021,3,23,8,0,tzinfo=ZoneInfo('Africa/Cairo'));y=x.astimezone(ZoneInfo('Asia/Taipei'));assert y.hour==14 and y.minute==0
d={'id':'q-340','subject':'Geography','title':'用宣布消息的8時，換算同時臺灣14時','art':str(a),'artMode':'deterministic-svg','generatorFile':'docs/comics/q-340-generate.py','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 換算8時宣布，不是約7時40分擱淺','text':'題幹先交代擱淺背景，後來才問官方在早上8時宣布消息時，臺灣是幾點。真正要換算的起點是08:00，不要把前文約07:40的事件時間帶入。','alt':'新精確事件卡將約07:40擱淺和08:00宣布分開，突出後者，日期為原卷2021/3/23。'},
{'heading':'② 依題目日期，臺灣比埃及快6小時','text':'2021年3月23日，埃及是UTC+2，臺灣是UTC+8；兩地差8−2＝6小時。臺灣的鐘錶比埃及快6小時，所以從埃及換到臺灣，要在埃及的鐘點加6小時。','alt':'新精確同時刻表UTC06:00、埃及08:00、臺灣14:00與UTC+0/+2/+8，計算6小時差；不使用現在日期的夏令規則。'},
{'heading':'③ 08:00加6小時，就是14:00','text':'埃及08:00＋6小時＝臺灣14:00，也就是同一天下午2時，選B。題目問各地的鐘錶時間，不是用31.23°E直接計算地方太陽時，也不用把兩地時差相加。','alt':'新精確兩鐘埃及8點和臺灣14點，分針皆12方向；時針8與2，表示同時刻上午8和下午2。'}],
'fourth':{'answer':'答案 B：14:00','points':['取宣布消息的08:00作為換算起點。','當日臺灣比埃及快6小時。','08:00＋6小時＝同日14:00。']},
'protectedWords':['08:00','07:40','14:00','UTC+2','UTC+8','2021年3月23日','6小時','31.23°E','地方太陽時'],
'originalChecked':{'images':['site/dist/assets/questions/q-340-source-973279ca26.jpg'],'visualChecked':True,'answer':'B','notes':'親見原13題2021/3/23、約7時40分、8:00公告與四項12/14/16/18；紅B黑D分開，不將擱淺背景當公告起點。'},
'sourceUrl':'https://chatgpt.com/share/6ae05208-3ffc-83ee-be7e-99cc4705ab6d','answerCheckedAgainst':'原卷B和獨立zoneinfo歷史日期轉換符合2021-03-23T08:00+02至同日14:00+08；IANA Cairo Egypt規則2014後至2023復行前、Taipei UTC+8源檔實讀。',
'references':[{'title':'IANA tzdb Africa','url':'https://data.iana.org/time-zones/tzdb/africa','supports':'Africa/Cairo UTC+2與Egypt歷年規則；本題2021日期','access':'web及Python原檔Egypt2014/2023規則行實讀'}, {'title':'IANA tzdb Asia','url':'https://data.iana.org/time-zones/tzdb/asia','supports':'Asia/Taipei時區記錄','access':'web全文與Python實讀Zone Asia/Taipei段，zoneinfo獨立換算'}],
'rationale':'精確時刻表與時鐘比人物或貨船圖直接，可同時排除誤抓7:40、時差反加及12小時鐘讀法；不畫不按刻度的全球經線或地方太陽時計算。',
'sourceAIUsed':False,'generationCalls':0,'manualLineBreaks':False,'diagramChecks':{'date':'2021-03-23','from':x.isoformat(),'to':y.isoformat(),'offsetDifferenceHours':6,'sameDate':x.date()==y.date(),'hourHands':[8,14],'minuteHands':[0,0]},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()}
Path('docs/comics/q-340.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
