"""Clean and normalize raw restaurant data."""

import json
import logging
import re
from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT
from src.models.restaurant import Restaurant

logger = logging.getLogger(__name__)

DEFAULT_ALIASES_PATH = PROJECT_ROOT / "data" / "config" / "city_aliases.json"

INVALID_RATING_TOKENS = frozenset(
    {
        "",
        "--",
        "new",
        "-",
        "nan",
        "none",
        "too few ratings",
        "not rated",
    }
)


def load_city_aliases(path: Path | None = None) -> dict[str, str]:
    aliases_path = path or DEFAULT_ALIASES_PATH
    with aliases_path.open(encoding="utf-8") as f:
        raw = json.load(f)
    return {str(k).strip().lower(): str(v).strip() for k, v in raw.items()}


def normalize_city(value: object, aliases: dict[str, str] | None = None) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None

    aliases = aliases or load_city_aliases()
    key = text.lower()
    if key in aliases:
        return aliases[key]

    # Title-case fallback for unknown cities
    return text.title()


def parse_cuisines(value: object) -> tuple[str, list[str]]:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "", []

    text = str(value).strip()
    if not text:
        return "", []

    tokens = [t.strip() for t in re.split(r"[,;/|]", text) if t.strip()]
    display = ", ".join(tokens)
    return display, tokens


def parse_cost(value: object) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) if value >= 0 else None

    text = str(value).strip().lower()
    if not text:
        return None

    # Extract first numeric token (handles "₹ 450", "450 for two", "300-500")
    match = re.search(r"(\d+(?:\.\d+)?)", text.replace(",", ""))
    if not match:
        return None
    return float(match.group(1))


def parse_rating(value: object) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        rating = float(value)
        if 0 <= rating <= 5:
            return rating
        return None

    text = str(value).strip().lower()
    if text in INVALID_RATING_TOKENS:
        return None

    try:
        rating = float(text)
    except ValueError:
        return None

    if 0 <= rating <= 5:
        return rating
    return None


def parse_rating_count(value: object) -> int:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return 0

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return max(0, int(value))

    text = str(value).strip().lower()
    if text in INVALID_RATING_TOKENS or not text:
        return 0

    # Handles "50+ ratings", "1K+ ratings", "1.5K ratings"
    k_match = re.search(r"([\d.]+)\s*k\+?\s*ratings?", text.replace(",", ""))
    if k_match:
        return max(0, int(float(k_match.group(1)) * 1000))

    match = re.search(r"(\d+)", text.replace(",", ""))
    if not match:
        return 0
    return int(match.group(1))


def make_restaurant_id(source_id: object, row_index: int, name: str, city: str) -> str:
    if source_id is not None and not (isinstance(source_id, float) and pd.isna(source_id)):
        text = str(source_id).strip()
        if text:
            return f"r_{text}_{row_index}"

    slug = re.sub(r"[^a-z0-9]+", "_", f"{name}_{city}".lower()).strip("_")
    return f"r_{slug}_{row_index}"


def preprocess_dataframe(
    df: pd.DataFrame,
    city_aliases: dict[str, str] | None = None,
) -> pd.DataFrame:
    """Transform mapped raw dataframe into normalized restaurant records."""
    city_aliases = city_aliases or load_city_aliases()
    records: list[dict] = []
    dropped_missing = 0
    duplicate_names = 0
    seen_name_city: set[tuple[str, str]] = set()

    for idx, row in df.iterrows():
        name = str(row.get("name", "")).strip()
        city = normalize_city(row.get("city"), city_aliases)

        if not name or not city:
            dropped_missing += 1
            continue

        name_city_key = (name.lower(), city.lower())
        if name_city_key in seen_name_city:
            duplicate_names += 1
        seen_name_city.add(name_city_key)

        cuisine_display, cuisines = parse_cuisines(row.get("cuisine"))
        cost = parse_cost(row.get("cost"))
        rating = parse_rating(row.get("rating"))
        rating_count = parse_rating_count(row.get("rating_count"))
        restaurant_id = make_restaurant_id(row.get("id"), int(idx), name, city)

        records.append(
            {
                "id": restaurant_id,
                "name": name,
                "city": city,
                "cuisine": cuisine_display,
                "cuisines": cuisines,
                "cost_for_two": cost,
                "rating": rating,
                "rating_count": rating_count,
            }
        )

    result = pd.DataFrame(records)

    logger.info(
        "Preprocessing complete: %d rows kept, %d dropped (missing name/city), %d duplicate name+city pairs",
        len(result),
        dropped_missing,
        duplicate_names,
    )

    if not result.empty:
        logger.info(
            "Sample stats — cities: %d, avg rating: %.2f, avg cost: %.1f",
            result["city"].nunique(),
            result["rating"].mean(skipna=True) or 0.0,
            result["cost_for_two"].mean(skipna=True) or 0.0,
        )

    return result


def dataframe_to_restaurants(df: pd.DataFrame) -> list[Restaurant]:
    restaurants: list[Restaurant] = []
    for _, row in df.iterrows():
        cuisines = row.get("cuisines")
        if isinstance(cuisines, list):
            cuisine_list = cuisines
        else:
            cuisine_list = list(cuisines) if cuisines is not None else []

        restaurants.append(
            Restaurant(
                id=str(row["id"]),
                name=str(row["name"]),
                city=str(row["city"]),
                cuisine=str(row["cuisine"]),
                cuisines=cuisine_list,
                cost_for_two=row["cost_for_two"] if pd.notna(row.get("cost_for_two")) else None,
                rating=row["rating"] if pd.notna(row.get("rating")) else None,
                rating_count=int(row.get("rating_count", 0)),
            )
        )
    return restaurants


def log_sample_rows(df: pd.DataFrame, count: int = 10) -> None:
    if df.empty:
        logger.info("No rows to sample")
        return
    sample = df.head(count)
    for _, row in sample.iterrows():
        logger.info(
            "Sample: id=%s name=%s city=%s cuisine=%s rating=%s cost=%s",
            row["id"],
            row["name"],
            row["city"],
            row["cuisine"],
            row["rating"],
            row["cost_for_two"],
        )
