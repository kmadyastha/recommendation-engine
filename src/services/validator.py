"""Validate and enrich LLM recommendation output."""

import logging

from src.api.schemas import RecommendationItem
from src.models.restaurant import Restaurant
from src.services.fallback_ranker import build_template_explanation

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Raised when LLM output fails validation."""


class RecommendationValidator:
    """Ensure LLM recommendations are grounded in the candidate set."""

    def validate(
        self,
        llm_recommendations: list[dict],
        candidates: list[Restaurant],
        limit: int,
    ) -> list[dict]:
        if not llm_recommendations:
            raise ValidationError("LLM returned empty recommendations")

        candidate_ids = {c.id for c in candidates}
        seen_ids: set[str] = set()
        seen_ranks: set[int] = set()
        validated: list[dict] = []

        for entry in llm_recommendations:
            restaurant_id = str(entry.get("restaurant_id", "")).strip()
            if not restaurant_id or restaurant_id not in candidate_ids:
                raise ValidationError(f"Invalid restaurant_id: {restaurant_id!r}")

            rank = entry.get("rank")
            if not isinstance(rank, int) or rank < 1:
                raise ValidationError(f"Invalid rank: {rank!r}")

            if rank in seen_ranks:
                raise ValidationError(f"Duplicate rank: {rank}")

            if restaurant_id in seen_ids:
                raise ValidationError(f"Duplicate restaurant_id: {restaurant_id}")

            why = entry.get("why_recommended")
            if not why or not str(why).strip():
                raise ValidationError(f"Missing why_recommended for {restaurant_id}")

            seen_ids.add(restaurant_id)
            seen_ranks.add(rank)
            validated.append(
                {
                    "restaurant_id": restaurant_id,
                    "rank": rank,
                    "why_recommended": str(why).strip(),
                }
            )

        validated.sort(key=lambda x: x["rank"])
        return validated[:limit]


def enrich_recommendations(
    validated: list[dict],
    candidates: list[Restaurant],
    preferences,
) -> list[RecommendationItem]:
    """Merge LLM ranks/explanations with dataset-backed factual fields."""
    by_id = {c.id: c for c in candidates}
    items: list[RecommendationItem] = []

    for entry in validated:
        restaurant = by_id.get(entry["restaurant_id"])
        if restaurant is None:
            logger.warning("Validated ID missing from candidates: %s", entry["restaurant_id"])
            continue

        items.append(
            RecommendationItem(
                rank=entry["rank"],
                restaurant_name=restaurant.name,
                cuisine=restaurant.cuisine,
                rating=restaurant.rating,
                cost_for_two=restaurant.cost_for_two,
                location=restaurant.city,
                why_recommended=entry["why_recommended"],
            )
        )

    if not items:
        raise ValidationError("No recommendations after enrichment")

    return items


def enrich_fallback(
    ranked: list[tuple[int, Restaurant]],
    preferences,
) -> list[RecommendationItem]:
    return [
        RecommendationItem(
            rank=rank,
            restaurant_name=restaurant.name,
            cuisine=restaurant.cuisine,
            rating=restaurant.rating,
            cost_for_two=restaurant.cost_for_two,
            location=restaurant.city,
            why_recommended=build_template_explanation(restaurant, preferences),
        )
        for rank, restaurant in ranked
    ]
