# CLAUDE.md — AI Agent 學習筆記

> 給 AI 助手（Claude Code、Codex 等）看的專案規則。動手新增或修改任何內容之前，請先讀完這份文件。

## 1. 專案目的
這是一個個人學習筆記網站，把「AI Agent 與設計模式」的課程內容整理成**可回頭查的小頁面**。
- 讀者：未來的我，以及想快速弄懂 Agent 概念的同學。
- 目標：每頁一個主題，**先講是什麼，再講怎麼運作，最後用例子與重點收尾**。
- 這**不是**課本抄寫，是整理後的筆記：用自己的話寫，保留關鍵定義與例子。

## 2. 技術限制（不要擅自改變）
- **純靜態網站**：只有 HTML + CSS，**沒有建置步驟、沒有框架、沒有 npm**。
- 不使用 JavaScript，除非使用者明確要求。
- 不引入外部 CDN、字型或圖片；所有樣式都放在 `assets/style.css`。
- 部署：GitHub Pages，從 `main` 分支根目錄發佈。根目錄的 `.nojekyll` 不要刪。
- 所有連結用**相對路徑**（Pages 會放在子路徑下，不能用 `/` 開頭）。

## 3. 檔案結構與命名
```
index.html            首頁（卡片列表）
pages/<slug>.html     每個主題一頁
assets/style.css      唯一的樣式檔
templates/page.html   新頁面模板（複製它，不要從別頁複製）
scripts/check.py      規則檢查腳本
CLAUDE.md             本文件
```
- 頁面檔名 `<slug>`：**小寫英文＋數字＋連字號**（kebab-case），例如 `tool-use.html`。不可有中文、空白、底線、大寫。
- 頁面一律放 `pages/`；首頁只有根目錄的 `index.html`。
- 不要新增其他資料夾，除非使用者要求。

## 4. 頁面格式（每一頁都要遵守）
以 `templates/page.html` 為準，必備項目：
1. `<html lang="zh-Hant">`，`<meta charset>` 與 viewport。
2. `<title>`：`頁面標題 | AI Agent 學習筆記`（**結尾固定**）。
3. `<meta name="description">`：一句話摘要，約 40～80 字（檢查腳本接受 30～100 字）。
4. 引用 `../assets/style.css`。
5. 頁首導覽（品牌連結＋「首頁」＋「四大設計模式」）。
6. 內容順序：`tag` 分類（見下方「分類」）→ **唯一一個 `<h1>`** → `p.lead` 導言 → 若干 `<h2>` 小節 → `div.note` 重點 → `<h2>來源</h2>`。
7. **「來源」章節必填**，至少一筆（課程教材、文件或連結）。沒有來源就不要寫那段內容。
8. 頁尾與回首頁連結。

### 分類（`<span class="tag">`，只能二選一）
| tag | 用在 | 首頁卡片放進 |
|---|---|---|
| `概念` | 解釋一個觀念或名詞（例如 RAG、Agent 定義） | `<!-- CONCEPTS:START/END -->` |
| `模式` | Agent 的設計模式（Reflection、Tool Use…） | `<!-- PATTERNS:START/END -->` |

`pages/agent-patterns.html` 是總覽頁，固定放在首頁「從這裡開始」，不放進上面兩個區塊。
要新增第三種分類時，先改 `scripts/check.py` 的 `SECTIONS`、`index.html` 與本表，再用它。

### 可用的版面元件（只用這些，不自創 class）
| 元件 | 用途 |
|---|---|
| `<div class="note"><b>重點：</b>…</div>` | 一句話記起來（每頁至少一個） |
| `<div class="warn"><b>備註：</b>…</div>` | 資料不足、限制、未確認之處 |
| `<div class="flow"><span>A</span><i>→</i><span>B</span></div>` | 流程 |
| `<table>` | 比較 |
| `<pre><code>` | 程式碼／JSON（要跳脫 `<` `>` 成 `&lt;` `&gt;`） |
| `.cards` / `.card` | 只用在首頁 |

## 5. 寫作規則
- 語言：**繁體中文**，專有名詞保留英文（Tool Use、LLM、JSON）。
- 語氣：簡潔、直接，一段 1～3 句；能用條列就不要寫長段落。
- 事實必須來自「來源」：**不要編造數字、日期、人名、引言或連結**。不確定就寫在 `warn` 裡說明，或不寫。
- **整理 vs. 推論：** 重新組織、換句話說、歸納來源已有的內容，可以寫；來源沒有的推論或延伸，必須放進 `warn`，並標明「這是我的整理，不是教材原文」。來源沒提供的細節（做法、數據、例子）不要補。
- 引用教材的程式或原文，只摘關鍵片段並註明來源；不整段複製。
- 不要在頁面裡留下模板的【佔位文字】。

## 6. 新增一頁的步驟（AI 請照順序做）
1. 複製 `templates/page.html` 到 `pages/<kebab-case-slug>.html`。
2. 替換所有【…】佔位文字；更新 `<title>`、`description`、`<h1>`、導言、內容、來源。
3. 依頁面的 `tag`，在 `index.html` 對應區塊（`CONCEPTS` 或 `PATTERNS` 的 START/END 標記**之間**）加一張 `.card`：
   `<a class="card" href="pages/<slug>.html"><b>標題</b><small>一句話說明。</small></a>`
4. 若與其他頁相關，用相對連結互相連（同在 `pages/` 內寫 `other.html`，從首頁寫 `pages/other.html`）。
5. 執行 `python3 scripts/check.py`，**必須顯示「✅ 檢查通過」**才算完成。
6. 更新本文件第 10 節的「目前頁面」表（新增一列）。
7. 回報給使用者：新增了哪個檔案、首頁加了什麼、檢查結果。

## 7. 修改既有內容
- 只改使用者要求的部分，不順手重排或改寫其他頁。
- 改樣式前先確認會不會影響全部頁面；樣式只改 `assets/style.css`，並保留深色模式（`prefers-color-scheme`）。
- 刪除頁面時，同步刪掉 `index.html` 的卡片與其他頁指向它的連結。

## 8. 完成前自我檢查清單
- [ ] `python3 scripts/check.py` 通過
- [ ] 若有瀏覽器工具：用 `python3 -m http.server` 開啟，確認版面、手機寬度不爆版；沒有就在回報中註明「未做視覺檢查」
- [ ] 所有連結可點、沒有壞連結
- [ ] 每個事實都有來源，沒有編造內容
- [ ] 沒有留下佔位文字或暫時檔

## 9. 不要做的事
- 不要引入框架、建置工具、外部資源。
- 不要把金鑰、個資、私人資料放進任何檔案。
- 不要自行 push 或改動 GitHub 設定，除非使用者要求。

## 10. 目前頁面
| 檔案 | 主題 |
|---|---|
| `pages/agent-patterns.html` | 四個設計模式總覽 |
| `pages/reflection.html` | Reflection |
| `pages/tool-use.html` | Tool Use（含作業實例） |
| `pages/planning.html` | Planning |
| `pages/rag.html` | RAG（概念） |
| `pages/multiagent.html` | Multiagent Collaboration |

可擴充的下一批主題（尚未建立）：Prompt／Context Engineering、MCP 與 A2A。新增後請更新這張表。
