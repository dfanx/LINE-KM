"""Google Drive client — all operations restricted to KM-DATA folder."""

import asyncio
import logging
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

    async def upload_markdown(self, filename: str, content: str) -> str:
        """Upload a .md file to KM-DATA folder. Returns file ID."""

        def _upload() -> str:
            file_metadata = {
                "name": filename,
                "parents": [self.folder_id],
                "mimeType": "text/markdown",
            }
            media = MediaIoBaseUpload(
                BytesIO(content.encode("utf-8")),
                mimetype="text/markdown",
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
        """Search for files inside KM-DATA folder by content."""

        def _search() -> list[dict]:
            safe_q = _sanitize_query(query)
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
