# 新 GPT 來源49／50交稿與機械加入

本批只處理使用者指定的兩個新網址，既有695題面／757原題不改，已排除的81道AI延伸不恢復。

- 來源49：`src-more-049`，Agent2，目錄`new-gpt-20261029-a`；每個原卷題／子題依序預留`q-850、852、854…`。
- 來源50：`src-more-050`，Agent3，目錄`new-gpt-20261029-b`；每個原卷題／子題依序預留`q-851、853、855…`。
- 題組保留每子永久ID、全文、四選項、答案、詳解、必要原圖及自身圖解，以最早ID作父題；沿用現有groupQuestions/catalog，不另建別名機制。
- 原卷／答案核對、新四格與自驗由交稿代理完成。Agent1只作基本去重、資產複製、資料完整性及機械加入，不重做解題、紅字或版面驗收。

每路沿用自己的穩定`manifest.json`：各件列`id、questionPath、specPath`（題組可列`childSpecs`）、本機資產映射、`qaReport`與`status: ready`；`source.json`記來源日期、全文／封存路徑和原卷附件。已有同等內容的格式可直接交，不為欄位名稱重工。定稿後不覆寫，修訂另附檔通知。

入庫沿用既有additional-sources、additional-questions、complete-questions、attach-comic與curate。每個真正新製圖解才記一個原漫畫整合事件，沿用6／20；技術題組不冒稱新畫。完成本批不足20仍正常commit all／push。

公開分享原卷仍需實際可讀。整批原圖不可讀時暫停該路轉錄與製圖，由root協調Chrome允許；AI文字比對僅列候選，不當成原卷或判答證據。
