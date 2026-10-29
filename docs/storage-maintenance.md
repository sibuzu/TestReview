# 網站圖片與 Git 減量

單題 HTML 共用部署目錄的圖片，不內嵌 base64。無字教學插畫採原尺寸 WebP quality 88，含字舊 AI 圖採無損 WebP；原卷照片、Logo 與精確 SVG 保持原檔。`curate.py` 與 `attach-comic.py` 使用 `optimized_assets.py`，避免重複發布未壓縮 PNG；無引用的部署圖片先備份再移出。

原始插畫、來源下載、點陣 QA 與含內嵌圖的舊預覽保留在本機 docs，透過 .gitignore 排除 Git。編輯原始插畫需另外搬移這些檔案；Git 部署與網站閱讀使用已版本管理的壓縮資產。

2026-10-29：完整舊 Git 與暫存區備份 `/home/jack/backups/WeiRuGo-size-reduction-20261029/before-rewrite-complete.bundle`；原始 docs 備份同目錄 `local-original-docs/`；移出的部署圖片按 SHA256 保存在 `/home/jack/backups/WeiRuGo-original-assets/`。可透過 WEIRUGO_ORIGINAL_ARCHIVE 改備份位置。備份不在網站部署或遠端 Git 內。

遠端以最後已發布版本為底精簡快照；被撤回的兩個 commit 與較新的題目製作仍保留本機未提交。舊 clone 不能沿用舊 main 直接 push，請另存未提交修改後重新 clone，避免把大歷史推回遠端。
