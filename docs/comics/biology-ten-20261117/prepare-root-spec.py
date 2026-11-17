"""Per-question local art spec; never attaches or curates shared data."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BATCH = Path(__file__).resolve().parent
CAPTIONS = {
    'q-975': [
        '新製草→兔→狐的概念情境：攝食同時傳遞食物物質與化學能，物種是輔助例子，不是原題新增條件。',
        '落葉經真菌分解、養分回到土壤供植物吸收，示意物質可循環；不表示散失的熱能也循環回植物。',
        '葉片與葉綠體放大圖：光能轉換成有機物中的化學能；生產者不能憑空創造能量。',
        '草、兔、狐及落葉分解者分開呈現；攝食傳遞物質與能量，物質回收與能量散熱須分別看待。'],
    'q-976': [
        '以白鷺作概念例子：巢中出生、左側飛入增加族群，死亡與右側飛出減少。原題未指物種，圖中隻數不是原圖數值。',
        '左側孵化代表出生、右側飛入代表遷入，兩者均增加當地族群；甲乙丙的比較仍依原卷兩線與累積變化判讀。',
        '左側死亡、右側遷出均減少當地族群；丙後減少項仍較多，因此總數繼續下降，不能把兩線水平當總數穩定。',
        '白鷺濕地僅作族群與棲地的概念圖，不提供負荷量數值；原卷乙交會不等於已達長期環境負荷量。'],
    'q-977': [
        '新製海洋剖面：左上甲外海表層、右側乙淺海與丁潮間帶有光；左下丙較深處光照不足。生物及深度不按比例。',
        '白色雙向箭頭由海面向下表示垂直水深；本題200公尺不是水平離岸距離。新製圖無精確比例，數值以原卷為準。',
        '主圖為放大的浮游植物；右下另示附著淺海岩石的大型藻類。放大尺寸不代表兩者實際大小。',
        '新製潮間帶綠藻與潮池；外海浮游植物另以放大框表示。有光與主要生產者種類須分別判斷。'],
    'q-965': [
        '生產者：葉片利用陽光製造有機養分；放大框為葉細胞及葉綠體的教學示意。',
        '分解者：落葉上的真菌菌絲與細菌放大示意；分解有機物，無機養分回到土壤可再利用。',
        '左上鹿取食植物是消費者；右下食腐甲蟲處理遺體屬清除者，也是一類消費者。',
        '基本功能模型：綠色植物提供有機養分，真菌等分解者回收物質；不表示真實生態系只有兩個物種。'],
    'q-966': [
        '蟬以口器吸取植物汁液；植物為生產者，蟬直接取食生產者，是初級消費者。',
        '螳螂以捕捉足取食蟬；蟬是初級消費者，因此螳螂是次級消費者。',
        '黃雀取食螳螂，在本題這條食物鏈中為三級消費者；不代表其所有食物都位於同一階層。',
        '植物→蟬→螳螂→黃雀。箭頭由食物指向取食者，表示物質與能量傳遞；標本圖不按實際大小比例。'],
    'q-967': [
        '白蟻及後腸鞭毛蟲放大示意：白蟻獲得可用養分，鞭毛蟲獲得棲所與食物來源，題幹為互利＋／＋。',
        '冬蟲夏草菌感染蝙蝠蛾幼蟲的教材示意；菌獲養分、幼蟲受害，屬寄生＋／－，菌體從幼蟲頭部附近伸出。',
        '蘭花以氣生根附著樹皮取得支撐，未侵入樹的維管組織取食；本題為片利＋／0。',
        '上方石珊瑚與組織內共生藻、下方螞蟻取得蚜蟲蜜露並提供保護，在本題均依互利＋／＋模型判讀。'],
    'q-968': [
        '新製壽山情境：人與臺灣獼猴爭取同一袋食物，沒有把人當獵物；不是示範餵食。',
        '臺灣獼猴吃遊客留下的食物仍是消費者，吃剩食不會變為分解者。',
        '獼猴攀爬時肌肉活動消耗能量並散熱；尾巴自然下垂，不用尾巴抓握樹枝。',
        '猴吃蘋果，腸絨毛與肌肉另作放大教學圖：部分吸收利用，部分由排遺及散熱離開，不杜撰固定比例。']}
ALTS = {
    'q-975': ['草、取食草的兔與遠處狐狸的類真實食物鏈情境', '植物根系與落葉菌絲的分解回收教材圖', '日照葉片、葉肉與葉綠體放大的科學插畫', '草、兔、狐與落葉分解者分開的自然史標本圖'],
    'q-976': ['白鷺出生、遷入、死亡與遷出的濕地概念插畫，非數值圖', '孵化與飛入濕地的白鷺，示意族群增加來源', '自然死亡與飛離濕地的白鷺，示意族群減少來源', '白鷺族群棲地、食物水域與空間的濕地生態插畫'],
    'q-977': ['明亮海面、淺海與潮間帶及深藍海洋深處的類真實剖面', '垂直白色水深箭頭與海岸剖面', '細膩矽藻及甲藻放大圖對比淺海附著大型藻', '潮間帶綠藻、潮池及浮游植物放大框'],
    'q-965': ['陽光下綠葉、根系及葉綠體放大教材插畫', '真菌菌絲與細菌分解落葉的微觀教學圖', '鹿取食植物與食腐甲蟲處理遺體的分開情境', '植物根系、土壤及真菌分解者的基本功能模型'],
    'q-966': ['真實形態的蟬吸取樹枝汁液', '綠色螳螂以捕捉足捉住蟬', '黃雀叼住螳螂的自然史插畫', '分開繪製植物、蟬、螳螂及黃雀的科學標本圖'],
    'q-967': ['白蟻與後腸鞭毛蟲的科學放大插畫', '冬蟲夏草菌由蝙蝠蛾幼蟲頭部附近長出的土壤剖面', '蘭花氣生根附著樹皮的片利情境', '石珊瑚共生藻與螞蟻蚜蟲的兩個互利情境'],
    'q-968': ['遊客收回食物袋與臺灣獼猴伸手爭食', '臺灣獼猴取食蘋果的類真實插畫', '以四肢攀樹、尾巴自由下垂的臺灣獼猴', '獼猴吃食物、腸絨毛與肌肉放大教材圖']}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('id', choices=CAPTIONS)
    qid = parser.parse_args().id
    spec = json.loads((BATCH/'old-specs'/f'{qid}.json').read_text())
    images = [f'docs/comics/art/{qid}-panel-{i}.png' for i in range(1, 5)]
    for path in images:
        assert (ROOT/path).is_file(), path
    for index, panel in enumerate(spec['panels']):
        panel.pop('diagram', None)
        panel.update(image=images[index], alt=ALTS[qid][index], caption=CAPTIONS[qid][index])
    spec['fourth'].update(image=images[3], alt=ALTS[qid][3], caption=CAPTIONS[qid][3])
    # The fourth caption is also selectable in the summary points in both views.
    spec['fourth']['points'].append(CAPTIONS[qid][3])
    for key in ['nativeArt','nativeLayout','styleReferences','rootReview','producerReview','validationFile','checkedAt','visualReview']:
        spec.pop(key, None)
    spec.update(art=images[0], generationMethod='Four independent built-in image_gen calls; high-quality realistic scientific educational illustrations; exact Chinese in selectable HTML',
                sourceGeneratedArtUsed=False, producerAgent='/root', visualChecked=False,
                scientificArtwork=True, artworkIsNewTeachingIllustration=True,
                rationale='依原題保留已核答案與解說，將舊圖升級為四張細膩類真實生物教材插畫。科學構造與物種關係逐圖核對，精確標示另置HTML，不將插畫當原卷或實拍。',
                artworkGenerationBatch='docs/comics/biology-ten-20261117/root-imagegen-records.json',
                layoutVersion='native-four-images-v7',
                reworkedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                artSHA256=hashlib.sha256((ROOT/images[0]).read_bytes()).hexdigest())
    (ROOT/f'docs/comics/{qid}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
    print(qid, 'local spec ready for isolated QA')

if __name__ == '__main__':
    main()
