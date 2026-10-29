from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-506.png');d={'id':'q-506','subject':'Chinese','title':'逐聯定位冬夜、見聞、戰亂與懷古','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 歲暮、霜雪、寒宵：是冬夜','text':'首聯由一年將盡、白晝變短，寫到霜雪初停的寒夜。這些線索指向冬季，A說秋夜不合。霽是雨雪停後轉晴，插畫用已停雪的清寒夜景，不是正在春花下賞景。','alt':'全新內建文學概念唐裝孤客立於河邊亭閣冬夜，地上霜雪、裸枝、清空，沒有秋葉春花或仍在暴雪。'},
{'heading':'② 鼓角與星河：同一夜的所聞所見','text':'五更鼓角是聽到的聲音，三峽星河影動搖是看到的水中星影。次聯將聽覺與視覺放在一起，沒有敘述詩人從一地移到另一地，因此B的空間遷移不合。','alt':'全新內建夜間江面星影與遠處古代守更鼓角來源同景，不畫詩人旅行或作精確星座圖。'},
{'heading':'③ 野哭、戰伐：不是隱居的閒趣','text':'頸聯由哭聲、戰亂想到百姓的痛苦；夷歌與漁樵聲放在這樣的背景下，也不能整聯讀成悠閒山林生活。因此C錯。插畫只輔助理解戰亂感受，不指稱原詩記載某場具體戰役。','alt':'全新內建匿名成人村民戶外垂首悲傷，近水小屋和漁舟背景，無血腥傷亡、無開心野餐，不冒充特定戰役實錄。'}],
'fourth':{'answer':'答案 D：兩廟背景引出末聯的懷古感慨','points':['臥龍指諸葛亮；躍馬指公孫述。','兩廟是傳統背景注解，詩句本身寫古人終歸黃土。','由古跡懷古而感寂寥，不是兩位古人剛在詩人身旁去世。']},
'protectedWords':['歲暮','霜雪','寒宵','五更鼓角','三峽星河','影動搖','所聞所見','空間遷移','野哭','戰伐','夷歌','漁樵','臥龍','諸葛亮','躍馬','公孫述','終歸黃土','懷古感慨'],
'originalChecked':{'images':['site/dist/assets/questions/q-506-reading-source-2a2b46768d.jpg','site/dist/assets/questions/q-506-notes-source-7383ac369b.jpg','site/dist/assets/questions/q-506-source-561bb03b86.jpg'],'visualChecked':True,'answer':'D','notes':'八句原詩/原註臥龍諸葛亮躍馬公孫述及36四項親見；沿既有D，區分原詩語句與兩廟背景注解，不將古人當同代剛逝。'},
'sourceUrl':'https://share.gemini.google/PayZ1lfF9trh','answerCheckedAgainst':'原詩逐聯與原題四概括獨立排A冬非秋/B見聞非遷移/C野哭非閒趣，沿原D；澳門官方公開教案C137課堂小結同列兩廟背景解讀。',
'references':[{'title':'澳門教育暨青年發展局公開教案C137：閣夜','url':'https://mirror1.dsedj.gov.mo/tplan/2018/plan/C137.pdf','supports':'冬夜/頷聯夜中所聞所見/頸聯悲情/末聯武侯白帝兩廟背景','access':'官方搜尋完整課堂小結節錄已讀，PDF實開逾時/本機TLS鏈失敗，未冒稱全文讀取；不同www入口返回HTML不是PDF，不採用'}],
'rationale':'前三格各核一個錯誤概括，第4格用可校文字釐清D兩廟的背景與兩古人終黃土，避免AI杜撰精確廟貌或古人與杜甫會面。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-506-generation.json','promptFile':'docs/comics/q-506-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'D','season':'winter','clearedSnowNotActiveBlizzard':True,'secondCoupletSpatialJourney':False,'thirdCoupletLeisure':False,'templesAreBackgroundAnnotation':True,'ancientFiguresAliveWithTangPoet':False,'specificBattleInvented':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-506.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
