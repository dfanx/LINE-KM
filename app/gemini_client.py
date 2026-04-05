"""Gemini API client for knowledge processing."""

import json
import logging
import re
from urllib.parse import quote

from google import genai
from google.genai import types
import httpx
from bs4 import BeautifulSoup

from config.settings import Settings
from app.prompts import get_system_prompt, get_url_prompt, get_ask_prompt, get_revise_prompt, IMAGE_PROMPT

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self, settings: Settings) -> None:
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._model = settings.gemini_model
        self._system_prompt = get_system_prompt()

    def _parse_response(self, text: str) -> dict:
        """Parse JSON from Gemini response."""
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        result = json.loads(text)
        required = ["title", "markdown_content", "line_display", "suggested_filename", "importance"]
        missing = [k for k in required if k not in result]
        if missing:
            raise ValueError(f"Gemini response missing fields: {missing}")
        return result

    async def process_text(self, text: str) -> dict:
        """Process plain text input into knowledge note."""
        logger.info("GEMINI_PROCESS_TEXT: len=%d", len(text))
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return self._parse_response(response.text)

    async def process_url(self, url: str) -> dict:
        """Fetch URL content, then process into knowledge note."""
        logger.info("GEMINI_PROCESS_URL: %s", url)
        page_title, content = await self._fetch_url(url)
        prompt = get_url_prompt(url=url, page_title=page_title, content=content)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return self._parse_response(response.text)

    async def process_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
        """Process image with Vision for OCR and content understanding."""
        logger.info("GEMINI_PROCESS_IMAGE: size=%d mime=%s", len(image_bytes), mime_type)
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=[IMAGE_PROMPT, image_part],
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return self._parse_response(response.text)

    async def ask_knowledge(self, question: str, context: str) -> str:
        """Answer a question based on knowledge base context."""
        logger.info("GEMINI_ASK: q=%s", question[:50])
        prompt = get_ask_prompt(context)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=f"{prompt}\n\n使用者問題：{question}",
            config=types.GenerateContentConfig(temperature=0.5),
        )
        return response.text

    async def revise_knowledge(self, instruction: str, original_content: str) -> dict:
        """Revise existing knowledge note based on user instruction."""
        logger.info("GEMINI_REVISE: instruction=%s", instruction[:50])
        prompt = get_revise_prompt(instruction, original_content)
        response = await self._client.aio.models.generate_content(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self._system_prompt,
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        return self._parse_response(response.text)

    async def _fetch_url(self, url: str) -> tuple[str, str]:
        """Fetch and extract readable content from a URL. Never raises — returns fallback on failure."""
        # Try regular HTML fetch
        try:
            return await self._fetch_html(url)
        except Exception as e:
            logger.warning("FETCH_HTML_FAILED: url=%s err=%s", url, e)

        # YouTube oEmbed fallback
        if "youtube.com" in url or "youtu.be" in url:
            try:
                return await self._fetch_youtube_oembed(url)
            except Exception as e:
                logger.warning("FETCH_OEMBED_FAILED: url=%s err=%s", url, e)

        # Last resort — let Gemini work with URL alone
        return url, f"（無法擷取該網頁的內容，請根據網址盡可能分析）\n網址：{url}"

    async def _fetch_html(self, url: str) -> tuple[str, str]:
        """Fetch and parse HTML content from a URL."""
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            resp = await client.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/131.0.0.0 Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
                },
            )
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else url

        # Extract og:description / meta description
        meta_desc = ""
        for attr in [{"property": "og:description"}, {"name": "description"}]:
            meta_tag = soup.find("meta", attrs=attr)
            if meta_tag and meta_tag.get("content"):
                meta_desc = str(meta_tag["content"])
                break

        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        if meta_desc:
            content = f"描述：{meta_desc}\n\n{content}"

        return title, content[:8000]

    async def _fetch_youtube_oembed(self, url: str) -> tuple[str, str]:
        """Fetch YouTube video metadata via oEmbed API."""
        oembed_url = f"https://www.youtube.com/oembed?url={quote(url, safe='')}&format=json"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(oembed_url)
            resp.raise_for_status()
            data = resp.json()

        title = data.get("title", "YouTube Video")
        author = data.get("author_name", "")
        return title, f"YouTube 影片\n標題：{title}\n作者：{author}\n網址：{url}"
