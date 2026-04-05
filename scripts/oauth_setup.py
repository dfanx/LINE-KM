"""
Google Drive OAuth 2.0 首次授權腳本

使用方式：
    python scripts/oauth_setup.py

功能：
1. 開啟瀏覽器完成 Google 帳號授權
2. 取得 Refresh Token 並自動寫入 auth.md
3. 搜尋 KM-DATA 資料夾 ID 並自動寫入 auth.md
"""

import re
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

AUTH_MD_PATH = Path(__file__).resolve().parent.parent / "auth.md"
SCOPES = ["https://www.googleapis.com/auth/drive"]


def _load_config() -> dict[str, str]:
    config: dict[str, str] = {}
    if not AUTH_MD_PATH.exists():
        print("❌ auth.md 不存在！請先複製 auth.example.md 為 auth.md 並填入 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET")
        sys.exit(1)

    for line in AUTH_MD_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ">", "`", "-", "[")):
            continue
        match = re.match(r"^([A-Z][A-Z0-9_]+)=(.+)$", line)
        if match:
            config[match.group(1)] = match.group(2).strip()
    return config


def _update_auth_md(key: str, value: str) -> None:
    """Update or add a KEY=VALUE pair in auth.md."""
    content = AUTH_MD_PATH.read_text(encoding="utf-8")
    pattern = re.compile(rf"^{re.escape(key)}=.*$", re.MULTILINE)

    if pattern.search(content):
        content = pattern.sub(f"{key}={value}", content)
    else:
        content += f"\n{key}={value}\n"

    AUTH_MD_PATH.write_text(content, encoding="utf-8")
    print(f"  ✅ 已寫入 {key} 到 auth.md")


def main():
    print("🔐 Google Drive OAuth 2.0 授權設定\n")

    config = _load_config()
    client_id = config.get("GOOGLE_CLIENT_ID", "")
    client_secret = config.get("GOOGLE_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("❌ 請先在 auth.md 中填入 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET")
        print("   取得方式：GCP Console → APIs & Services → Credentials → Create OAuth Client ID (Desktop)")
        sys.exit(1)

    # Step 1: OAuth authorization
    print("📋 步驟 1/3：開啟瀏覽器進行 Google 帳號授權...")

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": ["http://localhost"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=SCOPES,
    )

    credentials = flow.run_local_server(port=0)

    if not credentials.refresh_token:
        print("❌ 未取得 Refresh Token。")
        print("   請確認：")
        print("   1. OAuth Consent Screen 已設定")
        print("   2. 已將你的 Google 帳號加入測試使用者")
        print("   3. 若之前授權過，請至 https://myaccount.google.com/permissions 撤銷後重試")
        sys.exit(1)

    # Step 2: Save refresh token
    print("\n📋 步驟 2/3：儲存 Refresh Token...")
    _update_auth_md("GOOGLE_REFRESH_TOKEN", credentials.refresh_token)

    # Step 3: Find KM-DATA folder
    print("\n📋 步驟 3/3：搜尋 KM-DATA 資料夾...")
    service = build("drive", "v3", credentials=credentials)
    results = (
        service.files()
        .list(
            q="name = 'KM-DATA' and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
            fields="files(id, name)",
            pageSize=5,
        )
        .execute()
    )

    folders = results.get("files", [])

    if not folders:
        print("  ⚠️ 找不到名為 'KM-DATA' 的資料夾。")
        folder_id = input("  請手動輸入 KM-DATA 資料夾的 ID（從 Drive URL 中取得）：").strip()
    elif len(folders) == 1:
        folder_id = folders[0]["id"]
        print(f"  ✅ 找到 KM-DATA 資料夾：{folder_id}")
    else:
        print("  找到多個 KM-DATA 資料夾：")
        for i, f in enumerate(folders):
            print(f"    [{i + 1}] {f['name']} (ID: {f['id']})")
        choice = int(input("  請選擇（輸入數字）：")) - 1
        folder_id = folders[choice]["id"]

    _update_auth_md("KM_DATA_FOLDER_ID", folder_id)

    print("\n🎉 授權設定完成！")
    print("   啟動 Bot：uvicorn app.main:app --reload --port 8000")


if __name__ == "__main__":
    main()
