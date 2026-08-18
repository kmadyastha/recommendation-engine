"""LLM client and recommendation engine."""

import json
import logging
import re
from typing import Protocol

from openai import OpenAI

from src.config import get_settings
from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.prompt_builder import build_messages, build_retry_message

logger = logging.getLogger(__name__)

MAX_RETRIES = 2


class LLMClient(Protocol):
    def complete(self, messages: list[dict[str, str]]) -> str: ...


class OpenAILLMClient:
    """OpenAI-compatible chat completion client (works with OpenAI, Groq, etc.)."""

    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.3,
        timeout: float = 60.0,
        base_url: str | None = None,
    ) -> None:
        client_kwargs: dict = {"api_key": api_key, "timeout": timeout}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = OpenAI(**client_kwargs)
        self._model = model
        self._temperature = temperature

    def complete(self, messages: list[dict[str, str]]) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                response_format={"type": "json_object"},
            )
        except Exception:
            # Groq and some providers may not support json_object mode
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
            )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty LLM response")
        return content


def strip_json_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def parse_llm_response(raw: str) -> dict:
    cleaned = strip_json_fences(raw)
    data = json.loads(cleaned)

    if not isinstance(data, dict):
        raise ValueError("LLM response must be a JSON object")

    recommendations = data.get("recommendations")
    if not isinstance(recommendations, list):
        raise ValueError("LLM response missing recommendations array")

    return data


class RecommendationEngine:
    """Call LLM to rank candidates and generate explanations."""

    def __init__(self, client: LLMClient | None = None) -> None:
        settings = get_settings()
        if client is not None:
            self._client = client
        elif settings.llm_api_key:
            self._client = OpenAILLMClient(
                api_key=settings.llm_api_key,
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                base_url=settings.llm_base_url,
            )
        else:
            self._client = None

    @property
    def is_available(self) -> bool:
        return self._client is not None

    def recommend(
        self,
        preferences: UserPreferences,
        candidates: list[Restaurant],
    ) -> dict:
        if not self._client:
            raise RuntimeError("LLM client not configured")

        messages = build_messages(preferences, candidates)
        last_error: Exception | None = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                raw = self._client.complete(messages)
                parsed = parse_llm_response(raw)
                logger.info("LLM recommendation succeeded on attempt %d", attempt + 1)
                return parsed
            except Exception as exc:
                last_error = exc
                logger.warning("LLM attempt %d failed: %s", attempt + 1, exc)
                if attempt < MAX_RETRIES:
                    messages = messages + [build_retry_message()]

        raise RuntimeError(f"LLM failed after {MAX_RETRIES + 1} attempts: {last_error}")
