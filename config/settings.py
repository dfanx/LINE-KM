"""Settings management — reads from auth.md (local) or environment variables (Cloud Run)."""

import os
import re
from pathlib import Path
from functools import lru_cache

_AUTH_PATH = Path(__file__).resolve().parent.parent / "auth.md"


def _parse_auth_md() -> dict[str, str]:
    """Parse KEY=VALUE pairs from auth.md, skipping markdown syntax lines."""
    config: dict[str, str] = {}
    if not _AUTH_PATH.exists():
        return config

    for line in _AUTH_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith(("#", ">", "`", "-", "[")):
            continue
        match = re.match(r"^([A-Z][A-Z0-9_]+)=(.+)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            if value:
                config[key] = value
    return config


class Settings:
    """Application settings — environment variables take precedence over auth.md."""

    def __init__(self) -> None:
        file_config = _parse_auth_md()

        def _get(key: str, default: str = "") -> str:
            return os.environ.get(key, file_config.get(key, default))

        self.line_channel_secret: str = _get("LINE_CHANNEL_SECRET")
        self.line_channel_access_token: str = _get("LINE_CHANNEL_ACCESS_TOKEN")
        self.gemini_api_key: str = _get("GEMINI_API_KEY")
        self.gemini_model: str = _get("GEMINI_MODEL", "gemini-2.0-flash-lite")
        self.google_client_id: str = _get("GOOGLE_CLIENT_ID")
        self.google_client_secret: str = _get("GOOGLE_CLIENT_SECRET")
        self.google_refresh_token: str = _get("GOOGLE_REFRESH_TOKEN")
        self.km_data_folder_id: str = _get("KM_DATA_FOLDER_ID")
        self.allowed_user_ids: set[str] = {
            uid.strip() for uid in _get("ALLOWED_USER_IDS").split(",") if uid.strip()
        }

    def validate_core(self) -> list[str]:
        """Return list of missing required settings."""
        required = {
            "LINE_CHANNEL_SECRET": self.line_channel_secret,
            "LINE_CHANNEL_ACCESS_TOKEN": self.line_channel_access_token,
            "GEMINI_API_KEY": self.gemini_api_key,
            "GOOGLE_REFRESH_TOKEN": self.google_refresh_token,
            "KM_DATA_FOLDER_ID": self.km_data_folder_id,
        }
        return [k for k, v in required.items() if not v]


@lru_cache
def get_settings() -> Settings:
    return Settings()
