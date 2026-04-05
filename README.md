# LINE KM — 個人知識庫 Bot

> LINE Bot + Gemini AI 自動整理資訊碎片，存入 Google Drive，透過 Obsidian 檢索

## 功能

- **智能輸入**：支援文字、網址、圖片三種輸入方式
- **雙格式輸出**：同時生成 Obsidian Markdown + LINE 閱讀版
- **自動存檔**：處理完畢自動上傳至 Google Drive `KM-DATA` 資料夾
- **語意檢索**：`#ask [問題]` 搜尋知識庫並以 AI 整理回答

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

## 快速開始

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 設定機密

```bash
cp auth.example.md auth.md
# 編輯 auth.md，填入各項 API Key
```

### 3. Google Drive OAuth 授權（首次）

```bash
python scripts/oauth_setup.py
```

### 4. 本機測試

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. 部署至 Cloud Run

```bash
gcloud run deploy line-kb-bot --source . --region asia-east1 --allow-unauthenticated
```

## 專案結構

```
├── app/
│   ├── main.py          # FastAPI 主程式、LINE Webhook
│   ├── gemini_client.py # Gemini API 調用
│   ├── gdrive_client.py # Google Drive 上傳與檢索
│   └── prompts.py       # System Prompts
├── config/
│   └── settings.py      # auth.md 解析與設定管理
├── scripts/
│   └── oauth_setup.py   # OAuth 首次授權腳本
├── auth.md              # 🔒 機密（gitignored）
├── auth.example.md      # 機密範本
├── Dockerfile           # Cloud Run 部署
└── requirements.txt     # Python 依賴
```

## 安全性

- 所有 API Key 統一管理於 `auth.md`（已加入 `.gitignore`）
- LINE Webhook 簽名驗證
- User ID 白名單過濾（僅允許指定使用者）
- Google Drive 操作限定於 `KM-DATA` 資料夾

## 給 AI 的指引

如果你是接手的 AI 助手，請先閱讀：
1. `CHANGELOG.md` — 修改紀錄
2. `TODO.md` — 待辦事項
3. `spec.md` — 系統規格書
4. `instructions.md` — 開發憲章
