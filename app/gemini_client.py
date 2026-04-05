"""Gemini API client for knowledge processing."""

import json
import logging
import re

import google.generativeai as genai
import httpx
from bs4 import BeautifulSoup

from config.settings import Settings
from app.prompts import get_system_prompt, get_url_prompt, get_ask_prompt, IMAGE_PROMPT

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self, settings: Settings) -> None:
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=get_system_prompt(),
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.3,
            ),
        )
        self.ask_model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            generation_config=genai.GenerationConfig(temperature=0.5),
        )

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
        response = await self.model.generate_content_async(text)
        return self._parse_response(response.text)

    async def process_url(self, url: str) -> dict:
        """Fetch URL content, then process into knowledge note."""
        logger.info("GEMINI_PROCESS_URL: %s", url)
        page_title, content = await self._fetch_url(url)
        prompt = get_url_prompt(url=url, page_title=page_title, content=content)
        response = await self.model.generate_content_async(prompt)
        return self._parse_response(response.text)

    async def process_image(self, image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
        """Process image with Vision for OCR and content understanding."""
        logger.info("GEMINI_PROCESS_IMAGE: size=%d mime=%s", len(image_bytes), mime_type)
        image_part = {"mime_type": mime_type, "data": image_bytes}
        response = await self.model.generate_content_async([IMAGE_PROMPT, image_part])
        return self._parse_response(response.text)

    async def ask_knowledge(self, question: str, context: str) -> str:
        """Answer a question based on knowledge base context."""
        logger.info("GEMINI_ASK: q=%s", question[:50])
        prompt = get_ask_prompt(context)
        response = await self.ask_model.generate_content_async(
            f"{prompt}\n\n使用者問題：{question}"
        )
        return response.text

    async def _fetch_url(self, url: str) -> tuple[str, str]:
        """Fetch and extract readable content from a URL."""
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            resp = await client.get(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; KnowledgeBot/1.0)"},
            )
            resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        title = soup.title.string.strip() if soup.title and soup.title.string else url

        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = str(meta_tag["content"])

        text = soup.get_text(separator="\n", strip=True)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        content = "\n".join(lines)

        if meta_desc:
            content = f"描述：{meta_desc}\n\n{content}"

        return title, content[:8000]
