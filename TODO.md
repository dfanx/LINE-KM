# 📋 TODO — LINE KM 知識庫 Bot

> 最後更新：2026-04-05
> 總進度：Phase 1 完成

## 🟢 Phase 1：基礎建設
- [x] 專案目錄結構
- [x] 環境配置（requirements.txt, settings.py）
- [x] auth.md 機密管理
- [x] Dockerfile
- [x] 核心模組（Gemini / Drive / LINE）
- [ ] Git 初始化

## 🟡 Phase 2：OAuth 與本機測試
- [ ] GCP 建立 OAuth Client ID
- [ ] 執行 oauth_setup.py 授權
- [ ] 填入 auth.md（LINE Token, Gemini Key, User ID）
- [ ] 本機 uvicorn 啟動測試
- [ ] ngrok 本機測試 LINE Webhook

## 🔵 Phase 3：部署上線
- [ ] gcloud run deploy
- [ ] 設定 Cloud Run 環境變數
- [ ] LINE Bot Webhook URL 設定
- [ ] 端對端測試

## 🟣 Phase 4：驗證與優化
- [ ] 文字輸入 → 自動存檔測試
- [ ] URL 輸入 → 網頁摘要測試
- [ ] 圖片輸入 → OCR 測試
- [ ] #ask 語意檢索測試
- [ ] 安全性檢查（非白名單 User ID 被拒絕）

## 🐛 已知問題

| 問題 | 嚴重度 | 狀態 |
|------|--------|------|
| 暫無 | - | - |
