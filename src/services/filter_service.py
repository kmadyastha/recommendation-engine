"""Deterministic restaurant filtering and candidate selection."""

import logging
import math
from typing import Any

import pandas as pd

from src.config import load_budget_tiers
from src.data.preprocessor import normalize_city
from src.data.store import RestaurantStore
from src.models.preferences import BudgetTier, UserPreferences
from src.models.restaurant import Restaurant

logger = logging.getLogger(__name__)

DEFAULT_MAX_CANDIDATES = 50

BUDGET_ORDER: list[BudgetTier] = ["low", "medium", "high"]


class FilterResult:
    """Outcome of filtering restaurants against user preferences."""

    def __init__(
        self,
        candidates: list[Restaurant],
        total_matched: int,
        empty_reason: str | None = None,
        suggestions: list[str] | None = None,
    ) -> None:
        self.candidates = candidates
        self.total_matched = total_matched
        self.empty_reason = empty_reason
        self.suggestions = suggestions or []

    @property
    def is_empty(self) -> bool:
        return len(self.candidates) == 0


class FilterService:
    """Apply deterministic filters and select LLM-ready candidate sets."""

    def __init__(
        self,
        store: RestaurantStore,
        budget_tiers: dict[str, Any] | None = None,
        max_candidates: int = DEFAULT_MAX_CANDIDATES,
    ) -> None:
        self._store = store
        self._budget_tiers = budget_tiers or load_budget_tiers()
        self._max_candidates = max_candidates

    def list_cities(self) -> list[str]:
        """Distinct cities available in the store (for UI dropdowns)."""
        return self._store.list_cities()

    def list_cuisines(self) -> list[str]:
        """Distinct cuisine tokens available in the store (for UI dropdowns)."""
        return self._store.list_cuisines()

    def filter(self, preferences: UserPreferences) -> FilterResult:
        df = self._store.dataframe
        if df.empty:
            return FilterResult(
                candidates=[],
                total_matched=0,
                empty_reason="dataset_empty",
                suggestions=["Load restaurant data before requesting recommendations."],
            )

        normalized_location = normalize_city(preferences.location)
        if not normalized_location:
            return FilterResult(
                candidates=[],
                total_matched=0,
                empty_reason="invalid_location",
                suggestions=["Provide a valid city name."],
            )

        city_mask = df["city"].astype(str).str.lower() == normalized_location.lower()
        matched = df[city_mask]

        if matched.empty:
            cities = self.list_cities()
            sample = ", ".join(cities[:5])
            return FilterResult(
                candidates=[],
                total_matched=0,
                empty_reason="no_restaurants_in_city",
                suggestions=[
                    f"No restaurants found for '{preferences.location}'.",
                    f"Try one of: {sample}" if cities else "Check available cities via the API.",
                ],
            )

        matched = self._apply_rating_filter(matched, preferences.min_rating)
        matched = self._apply_cuisine_filter(matched, preferences.cuisine)
        matched = self._apply_budget_filter(matched, preferences.budget)

        total_matched = len(matched)
        if total_matched == 0:
            return FilterResult(
                candidates=[],
                total_matched=0,
                empty_reason="no_matches_for_filters",
                suggestions=self._build_suggestions(df, preferences, normalized_location),
            )

        ranked = self._rank_candidates(matched)
        capped = ranked.head(self._max_candidates)
        candidates = [self._store.row_to_restaurant(row) for _, row in capped.iterrows()]

        logger.info(
            "Filter matched %d restaurants (%d returned after cap) for %s",
            total_matched,
            len(candidates),
            normalized_location,
        )

        return FilterResult(candidates=candidates, total_matched=total_matched)

    def _apply_rating_filter(self, df: pd.DataFrame, min_rating: float) -> pd.DataFrame:
        if min_rating <= 0:
            return df

        def rating_ok(value: object) -> bool:
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return False
            return float(value) >= min_rating

        return df[df["rating"].apply(rating_ok)]

    def _apply_cuisine_filter(self, df: pd.DataFrame, cuisine: str | None) -> pd.DataFrame:
        if not cuisine:
            return df

        needle = cuisine.strip().lower()
        if not needle:
            return df

        def cuisine_ok(row: pd.Series) -> bool:
            cuisines = row.get("cuisines")
            tokens: list[str] = []
            if isinstance(cuisines, list):
                tokens = cuisines
            elif cuisines is not None and not (isinstance(cuisines, float) and pd.isna(cuisines)):
                tokens = [str(cuisines)]

            for token in tokens:
                token_lower = str(token).strip().lower()
                if token_lower == needle or needle in token_lower or token_lower in needle:
                    return True
            return False

        return df[df.apply(cuisine_ok, axis=1)]

    def _apply_budget_filter(self, df: pd.DataFrame, budget: BudgetTier) -> pd.DataFrame:
        if df.empty:
            return df

        cost_column = "cost_for_two" if "cost_for_two" in df.columns else "cost"
        if cost_column not in df.columns:
            return df

        tier = self._budget_tiers.get(budget)
        if tier is None:
            raise ValueError(f"Unknown budget tier: {budget}")

        min_cost = float(tier["min"])
        max_cost = tier.get("max")
        max_cost_val = float(max_cost) if max_cost is not None else None

        def budget_ok(value: object) -> bool:
            if value is None or (isinstance(value, float) and pd.isna(value)):
                return False
            cost = float(value)
            if cost < min_cost:
                return False
            if max_cost_val is not None and cost > max_cost_val:
                return False
            return True

        return df[df[cost_column].apply(budget_ok)]

    def _rank_candidates(self, df: pd.DataFrame) -> pd.DataFrame:
        working = df.copy()
        working["_score"] = working.apply(self._candidate_score, axis=1)
        return working.sort_values(by="_score", ascending=False)

    @staticmethod
    def _candidate_score(row: pd.Series) -> float:
        rating = row.get("rating")
        rating_count = row.get("rating_count", 0)

        if rating is None or (isinstance(rating, float) and pd.isna(rating)):
            rating_val = 0.0
        else:
            rating_val = float(rating)

        if rating_count is None or (isinstance(rating_count, float) and pd.isna(rating_count)):
            count_val = 0
        else:
            count_val = int(rating_count)

        return rating_val * math.log(count_val + 1)

    def _build_suggestions(
        self,
        df: pd.DataFrame,
        preferences: UserPreferences,
        normalized_location: str,
    ) -> list[str]:
        suggestions: list[str] = []
        city_df = df[df["city"].astype(str).str.lower() == normalized_location.lower()]

        without_rating = self._apply_cuisine_filter(
            self._apply_budget_filter(city_df, preferences.budget),
            preferences.cuisine,
        )
        if preferences.min_rating > 0 and len(without_rating) > 0:
            lower = max(0.0, preferences.min_rating - 0.5)
            suggestions.append(f"Lower minimum rating to {lower:.1f}.")

        without_cuisine = self._apply_rating_filter(
            self._apply_budget_filter(city_df, preferences.budget),
            preferences.min_rating,
        )
        if preferences.cuisine and len(without_cuisine) > 0:
            suggestions.append("Try a broader cuisine or remove the cuisine filter.")

        without_budget = self._apply_rating_filter(
            self._apply_cuisine_filter(city_df, preferences.cuisine),
            preferences.min_rating,
        )
        if len(without_budget) > 0:
            current_idx = BUDGET_ORDER.index(preferences.budget)
            if current_idx < len(BUDGET_ORDER) - 1:
                next_tier = BUDGET_ORDER[current_idx + 1]
                suggestions.append(f"Try a higher budget tier such as '{next_tier}'.")

        if not suggestions:
            suggestions.append("Broaden your search by relaxing rating, cuisine, or budget filters.")

        return suggestions
