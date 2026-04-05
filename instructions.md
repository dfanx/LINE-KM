# instructions.md（Project Execution Playbook）

> 用途：這份文件是本專案的「開發憲章」。任何新增/修改功能、修 bug、重構、上線，都必須遵守本文件的 Gate（卡關）規範與交付格式。  
> 原則：小步快跑、可驗收、可回滾、可觀測、可追溯。  
> 禁忌：先寫一堆功能再一起修；沒有驗收標準就宣稱完成；只靠 console 猜問題。

---

## 0. 技術棧（Tech Stack）
（請於規劃書生成後補上）

## 1. 專案目標與範圍（必填）
- **目標（Objective）**：  
- **成功指標（Success Metrics / KPI）**：  
- **不做什麼（Out of Scope）**：  
- **關鍵使用者（Primary Users）**：  
- **關鍵情境（Top 3 Use Cases / Journeys）**：  
  1.  
  2.  
  3.  

---

## 2. 不可變約束（Non-negotiables）
> 這些是「護城河」，避免失控擴張與技術債爆炸。若要變更，必須走「重大變更 Gate」。

- **架構/依賴**
  - 禁止未經評估新增大型依賴（state 管理、ORM、UI framework…）
  - 禁止無理由引入多種同類工具（例如同時用兩套 logger/validator）
- **資料與相容性**
  - 禁止未經評估改 DB schema / public API / 欄位語意
- **資安**
  - 禁止提交 secrets / tokens / private keys
- **品質**
  - 修 bug 必須補 regression test（或最小可重現腳本 + 驗收案例）
- **可回滾**
  - 任何改動都必須有回滾策略（feature flag / revert commit / 版本切回）

---

## 3. Definition of Done（DoD）— 什麼叫「完成」
每一個功能/修正，至少滿足以下條件才算 Done：

- ✅ 有**驗收標準**（Given/When/Then 或清楚的操作與預期結果）
- ✅ 有**最小測試**（unit 或 e2e 擇一；關鍵路徑優先）
- ✅ 有**可觀測性**（log/事件碼/必要的 traceId）
- ✅ 有**回滾策略**
- ✅ 文件有更新（README / RUNBOOK / CHANGELOG 至少一處）

---

## 4. 變更單位（Minimum Verifiable Change, MVC）
> 每次修改只做「一個最小可驗證變更」。避免大爆改。

- 一次 PR / 一次 commit 的理想範圍：
  - 解決 1 個明確問題；或交付 1 個可驗收的小功能
- 若需求很大：
  - 拆成多個 MVC + feature flag 漸進上線
- 禁止：
  - 「順手」重構無關區塊
  - 沒有證據就重寫整段（除非你先做 profiling / log 證據）

---

## 5. Git / 版本 / 分支規範
### 5.1 Branch
- `main`：可上線狀態
- `feat/<topic>`：新功能
- `fix/<topic>`：修 bug
- `chore/<topic>`：雜項、工具、文件

### 5.2 Commit message（必須可讀且可追溯）
建議格式（類 Conventional Commits）：
- `feat(scope): ...`
- `fix(scope): ...`
- `refactor(scope): ...`
- `docs(scope): ...`
- `chore(scope): ...`

### 5.3 Tag / Release（有上線就要有版本）
- Tag：`v0.1.0`、`v0.1.1`…
- Release note：寫到 `log.md` / `CHANGELOG.md`

---

## 6. Logging / 觀測性（必做）
> 目標：遇到問題時，不靠猜；靠證據定位。

### 6.1 結構化 log（最低要求）
每個關鍵事件至少包含：
- `event`：事件名稱（例如 `AUTH_LOGIN_ATTEMPT`）
- `scope`：模組/頁面/服務（例如 `auth`, `checkout`）
- `traceId`：一次操作的串接 id（前端可用 uuid）
- `payload`：必要但不含敏感資訊的關鍵欄位

### 6.2 事件碼 / 錯誤碼（建議）
- `AUTH_401`、`API_TIMEOUT`、`DB_WRITE_FAIL`…
- 錯誤訊息要「可行動」：下一步該查什麼要寫清楚

### 6.3 禁止事項
- 禁止把 token、密碼、完整個資寫入 log
- 禁止只印「出錯了」不附上下文（context）

---

## 7. 測試策略（最低可落地版）
> 不追求覆蓋率，追求「關鍵路徑不崩」。

### 7.1 必須存在的測試
- **關鍵路徑 E2E（至少 2～3 條）**
  - Journey 1：  
  - Journey 2：  
  - Journey 3：  
- **回歸測試（regression）**
  - 每修一個 bug，至少新增一條可防止重犯的測試或腳本

### 7.2 沒時間寫測試怎麼辦？
- 最低限度交付：
  - 「最小可重現腳本」+「驗收步驟」+「回滾策略」
  - 並把「補測試」列入 todo.md 的最高優先序

---

## 8. Debug / Bug 回報格式（必填）
> 你提供的資訊越像「法庭證據」，修復速度越快。

提交 bug 時，請用以下格式：

- **重現步驟（最短 3～5 步）**：
  1.  
  2.  
  3.  
- **預期結果**：  
- **實際結果**：  
- **Console error（請貼文字，不只截圖）**：  
- **Network（請附）**：
  - URL：
  - Method：
  - Status code：
  - Response（節錄，勿含敏感資訊）：
- **發生頻率**：必現 / 偶發（%）
- **環境**：OS / Browser / 版本 / 環境（dev/stage/prod）
- **最近一次發生時間**：

---

## 9. AI Agent 合作規範（Plan Mode Gate）
> AI 不是打字機；AI 是「技術 PM + Tech Lead」。  
> 每次修改前，AI 必須先交付以下內容，通過 Gate 才能動手改碼。

### 9.1 每次改動前必交付（Gate Checklist）
AI 必須輸出：

1) **本次目標（Outcome）**：一句話說清楚  
2) **影響面（Blast Radius）**：會動到哪些模組/路徑/資料  
3) **風險等級（Low/Med/High）** + 理由  
4) **最小變更方案（MVP/MVC）**：最小可驗證交付  
5) **替代方案**：更簡約或更務實的做法（至少 1 個）  
6) **回滾策略**：怎麼回、回到哪個版本/commit/tag  
7) **驗收方式**：要跑哪些測試、怎麼手動驗收  
8) **未處理風險**：本次刻意不做的部分（技術債聲明）

> 若 AI 無法提出替代方案或回滾策略，代表理解不足，必須先補齊再動手。

### 9.2 重大變更 Gate（更嚴格）
以下情況視為重大變更，必須先做「方案評估」再改：
- 改 DB schema / public API
- 引入大型依賴（框架、ORM、state 管理）
- 影響核心 journey
- 需要一次改動 > 3 個模組或跨層（前端+後端+DB）

重大變更必交付：
- 方案 A/B 比較（成本、風險、回滾、工期）
- 風險清單（至少 5 條）與緩解策略
- 分階段上線計畫（feature flag / 漸進 rollout）

---

## 10. 安全性最低標準（上線前 Gate）
上線前必檢查：

- **Secrets**：沒有任何 key/token 在 repo
- **輸入驗證**：所有外部輸入都有 validation
- **權限控管**：最小權限（least privilege）
- **依賴風險**：依賴版本無明顯已知漏洞（至少做一次掃描或檢查）
- **錯誤處理**：不暴露內部堆疊資訊給使用者（prod）

---

## 11. Release / 上線流程（可回滾）
- ✅ 版本標記（tag）
- ✅ 更新 `log.md`（本次改了什麼、為何改）
- ✅ 更新 `README.md`（若使用方式有變）
- ✅ 確認 feature flag（若有）預設策略
- ✅ 回滾演練：至少心理上能說出「出事怎麼回」

---

## 12. 文件與溯源（最小維護成本）
### 12.1 必備文件
- `README.md`：如何跑起來、如何測試、如何部署
- `instructions.md`：本文件
- `todo.md`：下一步工作分解與優先序
- `log.md`：變更紀錄（決策、trade-off、版本）

### 12.2 log.md 每次更新格式（建議）
- 日期：
- 版本：
- 變更摘要（3 點內）：
- 動機與取捨（trade-off）：
- 風險與回滾策略：
- 待辦（如果有）：

---

## 13. 工作節奏（避免「做完才發現方向錯」）
- 每完成 1 個 MVC，就做一次快速回顧：
  - 我們是否更接近 KPI？
  - 這個改動是否引入新複雜度？
  - 有沒有更簡的做法？

---

## 14. 專案初始化（開工前清單）
- [ ] 已完成規劃書（含 DoD / NFR / Out of Scope）
- [ ] 已定義 3 條關鍵 journey
- [ ] Repo 已初始化並推上 GitHub
- [ ] 已建立基本分支策略
- [ ] 已準備 `.env.example`
- [ ] 已建立最小 logging 規格（event/scope/traceId）
- [ ] 已建立至少 2 條關鍵路徑驗收方式（E2E 或手動步驟）

---

## 15. 附錄：驗收標準模板（直接複製）
### 功能驗收（Given/When/Then）
- **Given**：  
- **When**：  
- **Then**：  

### 手動驗收（步驟）
1.  
2.  
3.  
**預期**：  

---

## 16. 附錄：AI 修改輸出格式（強制）
AI 每次提交修改方案時，請使用：

- **Goal**：
- **Scope / Blast Radius**：
- **Risk Level**：
- **MVC Plan（Step-by-step）**：
- **Alternative Option**：
- **Rollback Plan**：
- **Validation（Tests + Manual）**：
- **Notes / Debt**：

---
