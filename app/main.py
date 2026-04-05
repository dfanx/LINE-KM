"""FastAPI main application — LINE Bot webhook handler."""

import logging
import re
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
import httpx

from linebot.v3 import WebhookParser
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent, ImageMessageContent

from config.settings import get_settings, Settings
from app.gemini_client import GeminiClient
from app.gdrive_client import GDriveClient
from app.prompts import HELP_TEXT

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("line-kb-bot")

# --- Global state (initialized in lifespan) ---
gemini: GeminiClient | None = None
gdrive: GDriveClient | None = None
parser: WebhookParser | None = None
_settings: Settings | None = None

LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_CONTENT_URL = "https://api-data.line.me/v2/bot/message/{message_id}/content"
URL_PATTERN = re.compile(r"^https?://\S+$")
KM_EDIT_PATTERN = re.compile(r"^#修改\s+(KM\d{3})\s+(.+)$", re.DOTALL)
KM_DELETE_PATTERN = re.compile(r"^#刪除\s+(KM\d{3})\s*$")


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    global gemini, gdrive, parser, _settings
    _settings = get_settings()

    missing = _settings.validate_core()
    if missing:
        logger.error("AUTH_MISSING: %s — check auth.md", missing)
        raise SystemExit(f"Missing required settings: {missing}")

    gemini = GeminiClient(_settings)
    gdrive = GDriveClient(_settings)
    parser = WebhookParser(channel_secret=_settings.line_channel_secret)
    logger.info("APP_START: Bot initialized")
    yield
    logger.info("APP_STOP: Shutting down")


app = FastAPI(lifespan=lifespan)


# ─── Health check ────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok"}


# ─── LINE Webhook ────────────────────────────────────────────────────────────

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()
    signature = request.headers.get("X-Line-Signature", "")

    try:
        events = parser.parse(body.decode("utf-8"), signature)
    except InvalidSignatureError:
        logger.warning("WEBHOOK_INVALID_SIG")
        raise HTTPException(status_code=403, detail="Invalid signature")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue

        user_id = event.source.user_id
        if _settings.allowed_user_ids and user_id not in _settings.allowed_user_ids:
            logger.warning("AUTH_DENIED: user_id=%s", user_id)
            continue

        logger.info("ACCEPTED: user_id=%s", user_id)
        background_tasks.add_task(_handle_message, event)

    return "OK"


# ─── Message routing ─────────────────────────────────────────────────────────

async def _handle_message(event: MessageEvent):
    trace = uuid.uuid4().hex[:8]
    reply_token = event.reply_token
    message = event.message

    try:
        if isinstance(message, TextMessageContent):
            text = message.text.strip()
            if text.lower() == "#help":
                await _reply(reply_token, HELP_TEXT)
            elif text.lower().startswith("#ask "):
                await _handle_ask(text[5:], reply_token, trace)
            elif (m := KM_EDIT_PATTERN.match(text)):
                await _handle_edit(m.group(1).upper(), m.group(2).strip(), reply_token, trace)
            elif (m := KM_DELETE_PATTERN.match(text)):
                await _handle_delete(m.group(1).upper(), reply_token, trace)
            elif URL_PATTERN.match(text):
                await _handle_url(text, reply_token, trace)
            else:
                await _handle_text(text, reply_token, trace)

        elif isinstance(message, ImageMessageContent):
            await _handle_image(message.id, reply_token, trace)

    except Exception as e:
        logger.error("PROCESS_ERROR: trace=%s error=%s", trace, str(e), exc_info=True)
        await _reply(reply_token, f"❌ 處理失敗，請稍後再試\n錯誤代碼：{trace}")


# ─── Handlers ────────────────────────────────────────────────────────────────

async def _handle_text(text: str, reply_token: str, trace: str):
    logger.info("HANDLE_TEXT: trace=%s len=%d", trace, len(text))
    result = await gemini.process_text(text)
    km_id, filename = await gdrive.upload_with_km_id(result["suggested_filename"], result["markdown_content"])
    await _reply(reply_token, _format_reply(result, km_id))
    logger.info("HANDLE_TEXT_DONE: trace=%s file=%s", trace, filename)


async def _handle_url(url: str, reply_token: str, trace: str):
    logger.info("HANDLE_URL: trace=%s url=%s", trace, url)
    result = await gemini.process_url(url)
    km_id, filename = await gdrive.upload_with_km_id(result["suggested_filename"], result["markdown_content"])
    await _reply(reply_token, _format_reply(result, km_id))
    logger.info("HANDLE_URL_DONE: trace=%s file=%s", trace, filename)


async def _handle_image(message_id: str, reply_token: str, trace: str):
    logger.info("HANDLE_IMAGE: trace=%s msg_id=%s", trace, message_id)
    image_bytes, mime_type = await _download_content(message_id)
    result = await gemini.process_image(image_bytes, mime_type)
    km_id, filename = await gdrive.upload_with_km_id(result["suggested_filename"], result["markdown_content"])
    await _reply(reply_token, _format_reply(result, km_id))
    logger.info("HANDLE_IMAGE_DONE: trace=%s file=%s", trace, filename)


async def _handle_edit(km_id: str, instruction: str, reply_token: str, trace: str):
    logger.info("HANDLE_EDIT: trace=%s km_id=%s", trace, km_id)
    file_info = await gdrive.find_file_by_km_id(km_id)
    if not file_info:
        await _reply(reply_token, f"❌ 找不到編號 {km_id} 的筆記")
        return

    original = await gdrive.read_file_content(file_info["id"])
    result = await gemini.revise_knowledge(instruction, original)
    new_filename = f"{km_id}_{result['suggested_filename']}"
    await gdrive.update_file(file_info["id"], new_filename, result["markdown_content"])
    await _reply(reply_token, f"✏️ 已修改 {km_id}\n\n{result['line_display']}\n\n✅ 已更新：{new_filename}")
    logger.info("HANDLE_EDIT_DONE: trace=%s file=%s", trace, new_filename)


async def _handle_delete(km_id: str, reply_token: str, trace: str):
    logger.info("HANDLE_DELETE: trace=%s km_id=%s", trace, km_id)
    file_info = await gdrive.find_file_by_km_id(km_id)
    if not file_info:
        await _reply(reply_token, f"❌ 找不到編號 {km_id} 的筆記")
        return

    await gdrive.delete_file(file_info["id"])
    await _reply(reply_token, f"🗑️ 已刪除 {km_id}\n📄 {file_info['name']}")
    logger.info("HANDLE_DELETE_DONE: trace=%s file=%s", trace, file_info["name"])


async def _handle_ask(question: str, reply_token: str, trace: str):
    logger.info("HANDLE_ASK: trace=%s q=%s", trace, question[:50])
    files = await gdrive.search_files(question)

    if not files:
        await _reply(reply_token, "🔍 在知識庫中沒有找到相關內容。")
        return

    context_parts = []
    for f in files[:5]:
        try:
            content = await gdrive.read_file_content(f["id"])
            context_parts.append(f"📄 {f['name']}:\n{content}")
        except Exception as e:
            logger.warning("ASK_READ_ERROR: file=%s err=%s", f["name"], str(e))

    if not context_parts:
        await _reply(reply_token, "🔍 找到檔案但無法讀取內容，請稍後再試。")
        return

    context = "\n\n---\n\n".join(context_parts)
    answer = await gemini.ask_knowledge(question, context)
    await _reply(reply_token, answer)
    logger.info("HANDLE_ASK_DONE: trace=%s matched=%d", trace, len(files))


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _format_reply(result: dict, km_id: str) -> str:
    importance = min(int(result.get("importance", 3)), 5)
    return (
        f"{result['line_display']}\n\n"
        f"🏷️ 編號：{km_id}\n"
        f"✅ 已存檔：{km_id}_{result['suggested_filename']}\n"
        f"⭐ 重要度：{'⭐' * importance}"
    )


async def _reply(reply_token: str, text: str):
    """Send reply via LINE Messaging API."""
    if len(text) > 5000:
        text = text[:4950] + "\n\n⚠️ 內容過長，已截斷"

    async with httpx.AsyncClient() as client:
        await client.post(
            LINE_REPLY_URL,
            headers={
                "Authorization": f"Bearer {_settings.line_channel_access_token}",
                "Content-Type": "application/json",
            },
            json={
                "replyToken": reply_token,
                "messages": [{"type": "text", "text": text}],
            },
        )


async def _download_content(message_id: str) -> tuple[bytes, str]:
    """Download image/file content from LINE."""
    url = LINE_CONTENT_URL.format(message_id=message_id)
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            url,
            headers={"Authorization": f"Bearer {_settings.line_channel_access_token}"},
        )
        resp.raise_for_status()
        content_type = resp.headers.get("content-type", "image/jpeg")
        return resp.content, content_type
