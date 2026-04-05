"""Google Drive client — all operations restricted to KM-DATA folder."""

import asyncio
import json
import logging
import re
from io import BytesIO

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

from config.settings import Settings

logger = logging.getLogger(__name__)

TOKEN_URI = "https://oauth2.googleapis.com/token"
INDEX_FILENAME = "_KM_INDEX.json"

# Lock to prevent concurrent KM ID assignment race condition
_km_id_lock = asyncio.Lock()


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
        """Scan KM-DATA folder for highest KMxxx number and return next. Uses lock to prevent race condition."""

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

        async with _km_id_lock:
            km_id = await asyncio.to_thread(_scan)
            return km_id

    async def upload_with_km_id(self, suggested_filename: str, content: str) -> tuple[str, str]:
        """Atomically assign KM ID and upload. Returns (km_id, full_filename)."""
        async with _km_id_lock:
            def _atomic():
                km_id = self._scan_max_km_id()
                filename = f"{km_id}_{suggested_filename}"
                file_id = self._do_upload(filename, content)
                self._index_upsert(km_id, file_id, filename, content)
                return km_id, filename
            return await asyncio.to_thread(_atomic)

    def _scan_max_km_id(self) -> str:
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

    # ─── Index management ────────────────────────────────────────────────

    def _find_index_file_id(self) -> str | None:
        results = (
            self._service.files()
            .list(
                q=(
                    f"'{self.folder_id}' in parents"
                    f" and name = '{INDEX_FILENAME}'"
                    f" and trashed = false"
                ),
                fields="files(id)",
                pageSize=1,
            )
            .execute()
        )
        files = results.get("files", [])
        return files[0]["id"] if files else None

    def _load_index_sync(self) -> dict | None:
        """Load index from Drive. Returns None if not found, dict otherwise."""
        file_id = self._find_index_file_id()
        if not file_id:
            return None
        data = self._service.files().get_media(fileId=file_id).execute()
        return json.loads(data.decode("utf-8"))

    def _save_index_sync(self, index: dict) -> None:
        """Save index to Drive. Creates or updates."""
        content = json.dumps(index, ensure_ascii=False, indent=2)
        media = MediaIoBaseUpload(
            BytesIO(content.encode("utf-8")),
            mimetype="application/json",
        )
        file_id = self._find_index_file_id()
        if file_id:
            self._service.files().update(fileId=file_id, media_body=media).execute()
        else:
            file_metadata = {
                "name": INDEX_FILENAME,
                "parents": [self.folder_id],
            }
            self._service.files().create(
                body=file_metadata, media_body=media, fields="id"
            ).execute()
        logger.info("INDEX_SAVED: entries=%d", len(index))

    @staticmethod
    def _extract_meta(content: str, filename: str) -> tuple[str, list[str], str]:
        """Extract title, tags, summary from markdown content."""
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else filename
        tags_match = re.search(r"tags:\s*\[(.+?)\]", content)
        tags = (
            [t.strip().strip("'\"") for t in tags_match.group(1).split(",")]
            if tags_match
            else []
        )
        summary = content[:300]
        return title, tags, summary

    def _index_upsert(self, km_id: str, file_id: str, filename: str, content: str) -> None:
        """Add or update an entry in the index. Call inside _km_id_lock or thread."""
        try:
            index = self._load_index_sync() or {}
            title, tags, summary = self._extract_meta(content, filename)
            index[km_id] = {
                "file_id": file_id,
                "filename": filename,
                "title": title,
                "tags": tags,
                "summary": summary,
            }
            self._save_index_sync(index)
        except Exception as e:
            logger.warning("INDEX_UPSERT_FAILED: km_id=%s err=%s", km_id, e)

    def _index_remove(self, km_id: str) -> None:
        """Remove an entry from the index."""
        try:
            index = self._load_index_sync() or {}
            if km_id in index:
                del index[km_id]
                self._save_index_sync(index)
        except Exception as e:
            logger.warning("INDEX_REMOVE_FAILED: km_id=%s err=%s", km_id, e)

    async def load_index(self) -> dict:
        """Load index for search. If not found, rebuilds from files."""
        index = await asyncio.to_thread(self._load_index_sync)
        if index is not None:
            return index
        logger.info("INDEX_NOT_FOUND: rebuilding from files")
        return await self.rebuild_index()

    async def rebuild_index(self) -> dict:
        """Rebuild index by scanning all KM files in folder."""

        def _rebuild() -> dict:
            results = (
                self._service.files()
                .list(
                    q=(
                        f"'{self.folder_id}' in parents"
                        f" and trashed = false"
                        f" and mimeType != 'application/vnd.google-apps.folder'"
                    ),
                    fields="files(id, name)",
                    pageSize=1000,
                )
                .execute()
            )
            index = {}
            for f in results.get("files", []):
                m = re.match(r"^(KM\d{3})_", f["name"])
                if not m:
                    continue
                km_id = m.group(1)
                try:
                    data = self._service.files().get_media(fileId=f["id"]).execute()
                    content = data.decode("utf-8")
                    title, tags, summary = self._extract_meta(content, f["name"])
                except Exception:
                    title, tags, summary = f["name"], [], ""
                index[km_id] = {
                    "file_id": f["id"],
                    "filename": f["name"],
                    "title": title,
                    "tags": tags,
                    "summary": summary,
                }
            self._save_index_sync(index)
            return index

        return await asyncio.to_thread(_rebuild)

    # ─── CRUD ────────────────────────────────────────────────────────────

    async def upload_markdown(self, filename: str, content: str) -> str:
        """Upload a .md file to KM-DATA folder. Returns file ID."""
        return await asyncio.to_thread(self._do_upload, filename, content)

    def _do_upload(self, filename: str, content: str) -> str:
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

            # Update index
            m = re.match(r"^(KM\d{3})_", new_filename)
            if m:
                self._index_upsert(m.group(1), file_id, new_filename, content)

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

            # Remove from index
            m = re.match(r"^(KM\d{3})_", meta.get("name", ""))
            if m:
                self._index_remove(m.group(1))

        await asyncio.to_thread(_delete)
