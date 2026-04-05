# 📝 CHANGELOG — LINE KM 知識庫 Bot

## 2026-04-05 - v0.1.0 專案初始化

### 新增
- **專案架構**：FastAPI + LINE Bot + Gemini + Google Drive 完整架構
- **auth.md 機密管理**：取代 .env，所有金鑰統一管理於 auth.md（gitignored）
- **app/gemini_client.py**：Gemini API 封裝，支援文字/URL/圖片處理 + #ask 語意檢索
- **app/gdrive_client.py**：Google Drive OAuth 2.0，所有操作限定 KM-DATA 資料夾
- **app/main.py**：LINE Webhook 處理，簽名驗證 + User ID 白名單 + 事件路由
- **app/prompts.py**：知識工程師 System Prompt，雙格式輸出規範
- **config/settings.py**：auth.md 解析器，環境變數優先（Cloud Run 相容）
- **scripts/oauth_setup.py**：OAuth 首次授權腳本（自動寫入 refresh token + folder ID）
- **Dockerfile**：Python 3.12 slim，Cloud Run 適配

### 架構決策
- **機密管理**：auth.md > .env — 可讀性更好，Markdown 格式便於維護
- **Google Drive**：OAuth 2.0（個人 Drive），程式碼層面限定 KM-DATA 資料夾
- **確認流程**：自動存檔 + 回傳 LINE 預覽，零摩擦體驗
- **LINE 回覆**：使用 httpx 直接呼叫 LINE API（比 SDK async client 更輕量）
