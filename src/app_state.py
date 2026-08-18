"""Shared application state set during FastAPI lifespan."""

from typing import Any

from src.data.store import RestaurantStore
from src.services.filter_service import FilterService
from src.services.recommendation_service import RecommendationService

budget_tiers: dict[str, Any] | None = None
restaurant_store: RestaurantStore | None = None
data_load_error: str | None = None
filter_service: FilterService | None = None
recommendation_service: RecommendationService | None = None


def get_store() -> RestaurantStore:
    return restaurant_store or RestaurantStore()


def get_filter_service() -> FilterService:
    if filter_service is None:
        return FilterService(get_store())
    return filter_service


def get_recommendation_service() -> RecommendationService:
    if recommendation_service is None:
        return RecommendationService(get_filter_service())
    return recommendation_service
