Plan: LINE KM 個人知識庫 Bot
使用者透過 LINE 傳送文字/網址/圖片，Gemini 3.1 Flash-Lite 自動解析並生成 Obsidian Markdown + LINE 閱讀格式雙輸出，自動存入個人 Google Drive，並支援 #ask 語意檢索。全程使用 gcloud CLI 部署到 Cloud Run。

Phase 1: 專案初始化與基礎建設（Step 1-3）
建立專案目錄結構 — 按 spec.md 第7節建立 line-kb-bot/ 資料夾，含 app/main.py, app/gemini_client.py, app/gdrive_client.py, app/prompts.py, config/settings.py，以及 .env.example, .gitignore, Dockerfile, requirements.txt, README.md, TODO.md, CHANGELOG.md, log.md
環境配置 — 使用 pydantic-settings 管理環境變數（LINE Token、Gemini API Key、OAuth credentials 等），requirements.txt 包含 fastapi, uvicorn, line-bot-sdk, google-generativeai, google-api-python-client, google-auth-oauthlib, httpx, python-dotenv
Dockerfile & Cloud Run 適配 — Python slim image，健康檢查端點 /health，PORT 環境變數綁定
Phase 2: 核心服務模組（Step 4-6）
Gemini Client — 封裝 process_text(), process_url(), process_image(), ask_knowledge() 四個方法，統一回傳 JSON（title, markdown_content, line_display, suggested_filename, importance）
System Prompt — 按 spec.md 第5節定義知識工程師角色指令，嚴格約束 JSON 輸出格式、繁體中文、YAML Frontmatter、LINE Emoji 規範
Google Drive Client — OAuth 2.0 認證，實作上傳 .md、全文檢索 fullText contains、讀取檔案內容，自動建立 KnowledgeBase/ 根資料夾
Phase 3: LINE Bot Webhook 整合（Step 7-8）
FastAPI 主程式 — LINE Webhook signature 驗證、User ID 白名單過濾、事件路由（TextMessage 判斷 #ask 或一般輸入、ImageMessage 走圖片處理）、結構化 logging
自動存檔 + 回傳預覽 — 收到訊息 → Gemini 處理 → 自動上傳 .md 到 Drive → LINE 回傳 line_display 預覽 + 存檔確認
Phase 4: 語意檢索（Step 9）
#ask 指令 — 解析 #ask [問題]，Google Drive 全文搜尋相關 .md，取前5篇內容送入 Gemini 重新整理，回傳簡明 LINE 版答案
Phase 5: OAuth 首次授權（Step 10，需人工操作）
Google OAuth 設定 — GCP Console 建立 OAuth Client ID → 下載 credentials.json → 執行本機授權腳本 → 儲存 refresh token 到 Cloud Run 環境變數。此步驟需人工在瀏覽器完成授權，會提供逐步指引
Phase 6: 安全性與部署（Step 11-12）
安全性 — Webhook 簽名驗證、User ID 白名單、所有密鑰走環境變數、輸入驗證（URL 格式、圖片大小）、錯誤不洩漏內部資訊
Cloud Run 部署 — gcloud run deploy 全 CLI 操作，設定環境變數，配置 LINE Bot Webhook URL 指向 Cloud Run
Relevant Files
[app/main.py] — FastAPI 主程式、Webhook 處理、User ID 過濾
[app/gemini_client.py] — Gemini API 調用（文字/URL/圖片/#ask）
[app/gdrive_client.py] — Google Drive OAuth 2.0、上傳、檢索
[app/prompts.py] — System Prompts 定義
[config/settings.py] — Pydantic Settings 環境變數管理
[Dockerfile] — Cloud Run 部署用映像檔
[requirements.txt] — Python 依賴套件
Verification
本機 uvicorn 啟動，GET /health 回 200
固定文字輸入測試 process_text()，驗證 JSON 欄位完整
OAuth 授權後上傳測試 .md 到 Google Drive
ngrok 本機測試 LINE Webhook：傳文字/URL/圖片，確認回傳格式正確
存入幾篇筆記後測試 #ask 檢索，確認回答相關
非白名單 user_id 發訊息被拒絕
Cloud Run 部署後 LINE Bot 端對端正常運作
Decisions
OAuth 2.0 存取個人 Google Drive（非 Service Account），首次需人工授權
自動存檔 模式，不做確認互動按鈕，直接處理+存檔+回傳預覽
URL 抓取 使用 httpx 簡單 HTTP GET（不做 JS 渲染）
#ask 檢索 用 Drive fullText contains + Gemini 重整，取前5篇
全程 gcloud CLI 部署，人工步驟會列出詳細指令
Further Considerations
Drive 資料夾結構 — 建議先平鋪存放於 KnowledgeBase/，靠 Obsidian tags 分類管理，簡單優先。如需按 category 分子資料夾可後續擴充。
Refresh Token 存放 — 先用 Cloud Run 環境變數，後續可遷移至 GCP Secret Manager 提升安全性。
SPA 網頁抓取 — httpx 無法渲染 JS，對 SPA 頁面只能抓 meta data。如有此需求，未來可加 headless browser。