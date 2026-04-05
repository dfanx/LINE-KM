# 🚀 AI 協作開發規格說明書（通用版 v2.0）

> **本文件是什麼？**
> 這是一份「給 AI 看的工作說明書」。當你要開始一個新專案時，把這份文件交給 AI（例如 GitHub Copilot、ChatGPT、Claude），AI 就會按照流程一步步帶你完成整個專案——從零開始，直到上線。
>
> **適用對象**：完全沒有程式基礎的新手也能使用
> **適用範圍**：任何技術棧、任何規模的網頁/應用程式專案
> **設計理念**：基於實戰開發經驗，萃取出通用的開發流程
>
> **如何使用？**
> 1. 複製這整份文件
> 2. 填寫「📝 第一部分：專案需求訪談表」中你知道的部分（不確定的留空就好）
> 3. 把整份文件貼給 AI，告訴它：「請根據這份規格說明書，開始協助我開發專案」
> 4. AI 會先問你問題、確認細節，然後開始動手做

---

## 📖 目錄

- [第一部分：專案需求訪談表](#-第一部分專案需求訪談表使用者填寫)
- [第二部分：AI 事前確認流程](#-第二部分ai-事前確認流程ai-必須在動手前完成)
- [第三部分：技術架構決策](#-第三部分技術架構決策)
- [第四部分：功能需求規格模板](#-第四部分功能需求規格模板)
- [第五部分：AI 工作流程](#-第五部分ai-工作流程開發全週期)
- [第六部分：品質標準與檢查清單](#-第六部分品質標準與檢查清單)
- [第七部分：上線與維運](#-第七部分上線與維運)
- [附錄 A：實戰踩坑紀錄](#-附錄-a實戰踩坑紀錄來自-triplan-專案)
- [附錄 B：常用技術棧速查表](#-附錄-b常用技術棧速查表)
- [附錄 C：成本估算參考](#-附錄-c成本估算參考)

---

# 📝 第一部分：專案需求訪談表（使用者填寫）

> **說明**：請盡量填寫你知道的部分，不確定的留空。AI 會在開始前逐一跟你確認。
> 每一題都有「白話解釋」，幫助你理解這題在問什麼。

### 1. 你想做什麼？

| 項目 | 你的回答 | 白話解釋 |
|------|---------|---------|
| 專案名稱 | | 你的 App 或網站叫什麼名字？ |
| 一句話描述 | | 用一句話告訴朋友「這個東西是幹嘛的」 |
| 主要功能（列出 3-5 個） | | 使用者打開你的 App 後，最常做的事情是什麼？ |
| 目標使用者 | | 誰會用這個產品？一般大眾？公司內部？特定族群？ |
| 有參考的產品嗎？ | | 有沒有你覺得「我想做類似這樣的東西」的網站或 App？ |

### 2. 規模與使用量預估

| 項目 | 你的回答 | 白話解釋 |
|------|---------|---------|
| 預估使用人數 | | 大概多少人會用？10 人？100 人？10,000 人？ |
| 同時在線人數 | | 最多同時有多少人在用？ |
| 需要存檔案嗎？ | | 使用者會上傳照片、文件嗎？大約多少？ |
| 資料量預估 | | 會產生多少筆資料？幾百筆？幾萬筆？ |

### 3. 你的環境與預算

| 項目 | 你的回答 | 白話解釋 |
|------|---------|---------|
| 電腦作業系統 | | Windows / Mac / Linux？ |
| 預算範圍 | | 每個月願意花多少錢維護？0 元也可以（有免費方案） |
| 有網域名稱嗎？ | | 有買 xxx.com 之類的網址嗎？ |
| 程式經驗 | | 完全沒有 / 會一點 HTML / 有寫過程式 |

### 4. 偏好（選填）

| 項目 | 你的回答 | 白話解釋 |
|------|---------|---------|
| 喜歡的介面風格 | | 簡約？色彩豐富？商業正式？可愛活潑？ |
| 語言偏好 | | 介面要中文？英文？多語言？ |
| 有想用的技術嗎？ | | 如果你聽過 React、Vue、Python 之類的，可以寫在這裡 |
| 需要手機版嗎？ | | 只在電腦上用？還是手機也要能用？ |

---

# 🤖 第二部分：AI 事前確認流程（AI 必須在動手前完成）

> **給 AI 的指令**：在寫任何一行程式碼之前，你**必須**完成以下確認流程。
> 使用者可能是完全零基礎的新手，所有提問都要用**高中生都能輕易讀懂的語言**。
> 不要使用未經解釋的技術術語。每個選項都要說明「這對你的意思是什麼」。

## 確認項目 1：技術棧選擇

**AI 必須做的事**：
1. 根據使用者的需求，提出 **3 個最適合的技術方案**
2. 每個方案都要包含：
   - 🏷️ 方案名稱（取一個容易記的名字）
   - 📝 一句話說明（用最白話的方式）
   - ✅ 優點（為什麼選這個好）
   - ❌ 缺點（選這個要注意什麼）
   - 💰 成本影響（會不會花比較多錢）
   - 📈 擴展性（之後想加功能方不方便）
   - 🎓 學習難度（1-5 顆星，1 最簡單）

**提問範例**：
```
你好！我看了你想做的專案，幫你整理了三個方案：

📦 方案 A：輕量網頁方案
就像做一個漂亮的網頁，打開瀏覽器就能用。
適合：資料量不大、功能較簡單的專案
技術：HTML + CSS + JavaScript（如果需要更多功能可搭配 Vue 或 React）
優點：最容易上手，網路上教學最多
缺點：複雜功能需要多花時間處理
成本：可以完全免費（用 GitHub Pages 或 Vercel 部署）
學習難度：⭐⭐

📦 方案 B：全端應用方案
前端（你看到的畫面）+ 後端（幕後處理資料的伺服器），像一個完整的 App。
適合：需要使用者帳號、儲存資料、複雜互動的專案
技術：Vue.js / React（前端）+ Node.js / Python（後端）+ 資料庫
優點：功能強大，什麼都做得到
缺點：東西比較多，建置時間較長
成本：小規模免費，中大規模每月 $0-30 美元
學習難度：⭐⭐⭐

📦 方案 C：快速原型方案
用特殊的「快速開發工具」，最短時間做出可以用的東西。
適合：想先試試看點子可不可行、個人工具
技術：Streamlit（Python）/ Gradio / 低程式碼平台
優點：開發速度最快，幾小時就能看到成果
缺點：介面客製化有限，不適合對外的正式產品
成本：免費或極低
學習難度：⭐

你覺得哪個方向比較接近你想要的？或者你有問題想問？
```

## 確認項目 2：部署方式選擇

**AI 必須做的事**：
1. 確認使用者只在自己電腦上用，還是要讓別人也能打開
2. 如果需要讓別人用，提出 **3 個部署方案**：

**提問範例**：
```
接下來確認一下，你做好的東西要怎麼讓人用呢？

🖥️ 方案 A：只在自己電腦上跑
就像安裝一個軟體在自己電腦上，打開瀏覽器就能用。
別人用不到，但最簡單、完全免費。
適合：個人工具、學習用、內部測試

☁️ 方案 B：放到網路上（免費方案）
讓任何人打開一個網址就能用。
免費平台有流量限制，但一般小專案完全夠用。
平台舉例：
  - Vercel / Netlify：適合靜態網頁或前端專案（完全免費）
  - Railway / Render：適合需要後端的專案（每月有免費額度）
  - Google Cloud Run：適合 Docker 容器化專案（每月 200 萬次免費請求）
  - Firebase Hosting：適合搭配 Firebase 服務的專案（免費額度很大方）
預估成本：$0/月（在免費額度內）

☁️ 方案 C：放到網路上（付費方案，更穩定）
跟方案 B 一樣讓人打開網址就能用，但效能更好、更穩定。
適合：正式對外營運、有一定使用者量的產品
平台舉例：
  - Google Cloud Run + Firebase：穩定可靠，自動擴展（每月 $5-50）
  - AWS（Lightsail / ECS）：企業級，功能最完整（每月 $5-100）
  - DigitalOcean App Platform：操作簡單，價格透明（每月 $5-25）
預估成本：依使用量而定，我可以幫你詳細估算

你目前的需求比較接近哪一種？
```

### 成本估算公式（AI 內部使用）

AI 在推薦方案時，應根據使用者提供的規模資訊，計算出具體的月費預估：

```
【免費額度對照表（以 Google Cloud 為例）】
Firestore：每日 50,000 次讀取 / 20,000 次寫入（免費）
Cloud Run：每月 200 萬次請求 + 36 萬 vCPU 秒（免費）
Cloud Storage：5 GB 儲存空間（免費）
Cloud Build：每日 120 分鐘建置時間（免費）
Firebase Auth：無限制（免費）

【估算方式】
每個使用者每天約 50-100 次 API 請求
每個使用者約 10-50 MB 儲存空間
100 位使用者 × 100 次/天 = 10,000 次/天 = 30 萬次/月 → 免費
1,000 位使用者 × 100 次/天 = 100,000 次/天 = 300 萬次/月 → 約 $5-15/月
10,000 位使用者 → 約 $50-150/月
```

## 確認項目 3：介面風格選擇

**AI 必須做的事**：
1. 根據專案類型，提供 **3 種介面風格建議**
2. 盡可能描述具體的視覺感受，或舉出知名網站/App 作為參考

**提問範例**：
```
最後確認一下你喜歡什麼樣的畫面風格：

🎨 風格 A：簡約乾淨（Minimal Clean）
大量留白，黑白灰為主色調，點綴一個主題色。
類似感覺：Apple 官網、Notion、Google 的介面
適合：工具類 App、專業服務、科技產品

🎨 風格 B：溫暖友善（Warm & Friendly）
圓角按鈕，柔和的色彩（如淺藍、薄荷綠、暖橘），可愛的小圖示。
類似感覺：Airbnb、Duolingo、LINE
適合：面向大眾的產品、社交類、旅遊類、生活類

🎨 風格 C：商業專業（Corporate Professional）
深色搭配亮色標題，表格與圖表為主，資訊密度高。
類似感覺：Bloomberg、Salesforce、企業後台管理系統
適合：數據儀表板、B2B 產品、管理後台

你可以選一個，也可以跟我說「我想要 A 的乾淨感，但顏色用 B 的溫暖色」這樣混搭也可以！
另外你有偏好的主題色嗎？比如藍色代表信任、綠色代表成長、橘色代表活力。
```

---

# 🏗️ 第三部分：技術架構決策

> **給 AI 的指令**：在使用者確認了上述三個項目之後，
> 你需要根據選擇結果，產出本部分的完整技術架構文件。

## 3.1 架構總覽（AI 填寫）

```
【待 AI 根據使用者選擇填寫】

專案名稱：___________
技術方案：___________

前端框架：___________
後端框架：___________
資料庫：  ___________
部署平台：___________
介面風格：___________

架構圖：
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   前端介面    │────▶│   後端 API    │────▶│    資料庫     │
│  (使用者看到) │◀────│  (幕後處理)   │◀────│  (存放資料)   │
└──────────────┘     └──────────────┘     └──────────────┘
```

## 3.2 資料結構設計（AI 填寫）

> AI 應根據使用者的功能需求，設計出完整的資料結構。
> 範例（來自 Triplan 專案）：

```javascript
// 範例：旅行app資料結構
users/{userId}
├── email, displayName, photoURL       // 基本資料
├── role: 'admin' | 'user'             // 角色（管理員或一般使用者）
├── isActive: boolean                  // 帳號是否啟用
├── maxTrips, maxStorageMB             // 使用配額
├── currentTripCount, currentStorageBytes  // 目前使用量（原子計數器）
└── settings: { fontSize, theme }      // 個人偏好

trips/{tripId}
├── destination, startDate, endDate    // 行程基本資訊
├── createdBy: userId                  // 建立者
├── editors: [userId]                  // 可編輯的人
├── viewers: [userId]                  // 只能看的人
├── isDeleted: boolean                 // 軟刪除標記
│
├── days/{dayId}                       // 子集合：每日行程
│   ├── date, items: [行程項目]
│   └── flight: { 航班資訊 }
│
└── expenses/{expenseId}               // 子集合：花費記錄
    ├── amount, currency, paidBy
    └── participants: [userId]
```

## 3.3 API 端點設計（AI 填寫）

> AI 應設計 RESTful API 結構。
> 範例（來自 Triplan 專案）：

```
認證相關：
  POST   /api/auth/register        建立使用者（管理員專用）
  GET    /api/auth/profile/:uid    取得使用者資料

核心功能：
  GET    /api/trips                 取得所有行程（含權限過濾）
  POST   /api/trips                 建立新行程（含配額檢查）
  GET    /api/trips/:id             取得單一行程
  PUT    /api/trips/:id             更新行程
  DELETE /api/trips/:id             軟刪除行程
  POST   /api/trips/:id/restore     還原行程
  DELETE /api/trips/:id/permanent   永久刪除

輔助功能：
  POST   /api/upload                上傳圖片（含壓縮優化）
  POST   /api/metadata              擷取網址預覽
  POST   /api/share                 建立分享連結
  GET    /api/share/:shareId        取得分享的行程（公開）
```

## 3.4 安全性架構（AI 必須設計）

> **這不是選填！每個專案都必須有安全性設計。**

```
認證層：
├── 使用者身份驗證（帳號密碼 / OAuth / 第三方登入[選項非必須]）
├── Token 管理（JWT / Session，自動刷新機制）
└── 密碼安全（交給專業服務處理，如 Firebase Auth，絕不自己存明文密碼）

授權層：
├── 角色權限（管理員 / 一般使用者 / 訪客）
├── 資源存取控制（只能存取自己的資料）
└── API 速率限制（防止惡意大量請求）

資料安全：
├── 輸入驗證（所有使用者輸入都要檢查）
├── API 金鑰保護（不寫死在程式碼中，使用環境變數）
├── HTTPS 加密傳輸
└── 安全標頭（Helmet.js 或同等工具）

【來自 Triplan 的實戰經驗】
- Token 自動刷新：設定在到期前 10 分鐘刷新（60 分鐘到期，50 分鐘刷新）
  原因：如果等 401 錯誤才刷新，使用者會看到短暫的錯誤畫面
- 角色快取 + 主動失效：快取 5 分鐘提升效能，但管理員修改權限時要主動清除快取
  踩坑：一開始忘了加快取失效，導致「管理員改了權限但要等 5 分鐘才生效」
- 速率限制要依功能分級：一般 API 120次/分鐘，上傳 15次/分鐘，登入 30次/15分鐘
  原因：上傳消耗更多伺服器資源，要更嚴格限制
```

---

# 📋 第四部分：功能需求規格模板

> **給 AI 的指令**：根據使用者的需求，為每個功能撰寫一份規格。
> 以下是模板和範例。

## 功能規格模板

```markdown
### F-XXX：[功能名稱]

**功能目標**：用一句話說明這個功能要達成什麼

**使用者操作流程**：
1. 使用者做 ___________
2. 系統回應 ___________
3. 使用者看到 ___________

**介面元素**：
- [ ] 按鈕：[按鈕文字] → 觸發 [什麼動作]
- [ ] 輸入框：[要輸入什麼]
- [ ] 顯示區域：[要顯示什麼]

**資料需求**：
- 需要從哪裡取得資料
- 要儲存什麼資料

**錯誤處理**：
- 如果 _____ 發生，顯示 _____ 訊息
- 如果 _____ 失敗，執行 _____ 動作

**驗收標準**（怎樣算做好了）：
- [ ] 使用者可以 _____
- [ ] 系統能夠 _____
- [ ] 錯誤情況有 _____
```

## 功能規格範例（來自 Triplan）

```markdown
### F-001：使用者登入

**功能目標**：讓已註冊的使用者可以安全登入系統

**使用者操作流程**：
1. 使用者打開網站，看到登入頁面
2. 輸入 Email 和密碼，按下「登入」按鈕
3. 系統驗證帳號密碼
4. 成功 → 跳轉到首頁（行程列表）
5. 失敗 → 在頁面上顯示錯誤訊息

**介面元素**：
- [x] 輸入框：Email（格式驗證）
- [x] 輸入框：密碼（密碼遮罩，type="password"）
- [x] 按鈕：「登入」→ 送出驗證
- [x] 提示：「請聯絡管理員開通帳號」（本系統不開放自行註冊）

**資料需求**：
- Firebase Authentication 驗證帳密
- 登入後取得 Firestore 中的使用者資料（角色、配額等）

**錯誤處理**：
- 帳號或密碼錯誤 → 「電子郵件或密碼錯誤」
- 帳號被停用 → 「帳號已停用，請聯絡系統管理員」
- 網路錯誤 → 「連線失敗，請稍後再試」

**驗收標準**：
- [x] 正確帳密可以登入
- [x] 錯誤帳密有明確提示
- [x] Token 自動刷新（50 分鐘一次）
- [x] 關閉瀏覽器後重新開啟會自動登入（記住登入狀態）

### F-002：行程管理（CRUD）

**功能目標**：使用者可以建立、查看、編輯、刪除旅行行程

**使用者操作流程**：
1. 首頁看到自己所有的行程卡片
2. 按 ＋ 按鈕 → 建立新行程（輸入目的地、日期、天數）
3. 點擊行程卡片 → 進入行程詳情頁
4. 在詳情頁中可以新增每天的行程項目
5. 刪除時先進入垃圾桶（可恢復），30 天後自動永久刪除

**資料需求**：
- trips 集合：基本資訊 + 權限 + 軟刪除狀態
- days 子集合：每日行程
- expenses 子集合：花費記錄

**特殊設計（來自實戰經驗）**：
- 「軟刪除」設計：不是真的刪掉，只是標記 isDeleted = true
  好處：使用者手滑刪錯可以從「垃圾桶」找回來
- 「配額檢查」設計：建立行程前先檢查是否超過上限
  原因：不同等級的使用者有不同的行程數量限制
- 「原子計數器」設計：使用 FieldValue.increment(1)
  原因：如果用 read → +1 → write，兩個人同時建立行程會出錯
```

---

# ⚙️ 第五部分：AI 工作流程（開發全週期）

> **這是整份文件最核心的部分。**
> AI 必須嚴格按照這個流程執行，每一步完成後要向使用者回報進度。

## 階段 0：環境準備（約 15-30 分鐘）

### 0.1 確認使用者的電腦環境

```
AI 要確認的事項：
□ 作業系統（Windows / Mac / Linux）
□ 是否已安裝 Node.js（前端/全端專案需要）
□ 是否已安裝 Python（Python 專案需要）
□ 是否已安裝 Git（版本控制，幾乎所有專案都需要）
□ 是否已安裝 Docker（本地測試/容器部署需要）
□ 編輯器（VS Code 推薦）

若缺少任何工具，AI 會提供安裝指令並協助安裝。
```

### 0.2 自動化環境建置腳本

> **AI 必須做的事**：為使用者的作業系統生成一鍵安裝腳本。

**Windows（PowerShell）範例**：
```powershell
# setup-env.ps1 — 一鍵環境建置
Write-Host "🔧 開始檢查開發環境..." -ForegroundColor Cyan

# 檢查 Node.js
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js $(node -v) 已安裝" -ForegroundColor Green
} else {
    Write-Host "📦 正在安裝 Node.js..." -ForegroundColor Yellow
    winget install OpenJS.NodeJS.LTS
}

# 檢查 Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host "✅ Git $(git --version) 已安裝" -ForegroundColor Green
} else {
    Write-Host "📦 正在安裝 Git..." -ForegroundColor Yellow
    winget install Git.Git
}

# 檢查 Docker
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "✅ Docker $(docker --version) 已安裝" -ForegroundColor Green
} else {
    Write-Host "📦 請手動安裝 Docker Desktop：https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
}

Write-Host "`n🎉 環境檢查完成！" -ForegroundColor Cyan
```

**Mac / Linux（Bash）範例**：
```bash
#!/bin/bash
# setup-env.sh — 一鍵環境建置
echo "🔧 開始檢查開發環境..."

# 檢查 Node.js
if command -v node &> /dev/null; then
    echo "✅ Node.js $(node -v) 已安裝"
else
    echo "📦 正在安裝 Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# 檢查 Git
if command -v git &> /dev/null; then
    echo "✅ Git 已安裝"
else
    echo "📦 正在安裝 Git..."
    sudo apt-get install -y git
fi

echo "🎉 環境檢查完成！"
```

### 0.3 專案初始化

AI 在完成環境確認後，必須：

1. **建立專案資料夾結構**
2. **初始化版本控制**（`git init`）
3. **安裝必要的套件**（`npm install` / `pip install` 等）
4. **建立 .gitignore**（排除不該上傳的檔案）
5. **建立 .env.example**（環境變數範本，不含真實密鑰）

```
AI 建立的初始資料夾結構範例：

my-project/
├── .git/                    # Git 版本控制（自動產生）
├── .gitignore               # 排除清單
├── .env.example             # 環境變數範本
├── README.md                # 專案說明書
├── TODO.md                  # 待辦事項追蹤
├── CHANGELOG.md             # 修改歷程記錄
├── docker-compose.yml       # 本地測試環境
├── Dockerfile               # 容器建置設定
├── setup-env.ps1            # 環境建置腳本（Windows）
├── setup-env.sh             # 環境建置腳本（Mac/Linux）
│
├── backend/                 # 後端程式碼
│   ├── package.json
│   ├── server.js
│   ├── config/
│   ├── middleware/
│   ├── routes/
│   └── scripts/            # 工具腳本（建立管理員等）
│
├── frontend/                # 前端程式碼
│   ├── package.json
│   ├── src/
│   │   ├── components/     # UI 元件
│   │   ├── views/          # 頁面
│   │   ├── stores/         # 狀態管理
│   │   ├── router/         # 路由
│   │   ├── composables/    # 可重用邏輯
│   │   └── config/         # 設定檔
│   └── index.html
│
├── docs/                    # 文件資料夾（AI 維護）
│   ├── ARCHITECTURE.md      # 架構說明（給 AI 讀的）
│   ├── DEPLOYMENT.md        # 部署指南
│   ├── BEGINNER_GUIDE.md    # 新手教學
│   └── SKILLLOG.md          # 開發經驗紀錄
│
└── scripts/                 # 自動化腳本
    ├── build-and-deploy.ps1 # 建置部署
    └── setup-backup.ps1     # 備份設定
```

## 階段 1：建立文件先行（在寫程式之前）

### 1.1 README.md — 專案說明書

> AI 必須在寫任何程式碼之前，先產出 README.md。

```markdown
# [專案名稱]

> [一句話描述]

## 📋 功能特色
- 功能 1：[描述]
- 功能 2：[描述]
- 功能 3：[描述]

## 🛠️ 技術棧
| 類別 | 技術 | 用途 |
|------|------|------|
| 前端 | [框架] | [用途] |
| 後端 | [框架] | [用途] |
| 資料庫 | [名稱] | [用途] |
| 部署 | [平台] | [用途] |

## 🚀 快速開始
### 安裝
（具體的安裝步驟）

### 本地執行
（如何在自己電腦上跑起來）

### Docker 執行
（如何用 Docker 跑起來）

## 📁 專案結構
（資料夾結構樹 + 每個檔案的說明）

## 📖 API 文件
（所有 API 端點的清單 + 說明）

## 🤝 給 AI 的指引
**重要！** 如果你是另一位 AI 助手，請先閱讀：
1. `docs/ARCHITECTURE.md` — 系統架構全覽
2. `CHANGELOG.md` — 最近的修改紀錄
3. `TODO.md` — 目前待辦事項
這三份文件可以讓你在 2 分鐘內了解整個專案的狀況。
```

### 1.2 TODO.md — 待辦事項追蹤

> 這是 AI 和使用者共同管理的開發進度。

```markdown
# 📋 TODO — [專案名稱] 開發進度

> 最後更新：[日期]  
> 總進度：[X]%（[已完成]/[總數]）

## 🟢 階段 1：基礎建設（目標：可以跑起來）
- [x] 環境建置（Node.js / Docker / Git）
- [x] 專案初始化（資料夾結構 + Git）
- [x] 資料庫設計（Schema 規劃）
- [ ] 基本 CRUD API
- [ ] 使用者認證

## 🟡 階段 2：核心功能（目標：主要功能可用）
- [ ] 功能 A
- [ ] 功能 B
- [ ] 功能 C

## 🔵 階段 3：介面優化（目標：好看好用）
- [ ] RWD 響應式設計
- [ ] Loading 動畫
- [ ] 錯誤訊息優化

## 🟣 階段 4：上線準備（目標：可以對外使用）
- [ ] 效能優化
- [ ] 安全性檢查
- [ ] 部署腳本
- [ ] 備份機制

## 🐛 已知問題
| 問題 | 嚴重度 | 狀態 |
|------|--------|------|
| [描述] | 高/中/低 | 處理中/待修 |
```

### 1.3 CHANGELOG.md — 修改歷程記錄

> **這是讓不同 AI 能快速接手的關鍵文件。**

```markdown
# 📝 CHANGELOG — 修改歷程

> 格式：每次修改都記錄「改了什麼」「為什麼改」「影響範圍」
> 這樣換一個 AI 助手接手時，不需要讀完所有程式碼就能了解脈絡。

## [日期] - [版本號或描述]

### 新增
- **[檔案名稱]**：[描述新增了什麼]
  - 原因：[為什麼要加這個]
  - 影響：[會影響到哪些其他檔案或功能]

### 修改
- **[檔案名稱]**：[描述修改了什麼]
  - 原因：[為什麼要改]
  - 前後差異：[從什麼 → 變成什麼]

### 修復
- **[Bug 描述]**：[如何修復]
  - 根因：[問題的根本原因]
  - 影響：[修復後哪些功能恢復正常]

### 架構決策
- **[決策描述]**：[選了什麼方案]
  - 考慮過的選項：[A, B, C]
  - 選擇原因：[為什麼選這個]
  - 取捨：[放棄了什麼]
```

### 1.4 docs/ARCHITECTURE.md — 系統架構（給 AI 讀的）

> **這是 AI 接手專案時的第一份文件。**
> 必須包含足夠的資訊，讓一個全新的 AI 在讀完後就能開始工作。

```markdown
# 🏗️ 系統架構說明

> 最後更新：[日期]
> 本文件是給 AI 助手閱讀的快速導覽。如果你是 AI，讀完這份就能開始工作。

## 一句話概述
[這個專案是做什麼的，用什麼技術做的]

## 架構圖
[ASCII 架構圖，展示各層之間的關係]

## 資料流向
[使用者操作 → 前端 → API → 資料庫 → 回傳 的完整路徑]

## 關鍵檔案索引
| 檔案 | 用途 | 關鍵程度 |
|------|------|---------|
| server.js | 後端主程式，所有 API 的進入點 | ⭐⭐⭐ |
| config/firebase.js | 資料庫連線設定（三種模式） | ⭐⭐⭐ |
| middleware/auth.js | 身份驗證 + 權限檢查 | ⭐⭐⭐ |
| routes/trips.js | 核心業務邏輯（行程 CRUD） | ⭐⭐⭐ |
| stores/auth.js | 前端登入狀態管理 | ⭐⭐ |
| router/index.js | 前端路由 + 登入保護 | ⭐⭐ |

## 目前狀態
- 已完成：[清單]
- 進行中：[清單]
- 尚未開始：[清單]
- 已知問題：[清單]

## 環境設定
- 開發環境：[如何啟動]
- 測試環境：[如何測試]
- 生產環境：[如何部署]

## 注意事項 & 踩坑紀錄
[重要的「別踩同樣的坑」提醒]
```

## 階段 2：本地開發（Docker 優先）

### 2.1 Docker 本地測試環境

> **為什麼用 Docker？**
> 想像 Docker 是一個「打包好的電腦環境」。不管你用 Windows、Mac 還是 Linux，
> 用 Docker 跑起來的結果都一模一樣。這樣就不會出現「我的電腦可以跑，你的不行」的問題。

**AI 必須做的事**：
1. 如果使用者沒有 Docker，協助安裝 Docker Desktop
2. 建立 `docker-compose.yml`（本地開發用）
3. 建立 `Dockerfile`（生產部署用）
4. 確保 `docker compose up` 一個指令就能把整個專案跑起來

**docker-compose.yml 範例（來自 Triplan 實戰經驗）**：
```yaml
# docker-compose.yml — 本地開發環境
# 使用方式：在終端機輸入 docker compose up --build

services:
  # 後端 API 伺服器
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"          # 你的瀏覽器訪問 http://localhost:8080
    environment:
      - NODE_ENV=development
    volumes:
      - ./backend:/app       # 修改程式碼會自動重新載入（不用重啟）
    depends_on:
      - db

  # 前端開發伺服器（開發時才需要，上線後前端會打包成靜態檔）
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"          # 開發時訪問 http://localhost:3000
    volumes:
      - ./frontend/src:/app/src  # 修改程式碼即時生效（Hot Reload）

  # 資料庫（依專案選擇）
  db:
    image: [資料庫映像]      # 例如 mongo:7, postgres:16, mysql:8
    ports:
      - "27017:27017"        # 資料庫埠號
    volumes:
      - db_data:/data/db     # 資料持久化（重啟不遺失）

volumes:
  db_data:                   # 資料庫檔案存放位置
```

**Dockerfile 範例（多階段建置，來自 Triplan 實戰）**：
```dockerfile
# ===== 階段 1：打包前端 =====
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci                      # 安裝前端套件
COPY frontend/ ./
RUN npm run build               # 打包成靜態檔案

# ===== 階段 2：生產環境 =====
FROM node:20-alpine AS production
WORKDIR /app

# 只安裝後端生產套件（比開發環境小很多）
COPY backend/package*.json ./
RUN npm ci --only=production

# 只複製必要的後端檔案（不要把整個 node_modules 搬過來）
COPY backend/server.js ./
COPY backend/config ./config
COPY backend/middleware ./middleware
COPY backend/routes ./routes

# 把前端打包好的靜態檔案放進來
COPY --from=frontend-builder /app/frontend/dist ./public

# 健康檢查（讓平台知道你的 App 還活著）
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:8080/health')"

EXPOSE 8080
CMD ["node", "server.js"]
```

### 2.2 何時不需要 Docker

> 小型專案（純前端、Streamlit、簡單腳本）不需要 Docker。

判斷標準：
- ✅ 需要 Docker：有前端 + 後端 + 資料庫（3 個以上服務）
- ✅ 需要 Docker：多人協作開發
- ✅ 需要 Docker：要部署到雲端容器服務
- ❌ 不需要 Docker：純前端網頁（HTML/CSS/JS）
- ❌ 不需要 Docker：Streamlit / Gradio 單一 Python 檔
- ❌ 不需要 Docker：個人學習用小程式

## 階段 3：開發與記錄

### 3.1 日誌系統（Log）— 必備

> **為什麼 Log 很重要？**
> 想像你的程式是一個黑盒子。出錯了你不知道裡面發生什麼事。
> Log 就是讓程式把「它正在做什麼」寫下來，方便你（或 AI）回頭查看。

**AI 必須做的事**：
1. 每個 API 都要有請求日誌（誰在什麼時候呼叫了什麼）
2. 每個錯誤都要有詳細的錯誤日誌（發生了什麼、為什麼）
3. 關鍵操作要有操作日誌（建立了什麼、刪除了什麼）
4. 出錯時，AI 要先看 Log 再嘗試修復

**後端 Logger 範例（來自 Triplan）**：
```javascript
// middleware/logger.js
const logger = (req, res, next) => {
  const start = Date.now();

  // 在回應結束時記錄日誌
  res.on('finish', () => {
    const duration = Date.now() - start;
    const logEntry = {
      method: req.method,           // GET, POST, PUT, DELETE
      url: req.originalUrl,         // /api/trips
      status: res.statusCode,       // 200, 404, 500
      duration: `${duration}ms`,    // 花了多少時間
      user: req.user?.uid || 'anonymous',
      timestamp: new Date().toISOString()
    };

    // 根據狀態碼用不同層級記錄
    if (res.statusCode >= 500) {
      console.error('❌ SERVER ERROR:', JSON.stringify(logEntry));
    } else if (res.statusCode >= 400) {
      console.warn('⚠️ CLIENT ERROR:', JSON.stringify(logEntry));
    } else {
      console.log('✅ OK:', JSON.stringify(logEntry));
    }
  });

  next();
};
```

**前端錯誤捕捉範例**：
```javascript
// main.js — 全域錯誤捕捉
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err, info);
};

window.onerror = (message, source, lineno, colno, error) => {
  console.error('Global Error:', { message, source, lineno, colno });
};

window.addEventListener('unhandledrejection', (event) => {
  console.error('Unhandled Promise:', event.reason);
});
```

### 3.2 AI 自助除錯流程

> **當使用者回報問題時，AI 應遵循以下流程：**

```
1️⃣ 第一步：問使用者「你看到什麼？」
   → 截圖、錯誤訊息、或行為描述

2️⃣ 第二步：查看 Log
   → 後端：終端機輸出 或 docker compose logs app
   → 前端：瀏覽器 F12 → Console 頁籤
   → 雲端：Cloud Logging 或 Dashboard

3️⃣ 第三步：定位問題
   → 是前端問題？（畫面相關）
   → 是後端問題？（API 回傳錯誤）
   → 是資料庫問題？（查詢/寫入失敗）
   → 是環境問題？（設定、權限、網路）

4️⃣ 第四步：修復並驗證
   → 修改程式碼
   → 重新測試
   → 確認 Log 沒有新的錯誤

5️⃣ 第五步：記錄到 CHANGELOG.md 和 SKILLLOG.md
   → 記下問題原因、修復方式
   → 這樣下次遇到同樣的問題就能快速解決
```

### 3.3 開發紀錄維護

> **AI 在每次修改後必須做的事**：

```
每次修改程式碼後，AI 必須：
     ↓
1. 更新 CHANGELOG.md（記錄改了什麼、為什麼改）
     ↓
2. 更新 TODO.md（標記完成的項目、新增發現的問題）
     ↓
3. 如果架構有變動 → 更新 docs/ARCHITECTURE.md
     ↓
4. 如果踩到新坑 → 更新 docs/SKILLLOG.md
     ↓
5. 如果影響部署 → 更新 docs/DEPLOYMENT.md
```

## 階段 4：測試驗證

### 4.1 測試策略

```
【最小必要測試】
以下是「不管專案多小都要有」的測試：

1. 冒煙測試（Smoke Test）— App 能正常啟動嗎？
   □ 後端 server 啟動，GET /health 回傳 200
   □ 前端首頁可以正常載入
   □ 登入功能正常運作

2. CRUD 測試 — 核心功能可以用嗎？
   □ 可以新增資料
   □ 可以讀取資料
   □ 可以更新資料
   □ 可以刪除資料

3. 權限測試 — 安全性沒問題嗎？
   □ 未登入的人不能存取受保護的頁面
   □ 一般使用者不能做管理員的事
   □ 使用者不能存取別人的資料

4. 錯誤處理測試 — 出錯時不會爆炸嗎？
   □ 輸入錯誤格式會有友善提示
   □ 網路斷線有適當的處理
   □ 伺服器錯誤有友善的錯誤頁面
```

### 4.2 AI 自動化測試輔助

```
AI 可以幫使用者做的事：
1. 用 curl 或 PowerShell 測試 API 是否正常回應
2. 檢查 docker compose logs 有沒有錯誤
3. 在瀏覽器手動走一遍操作流程
4. 用 Lighthouse（Chrome 內建工具）檢查效能分數
```

---

# ✅ 第六部分：品質標準與檢查清單

## 6.1 程式碼品質標準

```
【AI 寫程式時必須遵守的規則】

1. 可讀性
   - 變數名稱有意義（用 userProfile 不要用 data1）
   - 關鍵邏輯要有中文註解
   - 一個函數只做一件事

2. 安全性
   - 所有使用者輸入都要驗證
   - 密碼和金鑰不寫死在程式碼中
   - API 有速率限制
   - 使用 HTTPS

3. 錯誤處理
   - 所有 API 呼叫都有 try-catch
   - 錯誤訊息對使用者友善
   - 錯誤日誌對開發者有用

4. 效能
   - 圖片壓縮後再上傳
   - 大量資料用分頁載入
   - 靜態資源設定快取

5. 維護性
   - 程式碼有清楚的檔案結構
   - 重複的邏輯抽出為共用函數
   - 設定值使用環境變數
```

## 6.2 介面品質標準

```
【UI/UX 必備清單】

1. 響應式設計
   □ 手機（320px-480px）可正常使用
   □ 平板（768px-1024px）版面合理
   □ 桌機（1024px+）善用空間

2. 使用者回饋
   □ 按鈕點擊後有視覺回饋
   □ 載入中有 Loading 動畫或提示
   □ 操作成功有確認訊息
   □ 操作失敗有錯誤訊息和建議

3. 一致性
   □ 字體大小統一
   □ 顏色使用一致
   □ 按鈕風格統一
   □ 間距和對齊統一

4. 無障礙基本要求
   □ 圖片有替代文字
   □ 表單輸入框有標籤
   □ 色彩對比度足夠（文字看得清楚）
```

## 6.3 上線前安全性檢查清單

> **來自 Triplan 實戰的安全檢查項目**：

```
【認證與授權】
□ 所有受保護的 API 都有 Token 驗證
□ 管理員功能有角色檢查
□ 使用者只能存取自己的資料
□ Token 過期有自動刷新機制
□ 密碼不以明文儲存

【輸入驗證】
□ 所有使用者輸入都有伺服器端驗證（不只靠前端檢查）
□ 檔案上傳有類型和大小限制
□ SQL / NoSQL 注入防護
□ XSS（跨站腳本攻擊）防護

【基礎設施】
□ HTTPS 加密（部署平台通常自動提供）
□ 安全 HTTP 標頭（Helmet.js 或同類工具）
□ API 速率限制
□ 環境變數管理（不把密鑰寫死在程式碼中）
□ .gitignore 確認（service-account.json 等敏感檔案不上傳）

【資料保護】
□ 定期自動備份
□ 軟刪除機制（誤刪可復原）
□ 敏感日誌不記錄完整的 Token 或密碼
□ CORS 設定限制來源（上線後不要用 *）

【來自 Triplan 的踩坑經驗】
⚠️ 在開發時 CORS 設為 * 很方便，但上線前一定要改成只允許你的網域
⚠️ Firebase 的 Storage Rules 很容易忘記設定，上線前一定要檢查
⚠️ Cloud Run 的 Service Account 預設權限不夠，需要手動加 IAM 角色：
   - roles/datastore.user（Firestore 存取）
   - roles/firebase.admin（Auth 操作）
   - roles/serviceusage.serviceUsageConsumer（API 呼叫）
```

---

# 🚀 第七部分：上線與維運

## 7.1 上線前完整評估（AI 必須執行）

> **當使用者說「我想上線」時，AI 必須主動進行以下檢查：**

### 效能評估清單

```
【前端效能】
□ 首頁載入時間 < 3 秒
□ Lighthouse 效能分數 > 80
□ 圖片已壓縮（WebP 格式，來自 Triplan 經驗：Sharp 轉 WebP @ 80% 品質）
□ JavaScript 打包有程式碼分割（Code Splitting）
□ 靜態資源有快取標頭
   └── 帶 hash 的檔案：max-age=31536000（一年，因為檔名含內容指紋）
   └── HTML 檔案：no-cache（確保拿到最新版本）
□ Gzip / Brotli 壓縮啟用

【後端效能】
□ API 回應時間 < 500ms
□ 資料庫查詢有索引（來自 Triplan 經驗：Firestore 複合索引須預先部署）
□ 頻繁查詢的資料有快取
□ 大量寫入使用批次操作（Firestore 限制每批 500 筆）
□ 檔案上傳有大小限制（建議 10MB）

【基礎設施效能】
□ 自動擴展設定合理（Triplan 經驗：Cloud Run 設 0-10 個實例）
   └── 最小 0：沒人用時不花錢（但首次請求會慢 2-3 秒，稱為 Cold Start）
   └── 最大 10：防止突然大量請求時帳單爆炸
□ 記憶體配置合理（Triplan 經驗：512Mi 對小型應用足夠）
□ 健康檢查端點 (/health) 正常回應
```

### 安全性評估清單

```
（參見 6.3 節的完整清單）
AI 必須逐項檢查並回報結果給使用者。
```

## 7.2 部署自動化腳本

> **AI 必須提供一鍵部署腳本。**

**PowerShell 部署腳本範例（來自 Triplan 實戰）**：
```powershell
# build-and-deploy.ps1 — 一鍵建置部署
param(
    [string]$ProjectId = "your-project-id",
    [string]$Region = "asia-east1",
    [string]$ServiceName = "your-app"
)

Write-Host "🚀 開始部署 $ServiceName" -ForegroundColor Cyan

# 步驟 1：建置 Docker 映像
Write-Host "📦 Step 1/3：建置中..." -ForegroundColor Yellow
# （此處放建置指令，依部署平台而異）

# 步驟 2：推送到映像倉庫
Write-Host "☁️ Step 2/3：上傳中..." -ForegroundColor Yellow
# （此處放推送指令）

# 步驟 3：更新線上服務
Write-Host "🔄 Step 3/3：部署中..." -ForegroundColor Yellow
# （此處放部署指令）

Write-Host "✅ 部署完成！" -ForegroundColor Green
Write-Host "🌍 網址：https://$ServiceName-xxx.run.app" -ForegroundColor Cyan
```

## 7.3 備份策略

> **資料備份是上線後最重要的事，沒有之一。**

```
【自動備份建議】
頻率：每天一次（凌晨 4 點，使用者最少的時候）
保留：最近 7 天的備份
儲存：獨立的雲端儲存空間（與主資料庫分開）

【來自 Triplan 的備份架構】
Cloud Scheduler (每天 20:00 UTC = 凌晨 4:00 台灣時間)
  → Cloud Run Job
    → gcloud firestore export → Cloud Storage Bucket
    → 命名格式：backup-YYYYMMDD
    → 自動清除 7 天前的備份
```

## 7.4 上線後監控

```
【最小必要監控】
1. 健康檢查：每 30 秒確認 App 還活著
2. 錯誤通知：出現 500 錯誤時通知開發者
3. 使用量監控：確保沒有超出免費額度（避免意外帳單）

【免費監控工具推薦】
- Google Cloud Console 儀表板（Cloud Run 內建）
- UptimeRobot（免費，每 5 分鐘檢查一次你的網站是否正常）
- Firebase Console（查看資料庫使用量、認證使用者數量）
```

## 7.5 上線後版本更新流程

```
1. 在本地開發和測試新功能
2. 確認沒問題後，更新 CHANGELOG.md
3. 執行部署腳本
4. 確認線上版本正常運作
5. 如果有問題，用快速回滾指令還原

【快速回滾】
大多數雲端平台支援回滾到上一個版本：
  - Cloud Run：gcloud run services update-traffic --to-revisions=前次版本=100
  - Vercel：Dashboard → Deployments → 選之前的版本 → Redeploy
  - Railway：Dashboard → Deployments → Rollback
```

---

# 📚 附錄 A：實戰踩坑紀錄（來自 Triplan 專案）

> 以下是在開發 Triplan（旅行規劃 App）過程中踩過的坑，
> 每一個都是用時間和挫折換來的教訓。AI 在開發時要主動避免這些問題。

## 🔴 致命級問題

### 踩坑 #1：Firestore Timestamp 無法存入 IndexedDB
```
症狀：離線儲存功能出錯，瀏覽器報 DataCloneError
原因：Firestore 的 Timestamp 物件不是普通的 JavaScript 物件，IndexedDB 不認識它
修復：在存入 IndexedDB 前，把所有 Timestamp 轉成 ISO 字串
教訓：不同的儲存系統對資料格式有不同要求，跨系統傳資料時一定要轉換格式
```

### 踩坑 #2：Cloud Run 的 IAM 權限串聯（401 → 500 → 403）
```
症狀：部署上去後 API 全部回 403 PERMISSION_DENIED
原因：Cloud Run 的服務帳號預設沒有存取 Firebase 的權限
修復：手動加上 3 個 IAM 角色
   1. roles/datastore.user（才能讀寫 Firestore）
   2. roles/firebase.admin（才能驗證使用者 Token）
   3. roles/serviceusage.serviceUsageConsumer（才能呼叫 Firebase API）
教訓：「能在本機跑」不代表「能在雲端跑」，雲端環境需要額外設定權限
      而且跨 GCP 專案的權限設定特別容易出錯
```

### 踩坑 #3：Firestore 複合索引必須預先建置
```
症狀：查詢行程時報錯 "The query requires an index"
原因：Firestore 的複雜查詢（同時用多個條件過濾）需要預先建好索引
修復：部署 firestore.indexes.json（裡面定義了哪些查詢需要索引）
教訓：Firestore 不像傳統資料庫可以自動處理複雜查詢，要提前規劃索引
      CI/CD 流程中要加上 "firebase deploy --only firestore:indexes"
```

## 🟡 中級問題

### 踩坑 #4：角色快取缺少主動失效機制
```
症狀：管理員改了使用者的角色，但使用者的權限沒有立刻改變
原因：getUserProfile() 有 5 分鐘快取，改了資料庫，快取還是舊的
修復：加上 invalidateUserCache(uid) 函數，管理員修改後主動清除快取
教訓：有快取的地方就要有清除快取的機制
      口訣：「加快取時，一定要同時寫清除快取的程式」
```

### 踩坑 #5：undefined 會讓 Firestore Admin SDK 崩潰
```
症狀：更新資料時偶爾報 500 錯誤
原因：有些欄位的值是 undefined（不是 null），Firestore Admin SDK 不接受
修復：在 Firebase 設定中加上 ignoreUndefinedProperties: true
教訓：前端 SDK 會自動忽略 undefined，但後端 Admin SDK 很嚴格
      不同的 SDK 版本行為不同，要實際測試
```

### 踩坑 #6：SPA 路由的快取問題
```
症狀：更新部署後，使用者看到的還是舊版本
原因：瀏覽器對 index.html 做了快取，不會去拿新的 JavaScript
修復：index.html 不快取（no-cache），JavaScript/CSS 用內容雜湊命名
      加上 <meta name="app-version" content="時間戳"> 做版本偵測
教訓：帶雜湊的靜態檔案可以永久快取（因為內容改了檔名也會變）
      HTML 入口檔案絕不能快取（否則永遠載入舊的 JavaScript）
```

## 🟢 優良實踐（做對的事情）

### 實踐 #1：軟刪除 + 垃圾桶機制
```
做法：刪除只是標記 isDeleted = true，不是真的刪掉
好處：使用者手滑可以從垃圾桶復原
搭配：Cloud Functions 每天自動清理 30 天前的垃圾
```

### 實踐 #2：原子計數器防止覆蓋問題
```
做法：用 FieldValue.increment(1) 而不是 read → +1 → write
好處：兩個人同時建立行程不會把計數器搞錯
原理：由資料庫端做加法，保證不會有「兩人同時讀到 5，都寫回 6」的問題
```

### 實踐 #3：多階段 Docker 建置
```
做法：第一階段打包前端，第二階段只放生產需要的檔案
好處：最終映像從 700MB 縮小到 ~200MB，啟動更快、省錢
原理：打包工具（Node.js devDependencies）只在第一階段用，不帶到最終映像
```

### 實踐 #4：Token 提前刷新
```
做法：不等到 Token 過期（60 分鐘），在第 50 分鐘就主動刷新
好處：使用者永遠不會看到「登入已過期」的錯誤
搭配：axios 攔截器，萬一真的 401 了，自動刷新後重送請求
```

### 實踐 #5：三模式 Firebase 初始化
```
做法：根據環境自動選擇 Firebase 連線方式
  開發模式：用模擬器（不花錢、不影響正式資料）
  本機模式：用 Service Account JSON 檔
  雲端模式：用自動偵測的憑證（不需要 JSON 檔）
好處：同一套程式碼在任何環境都能跑
```

---

# 📚 附錄 B：常用技術棧速查表

> AI 在推薦技術方案時可以參考此表。

## 前端框架

| 框架 | 特色 | 適合 | 學習難度 |
|------|------|------|---------|
| **Vue.js** | 漸進式、友善新手、中文資源多 | 中小型專案、新手 | ⭐⭐ |
| **React** | 生態最大、就業機會多 | 各種規模、想找工作 | ⭐⭐⭐ |
| **Svelte** | 編譯型、效能最好、語法最簡潔 | 效能要求高的專案 | ⭐⭐ |
| **Next.js** | React + 伺服器渲染 + 一體化 | SEO 重要的網站 | ⭐⭐⭐ |
| **Nuxt.js** | Vue + 伺服器渲染 + 一體化 | SEO 重要的 Vue 專案 | ⭐⭐⭐ |
| **Astro** | 靜態為主、超快載入 | 部落格、官網、文件站 | ⭐⭐ |

## 後端框架

| 框架 | 語言 | 特色 | 適合 |
|------|------|------|------|
| **Express.js** | Node.js | 最輕量、最自由 | 快速開發、REST API |
| **Fastify** | Node.js | 比 Express 快、內建驗證 | 效能要求高的 API |
| **Django** | Python | 全功能內建、自帶管理後台 | 需要後台管理的專案 |
| **FastAPI** | Python | 超快、自動生成 API 文件 | Python 生態的 API |
| **Spring Boot** | Java | 企業級、功能最完整 | 大型企業專案 |
| **Go (Gin)** | Go | 編譯型、效能頂尖 | 高併發微服務 |

## 資料庫

| 資料庫 | 類型 | 特色 | 適合 |
|--------|------|------|------|
| **Firestore** | NoSQL (文件) | 免費額度大、即時同步、自動擴展 | Firebase 生態的專案 |
| **MongoDB** | NoSQL (文件) | 彈性 Schema、最流行的 NoSQL | 資料結構經常變的專案 |
| **PostgreSQL** | SQL (關聯) | 功能最強的開源 SQL、支援 JSON | 需要複雜查詢的專案 |
| **MySQL** | SQL (關聯) | 最普及、效能好 | 傳統 Web 應用 |
| **SQLite** | SQL (嵌入式) | 不需要伺服器、單一檔案 | 小型應用、桌面軟體 |
| **Supabase** | PostgreSQL 託管 | Firebase 的 SQL 替代品 | 偏好 SQL 但想要 Firebase 體驗 |
| **PlanetScale** | MySQL 託管 | 自動分支、自動擴展 | 需要資料庫版本控制 |

## 部署平台

| 平台 | 免費額度 | 特色 | 適合 |
|------|---------|------|------|
| **Vercel** | 100GB/月流量 | 最簡單、Git push 自動部署 | 前端 / Next.js |
| **Netlify** | 100GB/月流量 | 同 Vercel，表單功能好 | 靜態網站 / SPA |
| **Railway** | $5/月免費額度 | 支援任何語言、Docker | 全端應用 |
| **Render** | 750 小時/月免費 | 類 Heroku、支援 Docker | 全端應用（免費方案有 15 分鐘休眠） |
| **Google Cloud Run** | 200 萬次/月請求 | 容器化、自動擴展到 0 | Docker 容器化專案 |
| **Firebase Hosting** | 10GB/月流量 | 自動 CDN、搭配 Firebase 服務 | Firebase 生態專案 |
| **Fly.io** | 3 個小型 VM 免費 | 全球部署、Volumes 支援 | 需要持久化儲存的後端 |
| **GitHub Pages** | 完全免費 | 最簡單、直接從 Git 部署 | 純靜態網頁、個人網站 |

## 快速原型工具

| 工具 | 語言 | 特色 | 適合 |
|------|------|------|------|
| **Streamlit** | Python | 寫 Python 就能出網頁 | 數據分析 / AI 應用 |
| **Gradio** | Python | 專為 ML/AI 模型做界面 | AI Demo / 模型展示 |
| **Reflex** | Python | 純 Python 寫全端 Web App | Python 開發者 |
| **Retool** | 低程式碼 | 拖拉式建立內部工具 | 企業內部管理系統 |

---

# 📚 附錄 C：成本估算參考

## 月費估算對照表

### Google Cloud（Cloud Run + Firestore）— 來自 Triplan 實際經驗

| 使用者規模 | 月請求量 | 儲存量 | 預估月費 | 說明 |
|-----------|---------|--------|---------|------|
| 1-10 人 | ~3 萬 | <1 GB | **$0** | 完全在免費額度內 |
| 10-100 人 | ~30 萬 | 1-5 GB | **$0** | 仍在免費額度內 |
| 100-1,000 人 | ~300 萬 | 5-50 GB | **$5-30** | 開始超過免費額度 |
| 1,000-10,000 人 | ~3,000 萬 | 50-500 GB | **$50-150** | 需要考慮優化 |
| 10,000+ 人 | 3 億+ | 500+ GB | **$200+** | 建議專業架構評估 |

### 其他平台參考

| 平台 | 免費方案上限 | 超出後價格 | 適合規模 |
|------|------------|-----------|---------|
| Vercel | 100GB 流量 | $20/月起 | 前端為主的專案 |
| Railway | $5/月額度 | $5-50/月 | 小型全端專案 |
| Render | 750 小時/月 | $7/月起 | 小型全端專案 |
| DigitalOcean | 無免費方案 | $5/月起 | 穩定的中型專案 |
| AWS Lightsail | 3 個月免費 | $3.5/月起 | 想用 AWS 但要簡單 |
| Firebase（全套） | 超大方免費額度 | 依用量計費 | Firebase 生態專案 |

### 域名與其他費用

| 項目 | 費用 | 說明 |
|------|------|------|
| .com 域名 | ~$10-15/年 | Namecheap、Google Domains |
| .dev 域名 | ~$12-15/年 | 自帶 HTTPS |
| SSL 憑證 | $0 | Let's Encrypt 免費（多數平台自動設定） |
| CDN | $0-10/月 | Cloudflare 免費方案通常夠用 |
| Email 服務 | $0-5/月 | Resend、SendGrid 有免費額度 |

---

# 📚 附錄 D：AI 協作最佳實踐

## D.1 給使用者的建議

```
【如何有效和 AI 溝通】

1. 一次只提一個需求
   ❌ 「幫我做登入、首頁、設定頁、還有上傳功能」
   ✅ 「現在先做登入功能」→ 完成後 →「接下來做首頁」

2. 描述你看到的問題，不要猜原因
   ❌ 「資料庫壞了」
   ✅ 「我按下儲存按鈕後，畫面顯示紅色的錯誤訊息『儲存失敗』」

3. 提供截圖或錯誤訊息
   AI 能從錯誤訊息中快速找到問題，比口頭描述快 10 倍

4. 對 AI 的修改保持耐心
   程式開發本來就是「寫 → 測 → 改 → 再測」的循環，
   第一次做對比第一次就完美更重要
```

## D.2 給 AI 的行為準則

```
【AI 在本框架下的行為規範】

1. 先問後做
   □ 在寫程式前完成第二部分的確認流程
   □ 不確定使用者想法時，主動提問

2. 做一步報一步
   □ 每完成一個功能，告訴使用者做了什麼
   □ 更新 TODO.md 的進度
   □ 遇到問題時，先說明狀況再提出方案

3. 文件同步更新
   □ 改完程式 → 更新 CHANGELOG
   □ 遇到新坑 → 更新 SKILLLOG
   □ 架構變動 → 更新 ARCHITECTURE
   □ 新功能完成 → 更新 README

4. 安全第一
   □ 永遠不在程式碼中寫入真實的密鑰
   □ 任何使用者輸入都要驗證
   □ 上線前必須執行安全檢查清單

5. 錯誤處理透明化
   □ 出錯時先查 Log
   □ 找到原因後，向使用者解釋（用白話）
   □ 修復後記錄下來，避免重蹈覆轍

6. 保持可交接性
   □ 任何時候停下，另一個 AI 或人類都能從文件中接手
   □ 不依賴「只有這個對話知道」的上下文
   □ 所有重要決策都記錄在文件中
```

## D.3 AI 接手既有專案的標準流程

```
當一個新的 AI 被要求接手一個已經在開發中的專案時，應遵循：

1️⃣ 讀取 docs/ARCHITECTURE.md → 了解專案架構
2️⃣ 讀取 CHANGELOG.md → 了解最近修改了什麼
3️⃣ 讀取 TODO.md → 了解還有什麼待做
4️⃣ 讀取 docs/SKILLLOG.md → 了解踩過什麼坑
5️⃣ 向使用者確認：「我已經看完專案文件，目前的理解是 [概述]，你接下來想做什麼？」

如果以上文件不存在或不完整，AI 應先補齊文件再開始開發。
```

---

# 🔧 附錄 E：進階功能指南（備用）

> 以下功能不是每個專案都需要，但 AI 應該知道何時建議使用者加入。

## E.1 PWA（Progressive Web App）— 離線可用

```
什麼時候需要：
- 使用者會在沒有網路的地方使用（旅行、戶外、飛機上）
- 想要「加到手機桌面」的功能

注意事項（來自 Triplan 經驗）：
- Service Worker 一旦啟用，快取策略很難改
- 建議先做完所有功能再加 PWA，否則開發時會被快取困擾
- Triplan 曾因舊 Service Worker 導致更新不生效，最終先停用
```

## E.2 即時同步（Real-time Sync）

```
什麼時候需要：
- 多人同時編輯同一份資料（如 Google Docs）
- 需要即時通知（聊天、協作）

技術選項：
- Firestore onSnapshot()（文件監聽，Firestore 內建）
- WebSocket（自建即時通訊）
- Socket.io（WebSocket 的強化版，更容易用）
```

## E.3 多語言（i18n）

```
什麼時候需要：
- 使用者來自不同國家
- 未來可能拓展到海外市場

技術選項：
- vue-i18n（Vue 生態）
- react-intl（React 生態）
- next-intl（Next.js 專用）
```

## E.4 自動化測試

```
什麼時候需要：
- 專案越來越大，手動測試來不及
- 多人協作，怕改 A 壞 B

技術選項：
- Vitest / Jest（單元測試）
- Cypress / Playwright（端對端測試，模擬使用者操作）
- Supertest（API 測試）
```

## E.5 CI/CD 進階流程

```
什麼時候需要：
- 想要「推到 Git 就自動部署」
- 需要自動跑測試再部署

技術選項：
- GitHub Actions（與 GitHub 深度整合，免費額度充足）
- Google Cloud Build（與 GCP 深度整合）
- GitLab CI（與 GitLab 深度整合）

來自 Triplan 的流程：
Git push → GitHub Actions → Cloud Build → Docker 映像建置 → Cloud Run 部署
整個過程全自動，只要 push 程式碼就好。
```

---

# 📌 結語

本規格說明書基於 **Triplan 旅行規劃 App** 的完整開發經驗撰寫，
涵蓋從「零基礎使用者的第一個問題」到「部署上線後的維運監控」的完整生命週期。

**核心理念**：
1. **先問後做**：AI 不應該在不了解需求的情況下就動手
2. **文件先行**：README 和 TODO 比程式碼更早產生
3. **日誌為王**：出錯時先看 Log，不要盲猜
4. **安全內建**：安全性不是上線前才加的，是從第一行程式碼就要有的
5. **可交接性**：任何時候停下，任何 AI 或人類都能從文件中接手

**使用方式**：
將這份文件在新專案開始時提交給 AI，說：
> 「請根據這份規格說明書，開始協助我開發專案。」

AI 就會按照流程，從訪談你的需求開始，一步步帶你完成整個專案。

---

> 📅 版本：2.0
> 📅 日期：2026-03-11
> 📅 基於：Triplan 專案開發經驗 + 系統規格說明書範本
> 📅 技術棧：通用（不限定任何技術）
