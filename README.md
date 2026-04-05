# LINE KM — 個人知識庫 Bot

> LINE Bot + Gemini AI 自動整理資訊碎片，存入 Google Drive，透過 Obsidian 檢索

## 功能

- **智能輸入**：支援文字、網址、圖片三種輸入方式
- **雙格式輸出**：同時生成 Obsidian Markdown + LINE 閱讀版
- **自動存檔**：處理完畢自動上傳至 Google Drive `KM-DATA` 資料夾
- **KM 流水號**：每筆筆記自動編號 KM001、KM002...，方便後續修改/刪除
- **語意檢索**：`#ask [問題]` 搜尋知識庫並以 AI 整理回答
- **修改/刪除**：`#修改 KMxxx 指示` 或 `#刪除 KMxxx`
- **併發安全**：同時丟多則訊息不會衝突，系統自動排隊處理

## 指令一覽

| 指令 | 說明 | 範例 |
|------|------|------|
| 直接傳文字 | AI 整理成知識筆記存檔 | `今天學到 RAG 的原理...` |
| 傳網址 | 擷取網頁內容整理 | `https://example.com/article` |
| 傳圖片 | OCR + 知識整理 | （直接傳送圖片） |
| `#ask 問題` | 搜尋知識庫回答 | `#ask 什麼是 RAG？` |
| `#修改 KMxxx 指示` | 修改指定筆記 | `#修改 KM003 請簡潔一點` |
| `#刪除 KMxxx` | 刪除指定筆記 | `#刪除 KM004` |
| `#help` | 顯示指令說明 | `#help` |

## 技術棧

| 類別 | 技術 | 用途 |
|------|------|------|
| 語言 | Python 3.12 | 後端 |
| 框架 | FastAPI | Webhook + API |
| AI | Gemini Flash-Lite | 解析、分類、格式化 |
| 通訊 | LINE Messaging API | 使用者入口 |
| 儲存 | Google Drive | .md 檔案存放 |
| 同步 | Synology Cloud Sync | Drive → NAS |
| 檢索 | Obsidian | 本地知識庫瀏覽 |
| 部署 | GCP Cloud Run | 容器化部署 |

---

## 從零開始部署教學

以下是完整的 API 開通與設定流程。每一步都是必要的，請按順序操作。

### Step 1：建立 GCP 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點選上方專案選擇器 → **「新增專案」**
3. 輸入專案名稱（例如 `line-km`），點選**建立**
4. **⚠️ 重要：連結帳單帳戶**
   - 前往 [帳單設定](https://console.cloud.google.com/billing/linkedaccount)
   - 選擇或建立帳單帳戶並連結
   - **不連結帳單就無法啟用任何 API**（這是最常遺漏的步驟）

### Step 2：啟用所需 GCP API（共 4 個）

在 GCP Console 左側選單 → **API 和服務** → **啟用 API 和服務**，搜尋並啟用以下 4 個 API：

| API 名稱 | 用途 | 啟用連結 |
|----------|------|----------|
| Google Drive API | 檔案上傳與搜尋 | [啟用](https://console.cloud.google.com/apis/api/drive.googleapis.com) |
| Cloud Run Admin API | 部署容器 | [啟用](https://console.cloud.google.com/apis/api/run.googleapis.com) |
| Cloud Build API | Docker 建置 | [啟用](https://console.cloud.google.com/apis/api/cloudbuild.googleapis.com) |
| Artifact Registry API | Docker Image 儲存 | [啟用](https://console.cloud.google.com/apis/api/artifactregistry.googleapis.com) |

> 也可以用 CLI 一次啟用：
> ```bash
> gcloud services enable drive.googleapis.com run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
> ```

### Step 3：建立 Google OAuth 2.0 憑證（給 Google Drive 用）

1. 前往 [API 憑證頁面](https://console.cloud.google.com/apis/credentials)
2. 點選 **「建立憑證」** → **「OAuth 用戶端 ID」**
3. 如果是首次，系統會要求先設定 **OAuth 同意畫面**：
   - 使用者類型選 **「外部」**
   - 填寫應用程式名稱（例如 `line km`）
   - 支援電子郵件填你自己的 Gmail
   - 範圍（Scope）可以先跳過
   - **⚠️ 關鍵步驟：加入測試使用者**
     - 在「Audience（目標對象）」→「Test users（測試使用者）」
     - 點選 **「Add Users」**，輸入你的 Gmail（例如 `yourname@gmail.com`）
     - **不加測試使用者，OAuth 授權會出現 403 錯誤「已封鎖存取權」**
4. 回到憑證頁面 → 建立 OAuth 用戶端 ID
   - 應用程式類型選 **「桌面應用程式」**
   - 建立後會顯示 **Client ID** 和 **Client Secret**，複製到 `auth.md`

### Step 4：建立 LINE Bot

1. 前往 [LINE Developers Console](https://developers.line.biz/console/)
2. 建立 Provider → 建立 **Messaging API Channel**
3. 在 Channel 設定頁面取得：
   - **Channel Secret**（在 Basic settings 頁面）
   - **Channel Access Token**（在 Messaging API 頁面，點 Issue 生成）
4. 複製到 `auth.md`

### Step 5：取得 Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/apikey)
2. 點選 **「Create API Key」**
3. 選擇你的 GCP 專案
4. 複製 API Key 到 `auth.md`

### Step 6：準備 Google Drive

1. 在你的 Google Drive 中建立資料夾 **`KM-DATA`**
2. 這個資料夾將作為所有知識筆記的儲存位置

### Step 7：安裝依賴與 OAuth 授權

```bash
pip install -r requirements.txt
python scripts/oauth_setup.py
```

- 瀏覽器會開啟 Google 登入頁面，選擇你的帳號並授權
- 腳本會自動將 **Refresh Token** 和 **KM-DATA Folder ID** 寫入 `auth.md`

> ⚠️ 如果出現「已封鎖存取權」403 錯誤：
> 回到 Step 3，確認你的 Gmail 已加入 OAuth 同意畫面的測試使用者名單

### Step 8：部署至 Cloud Run

```bash
# 安裝 gcloud CLI（若尚未安裝）：https://cloud.google.com/sdk/docs/install

# 設定專案
gcloud config set project 你的專案ID

# 產生 env.yaml（從 auth.md 萃取環境變數）
python scripts/gen_env_yaml.py

# 部署
gcloud run deploy line-kb-bot \
  --source . \
  --region asia-east1 \
  --allow-unauthenticated \
  --env-vars-file=env.yaml \
  --memory=512Mi \
  --timeout=60 \
  --max-instances=1 \
  --quiet
```

部署成功後會顯示 Service URL，例如：
`https://line-kb-bot-xxxxx.asia-east1.run.app`

### Step 9：掛上 LINE Webhook

1. 回到 [LINE Developers Console](https://developers.line.biz/console/)
2. 進入你的 Channel → Messaging API
3. Webhook URL 填入：`你的Cloud Run URL/webhook`
4. 開啟 **Use webhook**
5. 點 **Verify** 確認連線

### Step 10：取得你的 LINE User ID

1. 用 LINE 傳送任意訊息給 Bot
2. 查看 Cloud Run logs：
   ```bash
   gcloud run services logs read line-kb-bot --region=asia-east1 --limit=20
   ```
3. 找到 `ACCEPTED: user_id=Uxxxxxxxxx`，複製 User ID
4. 填入 `auth.md` 的 `ALLOWED_USER_IDS=`
5. 重新產生 env.yaml 並更新部署：
   ```bash
   python scripts/gen_env_yaml.py
   gcloud run services update line-kb-bot --region=asia-east1 --env-vars-file=env.yaml --quiet
   ```

---

## 踩坑紀錄與注意事項

### GCP 帳單未連結
- **症狀**：啟用 API 時報錯 `UREQ_PROJECT_BILLING_NOT_FOUND`
- **原因**：GCP 專案必須連結帳單帳戶才能使用任何付費 API
- **解法**：到 GCP Console → 帳單 → 連結帳單帳戶

### Google OAuth 403「已封鎖存取權」
- **症狀**：OAuth 授權時瀏覽器顯示「已封鎖存取權：XXX 未完成 Google 驗證程序」
- **原因**：OAuth 同意畫面為「測試中」狀態，未將自己的 Gmail 加入測試使用者
- **解法**：GCP Console → OAuth 同意畫面 → Audience → Test users → 加入你的 Gmail

### Google Drive API 未啟用
- **症狀**：OAuth 授權成功但搜尋 KM-DATA 資料夾時報 403
- **原因**：啟用了 OAuth 但忘記啟用 Google Drive API
- **解法**：GCP Console → API → 搜尋 Google Drive API → 啟用

### #ask 搜尋不到任何內容
- **症狀**：`#ask` 指令總是回覆「在知識庫中沒有找到相關內容」
- **原因**：上傳檔案時 mimeType 使用 `text/markdown`，Google Drive 不索引此格式的全文
- **解法**：改用 `text/plain` 作為上傳 mimeType（檔名仍為 .md）
- **補充**：即使修正 mimeType，新上傳的檔案仍需數分鐘才能被 Google 索引。系統已加入回退策略：fullText 搜不到時自動讀取最近 10 筆筆記讓 AI 判斷

### gcloud deploy 互動提示導致中斷
- **症狀**：部署時卡在互動式確認提示（例如 "Do you want to continue?"）
- **解法**：加上 `--quiet` 參數跳過所有確認

### API 啟用後速率限制
- **症狀**：啟用 API 後立即部署報 `Quota exceeded for Mutate requests`
- **原因**：剛啟用的 API 有短暫的速率限制
- **解法**：等待 30 秒後重試

---

## 專案結構

```
├── app/
│   ├── main.py          # FastAPI 主程式、LINE Webhook、訊息路由
│   ├── gemini_client.py # Gemini API（文字/URL/圖片/修改/問答）
│   ├── gdrive_client.py # Google Drive（上傳/搜尋/修改/刪除/KM流水號）
│   └── prompts.py       # System Prompts + #help 文字
├── config/
│   └── settings.py      # auth.md 解析（env var 優先，支援 Cloud Run）
├── scripts/
│   └── oauth_setup.py   # OAuth 首次授權（自動寫入 Refresh Token）
├── auth.md              # 🔒 所有機密（gitignored，嚴禁上傳）
├── auth.example.md      # 機密範本（可上傳）
├── env.yaml             # 🔒 Cloud Run 環境變數（gitignored）
├── Dockerfile           # Cloud Run 部署用
└── requirements.txt     # Python 依賴
```

## 安全性

- 所有 API Key 統一管理於 `auth.md`（已加入 `.gitignore`）
- Cloud Run 環境變數檔 `env.yaml` 同樣 gitignored
- LINE Webhook 簽名驗證
- User ID 白名單過濾（僅允許指定使用者）
- Google Drive 操作嚴格限定在 KM-DATA 資料夾
- KM ID 指定操作時驗證檔案確實在 KM-DATA 資料夾內
- Google Drive 操作限定於 `KM-DATA` 資料夾

## 給 AI 的指引

如果你是接手的 AI 助手，請先閱讀：
1. `CHANGELOG.md` — 修改紀錄
2. `TODO.md` — 待辦事項
3. `spec.md` — 系統規格書
4. `instructions.md` — 開發憲章
