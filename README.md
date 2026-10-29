# WeiRuGo

繁體中文的國中錯題網站，依 `todo/todo.md` 及 `todo/more_gpt.md` 的分享連結持續整理。

```sh
npm run dev --prefix site
# http://127.0.0.1:4173
npm test --prefix site
python3 site/scripts/curate.py
```

VS Code Live Server 可直接開根目錄 `index.html`，會保留題目網址並轉到 `site/dist/index.html`。網站不需建置；請透過 HTTP 開啟。

單題閱讀頁與主網站共用 `assets/` 圖片，不再把圖片重複內嵌到每份 HTML。原卷照片保留原尺寸；無字教學插畫使用原尺寸 WebP，含文字的舊 AI 解說圖使用無損 WebP。重新整理資料時會沿用 `site/asset-map.json`，避免 PNG 與重複圖檔再進入部署目錄。

原始插畫、下載證據與點陣 QA 檔保留在本機，排除於 Git；2026-10-29 減量前備份在 `/home/jack/backups/WeiRuGo-size-reduction-20261029/`，從部署目錄移出的圖片在 `/home/jack/backups/WeiRuGo-original-assets/`。換機若要繼續編輯舊插畫，需另行搬移這些原始檔；瀏覽網站及 Git 部署不需要它們。可用 `WEIRUGO_ORIGINAL_ARCHIVE` 指定新的原圖備份位置。

- 預設列表模式，可切換卡片；依科目、已作／未作、冊次、章節與關鍵字篩選，日期或題名排序。
- 題目直接取代主區域，網址如 `index.html#question/q-024`。上方有麵包屑及「← 回上頁」，返回保留列表搜尋、篩選與捲動位置。
- 題幹、選項與必要閱讀材料或圖表先顯示；原卷作答、答案、逐項解析、詳細說明與本題原圖預設一起收合。
- 列表頁只保留標題、搜尋、篩選與題目；搜尋列到第一題的間距與題目間相同。
- 進入題目時，側欄列出目前科目、題數與可直接換題的標題；沿用進入前的篩選與排序，直接開啟網址則列該科目全部題目。
- 題目右上角以方框勾選切換已作／未作，以☆／★切換收藏，以?切換疑義標記；列表只留收藏星號。桌面側欄可獨立捲動，手機題目導覽可捲動。
- 沒有筆記、複習進度、題目編輯或手動新增功能。瀏覽器 localStorage 保存收藏、疑義及已作題目ID與尚待同步的ID／布林變更，不保存題目內容。標記鍵分別為 `test-review:favorites:v1`、`test-review:doubts:v1`、`test-review:answered:v1`；舊版資料只遷移收藏，再移除舊資料。
- 已移除備份及「我」頭像。收藏、疑義與已作共用雲端同步；題目開啟或展開答案不會自動改成已作。老師可從「有疑義的題目」清單集中檢視。

## 題目整理

每題只指定一個主要科目。出版社只供對應章節使用（國文南一、英文翰林、數學康軒、自然翰林、社會康軒），網頁不標示出版社；冊次或章節無可靠依據就歸綜合。英文作文依指定保留於英文綜合。

日期取可確認的首次出題日期，重貼或後續更正保留較早日期。原 AI 解答只供追查，必須對照原卷、全部選項與必要圖文。待處理舊題標「（待更新）」；待核對題目的頁面直接列出需確認的項目，能讀取的原始輸入也會原樣保留，可按前後連結依序核對。「待核對原題」是整理期間的暫態，不是使用者複習狀態。

來源證據在 `docs/sources/`，原圖在 `docs/source-pages/`；完成的舊題覆寫在 `docs/complete-questions/`，新增資料在 `docs/additional-questions.json`、`docs/additional-sources.json`。`curate.py` 產生 `site/dist/data.json` 及已核對題目的單頁閱讀版。

優先整理 `todo/todo.md` 的9個原始來源，再依次處理新增來源。`docs/imports/todo-progress.json`、`docs/imports/more-gpt-progress.json` 記錄原始與新增來源的處理狀態、原圖及跳過原因。只有 Notion 的來源不加入網站。若整批原圖都無法讀取，先暫停向使用者確認；個別缺圖則記錄並跳過。裁切後須實際檢視成品是否對應本題。

## Netlify

題庫閱讀仍可直接提供 `site/dist` 靜態檔案。雲端標記需要同時部署 `netlify/functions`，因此請以**完整Git專案**部署；只拖曳 `site/dist` 不會安裝後端功能。不產出ZIP，也不代為發布。題目使用hash網址。

設定已在根目錄 `netlify.toml`：Base directory為專案根目錄、Publish directory為`site/dist`、Functions directory為`netlify/functions`，Node.js 22，無需另外的build command。Netlify會安裝根目錄`package.json`與鎖定檔的依賴並打包Functions。

### 單一使用者雲端標記

- 正式網站：<https://weirugo.sibuzu.com>。沒有登入，所有裝置與訪客共用同一份收藏、疑義及已作標記。
- `/.netlify/functions/marks`使用Netlify site-wide Blobs保存資料，重新部署不會清掉標記。每題的收藏、疑義及已作各自寫入，避免兩部裝置更新不同標記時互相覆蓋。
- 初次同步會合併尚未上雲端的本機標記；雲端已取消的標記不會被另一台裝置的舊快取重新打開。離線變更先排入`test-review:mark-outbox:v1`，連線恢復後重試。同一標記若在兩台裝置修改，以最後成功寫入的操作為準。
- 開啟頁面、回到前景、恢復網路時同步；前景每60秒再讀取一次。也可點右上角同步狀態立即重試。同步不收合目前展開的答案。
- 新的已作標記需同時部署新版前端與Functions。舊後端未提供answered能力時，已作先留在本機待同步，收藏及疑義照常同步；新版部署後自動補傳。
- 指定的monitor（monitor.sibuzu.com、localhost／127.0.0.1:8765）與Live Server（localhost／127.0.0.1:5500、4173）會連到weirugo.sibuzu.com的同一個雲端端點；正式網站與Netlify預覽則使用自己的Functions端點。後端只允許這些明確指定的跨來源請求。
- 跨網址同步需同時更新正式網站的Functions（CORS）與前端。已開啟的舊頁面在更新後重新整理一次，才會載入新同步程式；原有本機收藏會自動合併。不清除瀏覽器資料，以免遺失尚待上傳的標記。
- 同步服務尚未就緒或網路不可用時，保留本機標記並顯示待同步；狀態顯示「標記已同步雲端」才代表該次同步完成。
- Blobs所需的服務憑證由Netlify Functions執行環境提供，不放入前端。參考[Netlify Blobs文件](https://docs.netlify.com/build/data-and-storage/netlify-blobs/)。

```sh
npm ci
npm test
```

目前已完成本機與模擬後端測試；須在完整專案部署到Netlify後，才能驗證正式雲端端點。

