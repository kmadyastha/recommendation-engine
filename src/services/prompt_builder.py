"""Assemble LLM prompts from templates and request context."""

import json
from pathlib import Path

from src.config import PROJECT_ROOT
from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant

PROMPTS_DIR = PROJECT_ROOT / "prompts"
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system.txt"
USER_TEMPLATE_PATH = PROMPTS_DIR / "user_template.txt"


def load_prompt_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Prompt template not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def candidate_payload(restaurant: Restaurant) -> dict:
    return {
        "id": restaurant.id,
        "name": restaurant.name,
        "city": restaurant.city,
        "cuisine": restaurant.cuisine,
        "rating": restaurant.rating,
        "rating_count": restaurant.rating_count,
        "cost_for_two": restaurant.cost_for_two,
    }


def build_messages(
    preferences: UserPreferences,
    candidates: list[Restaurant],
    *,
    system_path: Path | None = None,
    user_template_path: Path | None = None,
) -> list[dict[str, str]]:
    system_prompt = load_prompt_file(system_path or SYSTEM_PROMPT_PATH)
    user_template = load_prompt_file(user_template_path or USER_TEMPLATE_PATH)

    preferences_json = json.dumps(
        {
            "location": preferences.location,
            "budget": preferences.budget,
            "cuisine": preferences.cuisine,
            "min_rating": preferences.min_rating,
            "additional_preferences": preferences.additional_preferences,
            "limit": preferences.limit,
        },
        ensure_ascii=False,
    )
    candidates_json = json.dumps(
        [candidate_payload(c) for c in candidates],
        ensure_ascii=False,
    )

    user_message = user_template.format(
        preferences_json=preferences_json,
        limit=preferences.limit,
        candidates_json=candidates_json,
    )

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]


def build_retry_message() -> dict[str, str]:
    return {
        "role": "user",
        "content": (
            "Your previous response was invalid. Return ONLY valid JSON matching the schema. "
            "Use restaurant_id values exactly from the candidate list. No markdown fences."
        ),
    }
