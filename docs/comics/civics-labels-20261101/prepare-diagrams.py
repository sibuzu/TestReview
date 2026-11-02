import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def item(label,tone,**extra):return dict(label=label,tone=tone,**extra)
def diagram(kind,title,items,**extra):return dict(kind=kind,title=title,items=items,**extra)
sets=[item('甲｜全部刑事案件的判決總數','blue'),item('乙｜其中告訴乃論刑事案件的判決數','green')]
values={
'q-891':[
 diagram('nested','甲包含乙：乙是總數的一部分',sets,note='外框是甲，內框是乙；框的面積不代表實際件數。'),
 diagram('flow','題設的減少過程',[
  item('部分告訴乃論案件先調解成功','green'),
  item('依法撤回告訴等程序要件成立','gold'),
  item('這些案件不再進入原先的判決','green')],arrow='符合條件後',note='不是任何案件只要私下和解，就必然免除刑事責任。'),
 diagram('change','下移表示判決件數減少',sets,note='甲、乙各有「原本／減少後」兩個位置。原題未給確切件數，這裡只示意變化方向，不提供虛構數值。')],
'q-893':[
 diagram('bars','原表四類案件的件數',[
  item('甲｜民事案件','blue',value=32),item('乙｜告訴乃論刑事案件','green',value=35),item('丙｜非告訴乃論刑事案件','gold',value=18),item('丁｜行政訴訟案件','purple',value=10)],note='每條長條的名稱、顏色與件數直接對應；條長依原表數值比例繪製。'),
 diagram('sum','本題可聲請鄉鎮市調解的範圍',[
  item('甲｜民事案件','blue',shortLabel='甲',value=32),item('乙｜告訴乃論刑事案件','green',shortLabel='乙',value=35)],note='只加甲與乙；丙、丁不列入本題的67件。'),
 diagram('paths','公訴：看誰向法院起訴',[
  item('乙｜告訴乃論刑事案件','green',detail='須有合法告訴，才可追訴。'),
  item('丙｜非告訴乃論刑事案件','gold',detail='不以被害人告訴為追訴條件。')],arrow='均可能由檢察官依法偵查、起訴',target='法院受理檢察官提起的公訴',note='分類看追訴條件；公訴／自訴則看起訴者。乙不等於自訴，丙也不等於公訴。')]
}
for qid,ds in values.items():
 p=ROOT/f'docs/comics/{qid}.json';s=json.loads(p.read_text())
 for panel,d in zip(s['panels'],ds):panel['diagram']=d
 s.update(generationMethod='native HTML/CSS diagram blocks with selectable Chinese labels, exact bar ratios and explicit arrows',rationale='使用者指出無字圖示無法辨識角色與件數，改用直接標中文的可校對圖表區塊；不要求讀者靠顏色或文件圖示猜意義。原題、答案及詳解文字保持。',editableDiagramScript='docs/comics/civics-labels-20261101/prepare-diagrams.py',visualChecked=False)
 s['diagramReview']={'selectableChineseLabels':True,'noInventedQuestionData':True,'numericBars':'q-893採原表32/35/18/10；q-891原題未給確切數值，只示意減少方向。'}
 for k in ['rootReview','checkedAt','validationFile','visualReview']:s.pop(k,None)
 p.write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
