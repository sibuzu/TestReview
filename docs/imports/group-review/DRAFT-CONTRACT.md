# 題組完整合稿（原卷錯題，AI延伸已排除）

原子領取：`python -m monitor.group_queue claim-merge --agent /root/comic_lane_2`（或lane_3）。
全部候選已核完；root已報告45組／107筆原題及各科，才開啟合稿。

每組獨立寫入 `docs/imports/group-review/drafts/<group-id>/`，不改共享題庫、qid、來源進度或現有正式檔。

## question.json

- 取目前 `site/dist/data.json` 最新原題作快照，保留最早數字qid作parent；題組科目採已核review的代表科目。
- 新增 `groupQuestions`：依原卷順序列出每個子題的**完整原物件**，包括id/sourceId/subject/date/addedAt/passage/tables/questionFigures/question/所有選項/answer/correctOption/explanation/optionAnalysis/studentAnswer/trap/verificationNote/images/explanationFigures/teachingComic/protectedWords。不得用摘要取代，不按art hash刪任何子漫畫。
- 每子可另加 `originalQuestionNumber`；以已核原卷號為準。最早qid與卷面順序可能不同（如153是原第2項，471才是原第1項）。
- parent的passage/tables/questionFigures放已核共同材料，必須取自現有可核內容。子物件的同文照留，由renderer避免重複展示；各子特定材料或附圖不得丟失。
- parent title用清楚的原卷題組名稱。date取子題最早可確認日期，dateLabel沿相應紀錄；addedAt取最早加入日，subject採代表科目，sourceId沿保留原題或代表原題的有效來源。
- 為搜尋與舊版相容，parent question/answer/explanation合列各子原文（帶原題號／標題），不新解題、不變更答案。parent optionAnalysis可清空避免誤當全組同一四選項。
- parent images及explanationFigures保留各子聯集；parent teachingComic沿保留qid既有漫畫作舊版相容。新renderer顯示所有子漫畫一次，不能只留下parent一張。
- 不重新製圖，不採來源AI圖，不把AI延伸重新收入，不改老師已確認的內容。若有新矛盾，隔離報root，不自行訂正。

## manifest.json

必填：`questionIds`（本組全部baseline IDs）、`retainId`、`displayOrder`、`draftPath`（question.json相對repo路徑）、`childCoverage`（完整IDs陣列）、`reviewReport`、`childSnapshots`（每子原物件的SHA256與來源）、`checks`（逐子原題／選項／答案／解說／圖／漫畫未損）。

交稿：`python -m monitor.group_queue stage --agent <agent> --group <group-id> --manifest <manifest-path>`。

交稿後立即領下一組。Agent 1只接ready完整稿做去重、技術整合、相容與頁面驗收；root正在完成顯示／雲端相容，尚未放行前不要自行發布或改正式資料。
