系統開發規格書 (System Development Specification)
1. 系統概述 (Project Overview)
本系統旨在建立一個「低摩擦、自動化、數位主權」的個人知識庫。

入口：Line Bot (支援文字、網址、圖片)。

大腦：Gemini 3.1 Flash-Lite (負責解析、分類、格式化)。

儲存：Google Drive 

核心價值：利用 AI 處理資訊碎片，達成「輸入即整理，回傳即調用」。

2. 技術棧 (Tech Stack)
語言：Python 3.10+

Web 框架：FastAPI (部署於 GCP Cloud Run)

AI 模型：Gemini 3.1 Flash-Lite-Preview (Google AI Studio API)

通訊介面：Line Messaging API SDK

儲存介面：Google Drive API v3

同步機制：Synology Cloud Sync (NAS 端)

前端檢索：Obsidian (本地端)

3. 系統架構圖 (Architecture)
程式碼片段
graph TD
    A[使用者 Line] -->|傳送資訊| B[GCP Cloud Run - FastAPI]
    B -->|調用| C[Gemini 3.1 Flash-Lite]
    C -->|回傳 JSON| B
    B -->|回傳確認卡片| A
    A -->|確認存檔| B
    B -->|寫入 .md| D[Google Drive]
    D -->|同步| E[Synology NAS / Obsidian]
    A -->|#ask 指令| B
    B -->|語意檢索| D
4. 核心功能規格 (Core Features)
A. 智能輸入處理 (Ingestion)
文字：直接進行摘要與邏輯提取。

網址：抓取 Meta Data 或網頁內容進行深度總結。

圖片：利用 Vision 能力進行 OCR 與內容理解。

B. 雙格式輸出 (Dual-Output Strategy)
AI 必須同時產出兩種格式以解決閱讀痛點：

Obsidian Markdown：包含 YAML 標籤與 Callout 語法。

Line Display Text：去除符號，使用 Emoji 視覺化，適合手機閱讀。

C. 語意檢索 (#ask)
使用者輸入 #ask [關鍵字或問題]。

系統檢索 Google Drive 內容，並由 AI 重新整理成「簡明 Line 版」回答。

5. Prompt Engineering (系統核心指令)
系統提示詞 (System Prompt)：

Plaintext
Role: 你是知識工程師，負責將碎片化資訊轉化為 Obsidian 格式與 Line 閱讀格式。
Output Format: 請嚴格輸出 JSON 格式，包含以下欄位：
{
  "title": "標題",
  "markdown_content": "--- \n date: {{DATE}} \n tags: [] \n --- \n # 標題 \n > [!ABSTRACT] 摘要 \n ### 💡技術核心 \n ...",
  "line_display": "📅 日期 \n 💡 核心摘要 \n 🚀 技術重點 \n ...",
  "suggested_filename": "YYYY-MM-DD_Title.md",
  "importance": 1-5
}
Constraints:
- 使用繁體中文。
- Markdown 必須包含 YAML Frontmatter。
- Line 格式嚴禁使用 #, *, > 等符號，改用 Emoji。
6. 資料架構與儲存規範 (Data Schema)
Obsidian Markdown 模板：
Markdown
---
date: 2026-04-05
tags: [AI/工具, 開發/Workflow]
source: "https://..."
category: 技術
importance: 4
---

# {{TITLE}}

> [!ABSTRACT] 核心摘要
> 一句話總結資訊。

### 💡 技術與觀念核心
- 重點一
- 重點二

---
[完整資訊請參考 Source]
7. VS Code 專案目錄結構
建議在 VS Code 中建立以下結構：

Plaintext
📂 line-kb-bot/
├── 📂 app/
│   ├── main.py          # FastAPI 主程式、Line Webhook
│   ├── gemini_client.py # 處理 Gemini API 調用
│   ├── gdrive_client.py # 處理 Google Drive 上傳與檢索
│   └── prompts.py       # 存放 System Prompts
├── 📂 config/
│   └── settings.py      # 讀取環境變數 (API Keys)
├── .env                 # 存放秘鑰 (不可上傳 git)
├── Dockerfile           # 用於部署至 GCP Cloud Run
└── requirements.txt     # 相依套件 (fastapi, google-generativeai, line-bot-sdk)
8. 實作路徑 (Roadmap)

撰寫程式後，全程使用本機的google cloud cli自動運行及上傳，若是遇到需要選擇或是人工操作時，你會列出詳細步驟協助我一步一步跟著你的指令完成

9. 全性考量


安全：使用 .env 管理 API KEY；在 Line Bot 加入 user_id 過濾機制，確保只有你能存取。