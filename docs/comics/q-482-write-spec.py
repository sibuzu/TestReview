from pathlib import Path
import json,hashlib
a=Path('docs/comics/art/q-482.png');d={'id':'q-482','subject':'Chinese','title':'惜別是一層，全詩重在不受賞識的失意','art':str(a),'artMode':'imagegen','layoutVersion':'native-fluid-v6',
'panels':[{'heading':'① 空自歸：反覆等待，卻仍落空','text':'寂寂竟何待、朝朝空自歸，寫一天天等待卻空自歸來的冷清與失望。這個開頭先定下失意的基調，並未交代歲末年終，也不是描寫戰火造成的逃難。','alt':'全新內建詩人獨自返回安靜街巷的失意情境，房舍完整，無戰火、年末節物、考試榜單或具體罷官事件。'},
{'heading':'② 惜與故人違：有不捨，但只是一層','text':'想離去，又捨不得與故人分別，確實有惜別之情。所以 C 有局部線索，卻不能只憑這一句，就概括整首詩；還要接著讀誰相假、知音稀，找反覆出現的主要情緒。','alt':'全新內建詩人與成年舊友相別示意，關切而不誇張哭泣，不把朋友當敵人，也不聲稱是真實歷史肖像。'},
{'heading':'③ 誰相假、知音稀：點出歸隱的原因','text':'掌權者有誰肯賞識、援引自己？了解自己的知音又太少。末尾掩故園扉的歸隱，是不受賞識後的選擇；不能因想隱居，就替原詩加上躲避戰亂的理由。','alt':'全新內建詩人寂寞歸園、輕掩木門的詩境，無戰爭、廢墟、難民或特定帝王拒絕的新增事件。'}],
'fourth':{'answer':'答案 A：無人賞識，暗自悲傷','points':['空自歸、誰相假、知音稀，共同指向失意。','C 抓到惜別的一層，未涵蓋全詩重心。','B 歲末、D 戰火，都缺少詩句依據。']},
'protectedWords':['孟浩然','留別王維','空自歸','誰相假','知音稀','不受賞識','惜別','失意','歲末年終','故人','歸隱','主要情緒','故園扉','隱居','戰亂','朝朝','寂寂','無人賞識','暗自悲傷','惜與故人違'],
'originalChecked':{'images':['site/dist/assets/questions/q-482-source-b253a51f29.jpg'],'visualChecked':True,'answer':'A','notes':'親見25題原卷八句與四項；不改版本寂寂竟何待/只應守寂寞。全詩失意最合A，惜別C為其中一層，歲末/戰火無據。'},
'sourceUrl':'https://share.gemini.google/WVU6ALcogle7','answerCheckedAgainst':'原卷空自歸、當路誰相假、知音世所稀三線索與末聯；原A不變，不補具體仕途事件或年末戰亂。',
'references':[{'title':'教育部重編辭典：留別','url':'https://dict.revised.moe.edu.tw/dictView.jsp?ID=63523&q=1&word=%E7%95%99','supports':'留別詞義與引用當路誰相假/知音世所稀','access':'搜尋摘要已讀；開頁輸出截斷未以全文查證申報，未用異文替換原卷'}],
'rationale':'平靜失意歸來、惜別與歸園三景配合原句，保留C的局部合理線索而指出全詩A重心；不圖像化成沒有依據的兵災、年終或帝王直接拒絕。',
'sourceAIUsed':False,'generationCalls':1,'generationMetadata':'docs/comics/q-482-generation.json','promptFile':'docs/comics/q-482-prompt.txt','manualLineBreaks':False,'diagramChecks':{'answer':'A','partingEmotionPresent':True,'partingIsWholePoem':False,'warEvidenceInPoem':False,'yearEndEvidenceInPoem':False,'specificExamOrImperialRejectionAdded':False,'poemVariantSilentlyChanged':False},'artSHA256':hashlib.sha256(a.read_bytes()).hexdigest()};Path('docs/comics/q-482.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
