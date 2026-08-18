"""In-memory restaurant store backed by Pandas."""

import logging
import time
from pathlib import Path

import pandas as pd

from src.config import PROJECT_ROOT, get_settings
from src.models.restaurant import Restaurant

logger = logging.getLogger(__name__)


class RestaurantStoreError(FileNotFoundError):
    """Raised when the processed dataset cannot be loaded."""


class RestaurantStore:
    """Searchable in-memory store for normalized restaurant records."""

    def __init__(self, df: pd.DataFrame | None = None) -> None:
        self._df = df if df is not None else pd.DataFrame()

    @property
    def dataframe(self) -> pd.DataFrame:
        return self._df

    def __len__(self) -> int:
        return len(self._df)

    @classmethod
    def from_parquet(cls, path: Path) -> "RestaurantStore":
        resolved = path if path.is_absolute() else PROJECT_ROOT / path
        if not resolved.exists():
            raise RestaurantStoreError(f"Processed dataset not found: {resolved}")

        logger.info("Loading restaurant store from %s", resolved)
        start = time.perf_counter()
        df = pd.read_parquet(resolved)
        elapsed_ms = (time.perf_counter() - start) * 1000
        store = cls(df)
        logger.info("Restaurant store loaded: %d rows in %.0f ms", len(store), elapsed_ms)
        return store

    @classmethod
    def load(cls, path: Path | None = None) -> "RestaurantStore":
        settings = get_settings()
        data_path = path or settings.data_path
        if not data_path.is_absolute():
            data_path = PROJECT_ROOT / data_path
        return cls.from_parquet(data_path)

    def get_by_id(self, restaurant_id: str) -> Restaurant | None:
        if self._df.empty:
            return None
        matches = self._df[self._df["id"] == restaurant_id]
        if matches.empty:
            return None
        return self._row_to_restaurant(matches.iloc[0])

    def row_to_restaurant(self, row: pd.Series) -> Restaurant:
        """Convert a dataframe row to a Restaurant model."""
        return self._row_to_restaurant(row)

    def list_cities(self) -> list[str]:
        if self._df.empty or "city" not in self._df.columns:
            return []
        return sorted(self._df["city"].dropna().unique().tolist())

    def list_cuisines(self) -> list[str]:
        if self._df.empty or "cuisines" not in self._df.columns:
            return []
        tokens: set[str] = set()
        for value in self._df["cuisines"]:
            if isinstance(value, list):
                tokens.update(str(t).strip() for t in value if str(t).strip())
            elif hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
                tokens.update(str(t).strip() for t in value if str(t).strip())
            elif value is not None and not (isinstance(value, float) and pd.isna(value)):
                tokens.add(str(value).strip())
        return sorted(tokens)

    def stats(self) -> dict:
        if self._df.empty:
            return {
                "row_count": 0,
                "city_count": 0,
                "avg_rating": None,
                "avg_cost_for_two": None,
            }
        return {
            "row_count": len(self._df),
            "city_count": self._df["city"].nunique(),
            "avg_rating": float(self._df["rating"].mean(skipna=True)) if self._df["rating"].notna().any() else None,
            "avg_cost_for_two": float(self._df["cost_for_two"].mean(skipna=True))
            if self._df["cost_for_two"].notna().any()
            else None,
        }

    @staticmethod
    def _row_to_restaurant(row: pd.Series) -> Restaurant:
        cuisines = row.get("cuisines")
        if isinstance(cuisines, list):
            cuisine_list = [str(c) for c in cuisines]
        elif hasattr(cuisines, "__iter__") and not isinstance(cuisines, (str, bytes)):
            cuisine_list = [str(c) for c in cuisines]
        else:
            cuisine_list = list(cuisines) if cuisines is not None else []

        return Restaurant(
            id=str(row["id"]),
            name=str(row["name"]),
            city=str(row["city"]),
            cuisine=str(row["cuisine"]),
            cuisines=cuisine_list,
            cost_for_two=row["cost_for_two"] if pd.notna(row.get("cost_for_two")) else None,
            rating=row["rating"] if pd.notna(row.get("rating")) else None,
            rating_count=int(row.get("rating_count", 0)),
        )
