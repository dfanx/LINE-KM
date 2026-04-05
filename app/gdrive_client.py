"""Google Drive client — all operations restricted to KM-DATA folder."""

import asyncio
import logging
import re
from io import BytesIO

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from config.settings import Settings

logger = logging.getLogger(__name__)

TOKEN_URI = "https://oauth2.googleapis.com/token"


def _sanitize_query(query: str) -> str:
    """Sanitize search query to prevent injection in Drive API query string."""
    return query.replace("\\", "").replace("'", "").strip()[:100]


class GDriveClient:
    """Google Drive client — all operations scoped to KM-DATA folder only."""

    def __init__(self, settings: Settings) -> None:
        self.folder_id = settings.km_data_folder_id
        creds = Credentials(
            token=None,
            refresh_token=settings.google_refresh_token,
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            token_uri=TOKEN_URI,
        )
        self._service = build("drive", "v3", credentials=creds)

    # ─── KM ID management ────────────────────────────────────────────────

    async def get_next_km_id(self) -> str:
        """Scan KM-DATA folder for highest KMxxx number and return next."""

        def _scan() -> str:
            results = (
                self._service.files()
                .list(
                    q=f"'{self.folder_id}' in parents and trashed = false",
                    fields="files(name)",
                    pageSize=1000,
                )
                .execute()
            )
            max_num = 0
            for f in results.get("files", []):
                m = re.match(r"^KM(\d{3})_", f["name"])
                if m:
                    max_num = max(max_num, int(m.group(1)))
            return f"KM{max_num + 1:03d}"

        return await asyncio.to_thread(_scan)

    async def find_file_by_km_id(self, km_id: str) -> dict | None:
        """Find a file by KM ID prefix (e.g. 'KM003'). Returns {id, name} or None."""

        def _find() -> dict | None:
            safe_id = re.sub(r"[^A-Za-z0-9]", "", km_id)
            results = (
                self._service.files()
                .list(
                    q=(
                        f"'{self.folder_id}' in parents"
                        f" and name contains '{safe_id}_'"
                        f" and trashed = false"
                    ),
                    fields="files(id, name)",
                    pageSize=5,
                )
                .execute()
            )
            for f in results.get("files", []):
                if f["name"].startswith(f"{safe_id}_"):
                    return f
            return None

        return await asyncio.to_thread(_find)

    # ─── CRUD ────────────────────────────────────────────────────────────

    async def upload_markdown(self, filename: str, content: str) -> str:
        """Upload a .md file to KM-DATA folder. Returns file ID."""

        def _upload() -> str:
            file_metadata = {
                "name": filename,
                "parents": [self.folder_id],
                "mimeType": "text/plain",
            }
            media = MediaIoBaseUpload(
                BytesIO(content.encode("utf-8")),
                mimetype="text/plain",
            )
            result = (
                self._service.files()
                .create(body=file_metadata, media_body=media, fields="id, name")
                .execute()
            )
            logger.info("GDRIVE_UPLOAD: %s (id=%s)", result["name"], result["id"])
            return result["id"]

        return await asyncio.to_thread(_upload)

    async def search_files(self, query: str) -> list[dict]:
        """Search for files inside KM-DATA folder. Uses fullText first, falls back to listing recent files."""

        def _search() -> list[dict]:
            safe_q = _sanitize_query(query)
            # Strategy 1: fullText search (works after Google indexes the file)
            q = (
                f"'{self.folder_id}' in parents"
                f" and mimeType != 'application/vnd.google-apps.folder'"
                f" and trashed = false"
                f" and fullText contains '{safe_q}'"
            )
            results = (
                self._service.files()
                .list(
                    q=q,
                    fields="files(id, name, modifiedTime)",
                    orderBy="modifiedTime desc",
                    pageSize=5,
                )
                .execute()
            )
            files = results.get("files", [])
            if files:
                return files

            # Strategy 2: fallback — list recent files from folder
            logger.info("SEARCH_FALLBACK: fullText empty, listing recent files")
            q_all = (
                f"'{self.folder_id}' in parents"
                f" and trashed = false"
                f" and mimeType != 'application/vnd.google-apps.folder'"
            )
            results = (
                self._service.files()
                .list(
                    q=q_all,
                    fields="files(id, name, modifiedTime)",
                    orderBy="modifiedTime desc",
                    pageSize=10,
                )
                .execute()
            )
            return results.get("files", [])

        return await asyncio.to_thread(_search)

    async def read_file_content(self, file_id: str) -> str:
        """Read file content — verifies file is inside KM-DATA folder first."""

        def _read() -> str:
            meta = (
                self._service.files()
                .get(fileId=file_id, fields="parents")
                .execute()
            )
            if self.folder_id not in meta.get("parents", []):
                raise PermissionError(f"File {file_id} is not in KM-DATA folder")

            data = self._service.files().get_media(fileId=file_id).execute()
            return data.decode("utf-8")

        return await asyncio.to_thread(_read)

    async def update_file(self, file_id: str, new_filename: str, content: str) -> None:
        """Update file content and name in KM-DATA folder."""

        def _update():
            meta = (
                self._service.files()
                .get(fileId=file_id, fields="parents")
                .execute()
            )
            if self.folder_id not in meta.get("parents", []):
                raise PermissionError(f"File {file_id} is not in KM-DATA folder")

            media = MediaIoBaseUpload(
                BytesIO(content.encode("utf-8")),
                mimetype="text/plain",
            )
            self._service.files().update(
                fileId=file_id,
                body={"name": new_filename},
                media_body=media,
            ).execute()
            logger.info("GDRIVE_UPDATE: %s (id=%s)", new_filename, file_id)

        await asyncio.to_thread(_update)

    async def delete_file(self, file_id: str) -> None:
        """Move file to trash — verifies file is in KM-DATA folder first."""

        def _delete():
            meta = (
                self._service.files()
                .get(fileId=file_id, fields="parents, name")
                .execute()
            )
            if self.folder_id not in meta.get("parents", []):
                raise PermissionError(f"File {file_id} is not in KM-DATA folder")

            self._service.files().update(
                fileId=file_id, body={"trashed": True}
            ).execute()
            logger.info("GDRIVE_DELETE: %s (id=%s)", meta["name"], file_id)

        await asyncio.to_thread(_delete)
