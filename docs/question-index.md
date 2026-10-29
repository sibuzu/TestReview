# 本機題庫索引

`site/scripts/question_index.py` 使用 Python 內建 SQLite＋FTS5，整理正式題目、待整合稿、共同文章、題組小題、原 AI 來源與網址別名、漫畫狀態及確認紀錄。這是可刪除重建的搜尋索引，原始資料仍以 `site/dist/data.json`、來源紀錄與各來源稿件為準。

索引預設存於 `.cache/question-index.sqlite3`；`.cache/` 已被 Git 排除，Netlify 的發布目錄仍為 `site/dist`。不改網站讀取方式、不新增 Netlify build command、Function 或雲端資料庫，也不讀寫使用者的收藏／已作／疑義標記。

## 常用指令

在專案根目錄執行：

```bash
# 手動重建／查看收錄統計
python site/scripts/question_index.py build
python site/scripts/question_index.py status

# 正式題庫搜尋；短詞也可找，空白分開的詞需同時出現
python site/scripts/question_index.py search '康熙 義民'
python site/scripts/question_index.py search 'bicycle riding' --subject English

# 同時尋找正式題目及本批新來源草稿
python site/scripts/question_index.py search '朱一貴' --kind all
python site/scripts/question_index.py search '鰻苗' --kind draft

# 舊題號會沿別名解析；列出完整材料、答案、解說與原 AI 連結
python site/scripts/question_index.py show q-821

# 由網址／標題／封存對話文字尋找來源（即使尚未拆題）
python site/scripts/question_index.py source PG8U2uUXtGhv
python site/scripts/question_index.py source '海岸侵蝕'

# 查某分享連結已對應哪些題目，支援已保存的網址別名
python site/scripts/question_index.py search 'https://share.gemini.google/PG8U2uUXtGhv'

# 新稿查重；題組稿會逐小題輸出
python site/scripts/question_index.py candidates docs/imports/new-gemini/gemini061/questions/page01-q04.json
python site/scripts/question_index.py candidates docs/imports/new-gemini/gemini060/group-p37-q02-q03.json
```

每次查詢會比較來源檔案清單、大小與修改時間，資料有更新便重建後再查。不依賴人工記得刷新。若整理代理恰在寫檔中、來源 JSON 不完整或重建期間資料改變，會保留上一份完整索引並回報失敗；等該次寫入完成後重試，不會覆寫正式題庫。另以 SQLite integrity／foreign-key checks 驗證新索引，成功後才原子替換。

## 查重界線

- 題幹與選項、共同材料分開建索引與指紋；同文章但不同小題列於 `sharedMaterialNotDuplicate`，不當成重複題刪除。
- `exactTextCandidates` 只表示文字相同或題幹相同；必要圖形、表格、條件及完整選項仍需核對，不自動合併或排除。
- `similarStems` 只比較題幹及題內選項，不讓長篇共用文章拉高相似度。
- 同一來源的新舊分享 URL 保留多對多關係；不同 URL 不保證不同題，同 URL 也不是內容比對證據。
- 已發布題組保留各小題草稿與同一正式題號的對應；舊題號依 `docs/question-aliases.json` 解析，不重排題號。題組整筆入庫的收據也會對應到每一個小題，不誤列成仍未入庫。
- 使用者已取消的後續來源及明確略過的小題不放進活躍草稿索引；原件仍保留本機歷史，不因搜尋或重建而自動重新收入。
- 原卷辨讀、紅字訂正核對與解說審查仍由原分工執行，索引不代表已通過內容驗證。

資料表包括 `records`、`passages`、`sources`、`source_urls`、`record_sources`、`question_groups`、`group_members`、`aliases`、`confirmations` 及全文索引。圖檔只記路徑，不把圖片放進資料庫。原始 PNG／原卷的減量與保存流程維持不變。

驗證：

```bash
python -m unittest discover -s site/scripts -p test_question_index.py
```

調整索引 schema 或正規化方式時，提高程式的 `VERSION`，或執行一次 `build`，使舊索引重建。
