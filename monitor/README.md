# WeiRuGo 進度監看

參考 `~/ai/WeiRuGo/monitor/` 的深色監看頁。沿用 Port **8765**，每15秒重新讀取實際檔案。

- 頁面：<http://localhost:8765/>
- 題庫：<http://localhost:8765/site/index.html>
- 健康檢查：`/health`；即時資料：`/api/status`。
- 進度來源：`docs/imports/todo-progress.json`、`more-gpt-progress.json`、`more-gemini-progress.json`。
- 題數與待老師確認題目：`site/dist/data.json`。需核對題幹或答案的項目會自動列出，連結直接開啟本機同一服務的完整題目。
- 其他待確認事項：`monitor/confirmations.json` 的 `requests`，欄位為 `id`、`state: pending`、`title`、`kind`、`questions`，可選 `url`。確認後移至 `resolved`，記錄實際結果與時間。
- 目前工作：`monitor/activity.json`。這是有時間的工作紀錄，不是背景程序心跳；頁面不會自行啟動整理。
- 進度比例：僅以45個 GPT＋58個 Gemini來源的結案數計算。完成、已核實的重複／排除／無法取得來源算結案，部分完成不算。題目總數未知，不把來源比例當成題數完成率。
- 需要使用者確認或重要進度通知時，依使用者指示同步發送到 `https://ntfy.sh/sibuzu_codex`；不要逐次頁面更新都發通知。

啟動及檢查：

```bash
systemctl --user status testreview-monitor.service
systemctl --user restart testreview-monitor.service
python3 -m unittest monitor.test_server -v
```

使用者已授權停止占用同一Port的舊監看頁；切換前服務狀態存於 `previous-services.json`。只切換監看服務，不停止其他專案的製作工作。若要恢復原MV監看頁：

```bash
systemctl --user disable --now testreview-monitor.service
systemctl --user enable --now mv-monitor.service
```

「需要你確認」卡片的「確認 OK」按鈕呼叫 `POST /api/confirm`，將目前卡片的完整內容、題目與原AI連結、確認結果與時間寫入 `resolved`。重複點選不會重複建立紀錄；卡片內容已變更時，必須重新查看後確認。儲存失敗會保留卡片並可重試。也可繼續在Codex對話中回覆。

確認與整理程式共用檔案鎖及原子寫入，避免互相覆寫。有缺漏的題目即使已獲使用者確認，也不會自動冒稱原文、圖或選項已補齊。服務不提供修改題目或執行命令端點；只公開監看頁與題庫 `site/dist` 中的檔案，不開放整個工作目錄。

## 分開取資料與整理

背景取資料顯示在目前工作下方，讀取 `acquisition.json` 與
`gemini-acquisition.json`。來源的取資料結果存於 `docs/acquisition/`；原圖在
`docs/source-pages/`，對話在 `docs/sources/`。取資料成功不代表題目已核對。

- GPT：`site/scripts/prefetch_gpt.py plan --target <授權Chrome分享頁targetId> <來源序號…>`
  產生 `.cache/share-prefetch/commands.jsonl`。把JSONL送入目前已獲允許的
  Chrome bridge連線，由該程式依序捲動、保存對話及附件。同時執行
  `python -u site/scripts/prefetch_gpt.py watch`，接收完成的檔案。
  `merge` 子命令才將取得的原圖合併回整理佇列，保留題目ID與核對狀態。
- Gemini：在可解析 `playwright` 的Node環境執行
  `node site/scripts/prefetch_gemini.cjs <來源序號…>`。使用獨立無頭瀏覽器，
  不占用GPT的授權Chrome。程式保存原尺寸圖片與建立日期，僅寫取資料紀錄。
- 兩個取資料程式可同時執行，並與本地題目整理並行；同一批不重複啟動。
  網頁仍須完成載入才收集附件；未載入的空殼頁面不算成功。
- GPT圖片可能重複或經伺服器重新壓縮；附件數、檔案大小、雜湊是查核線索，
  不能只憑數字差異就斷言缺圖。保留差異，整理時逐張核對。
- `.cache/` 暫存包包含瀏覽器HTML與圖片資料，不加入Git、不由監看頁公開。
