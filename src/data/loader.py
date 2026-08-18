"""Load raw Swiggy dataset files from disk."""

import json
import logging
from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT

logger = logging.getLogger(__name__)

DEFAULT_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DEFAULT_MAPPING_PATH = PROJECT_ROOT / "data" / "config" / "column_mapping.json"

REQUIRED_INTERNAL_FIELDS = (
    "name",
    "city",
    "cuisine",
    "cost_for_two",
    "rating",
    "rating_count",
)

EMPTY_COLUMNS = ["id", "name", "city", "rating", "rating_count", "cost", "cuisine"]


class DatasetLoadError(FileNotFoundError):
    """Raised when the raw dataset file cannot be found or read."""


def load_column_mapping(path: Path | None = None) -> dict:
    mapping_path = path or DEFAULT_MAPPING_PATH
    with mapping_path.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_raw_path(raw_path: Path | None = None, raw_dir: Path | None = None) -> Path:
    """Resolve path to raw dataset file (CSV or JSON)."""
    if raw_path is not None:
        candidate = raw_path if raw_path.is_absolute() else PROJECT_ROOT / raw_path
        if candidate.is_dir():
            nested = candidate / "data.json"
            if nested.is_file():
                return nested
            raise DatasetLoadError(f"Raw dataset path is a directory without data.json: {candidate}")
        if candidate.exists():
            return candidate
        raise DatasetLoadError(f"Raw dataset file not found: {candidate}")

    search_dir = raw_dir or DEFAULT_RAW_DIR
    if not search_dir.is_absolute():
        search_dir = PROJECT_ROOT / search_dir

    candidates = [
        search_dir / "swiggy.csv",
        search_dir / "data.json" / "data.json",
        search_dir / "data.json",
        search_dir / "restaurants.csv",
        search_dir / "Swiggy.csv",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate

    raise DatasetLoadError(
        f"No raw dataset found in {search_dir}. "
        "Place swiggy.csv or data.json from Kaggle in data/raw/"
    )


def map_raw_columns(df: pd.DataFrame, mapping: dict | None = None) -> pd.DataFrame:
    """Map heterogeneous raw column names to internal field names."""
    mapping = mapping or load_column_mapping()
    source_columns = mapping["source_columns"]
    renamed: dict[str, pd.Series] = {}

    normalized_cols = {str(c).strip().lower(): c for c in df.columns}

    for internal_name, aliases in source_columns.items():
        for alias in aliases:
            key = alias.strip().lower()
            if key in normalized_cols:
                renamed[internal_name] = df[normalized_cols[key]]
                break

    missing = [f for f in ("name", "city", "cuisine") if f not in renamed]
    if missing:
        raise DatasetLoadError(
            f"Required columns missing after mapping: {missing}. "
            f"Available columns: {list(df.columns)}"
        )

    mapped = pd.DataFrame(renamed)

    # Optional fields
    for optional in ("id", "rating", "rating_count", "cost"):
        if optional not in mapped.columns:
            mapped[optional] = None

    return mapped


def flatten_kaggle_json(data: dict) -> pd.DataFrame:
    """Flatten nested Kaggle data.json into a tabular dataframe."""
    rows: list[dict] = []

    for city_name, city_payload in data.items():
        if not isinstance(city_payload, dict):
            continue
        restaurants = city_payload.get("restaurants", {})
        if not isinstance(restaurants, dict):
            continue

        for restaurant_id, restaurant in restaurants.items():
            if not isinstance(restaurant, dict):
                continue
            rows.append(
                {
                    "id": restaurant_id,
                    "name": restaurant.get("name"),
                    "city": city_name,
                    "rating": restaurant.get("rating"),
                    "rating_count": restaurant.get("rating_count"),
                    "cost": restaurant.get("cost"),
                    "cuisine": restaurant.get("cuisine"),
                }
            )

    logger.info("Flattened JSON into %d restaurant rows across cities", len(rows))
    return pd.DataFrame(rows, columns=EMPTY_COLUMNS) if not rows else pd.DataFrame(rows)


def read_raw_json(path: Path) -> pd.DataFrame:
    """Read nested Kaggle data.json format."""
    logger.info("Loading JSON dataset from %s (this may take a few minutes)", path)
    with path.open(encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise DatasetLoadError("Expected top-level JSON object keyed by city name")

    return flatten_kaggle_json(data)


def read_raw_csv(path: Path) -> pd.DataFrame:
    """Read and column-map a Swiggy CSV file."""
    logger.info("Loading raw CSV from %s", path)

    try:
        df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        logger.warning("UTF-8 decode failed for %s; retrying with latin-1", path)
        df = pd.read_csv(path, encoding="latin-1", low_memory=False)

    if df.empty:
        logger.warning("Raw CSV is empty: %s", path)
        return pd.DataFrame(columns=EMPTY_COLUMNS)

    mapped = map_raw_columns(df)
    logger.info("Mapped %d raw rows with columns: %s", len(mapped), list(mapped.columns))
    return mapped


def read_raw_dataset(path: Path | None = None, raw_dir: Path | None = None) -> pd.DataFrame:
    """Read raw Swiggy dataset from CSV or JSON."""
    dataset_path = resolve_raw_path(path, raw_dir)

    if dataset_path.suffix.lower() == ".json":
        return read_raw_json(dataset_path)
    return read_raw_csv(dataset_path)


if __name__ == "__main__":
    import sys

    from src.data.pipeline import main

    sys.exit(main())
