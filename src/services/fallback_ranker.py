"""Rule-based restaurant ranking when LLM is unavailable."""

import math

from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant


def candidate_score(restaurant: Restaurant) -> float:
    """Score by rating weighted by popularity (rating_count)."""
    rating = restaurant.rating if restaurant.rating is not None else 0.0
    return rating * math.log(restaurant.rating_count + 1)


def rank_restaurants(restaurants: list[Restaurant], limit: int) -> list[tuple[int, Restaurant]]:
    """Return top restaurants as (rank, restaurant) pairs."""
    if not restaurants or limit <= 0:
        return []

    scored = sorted(restaurants, key=candidate_score, reverse=True)
    return [(rank, restaurant) for rank, restaurant in enumerate(scored[:limit], start=1)]


def build_template_explanation(restaurant: Restaurant, preferences: UserPreferences) -> str:
    """Generate a template explanation for rule-based recommendations."""
    parts: list[str] = []

    if restaurant.rating is not None:
        parts.append(f"Rated {restaurant.rating:.1f}")
    if restaurant.cuisine:
        parts.append(f"serves {restaurant.cuisine}")
    parts.append(f"in {restaurant.city}")

    if restaurant.cost_for_two is not None:
        parts.append(f"cost for two is ₹{restaurant.cost_for_two:.0f}")

    parts.append(f"matching your {preferences.budget} budget")

    if preferences.cuisine:
        parts.append(f"and {preferences.cuisine} preference")

    if preferences.additional_preferences:
        parts.append(f"({preferences.additional_preferences})")

    return ", ".join(parts) + "."


def build_summary(
    preferences: UserPreferences,
    returned: int,
    total_candidates: int,
) -> str:
    if returned == 0:
        return ""

    cuisine_part = f" {preferences.cuisine}" if preferences.cuisine else ""
    return (
        f"Found {returned} top{cuisine_part} restaurant recommendations in "
        f"{preferences.location} for a {preferences.budget} budget "
        f"(from {total_candidates} matching options)."
    )
