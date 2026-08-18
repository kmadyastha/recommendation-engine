"""FastAPI route handlers."""

from fastapi import APIRouter, Depends

from src import app_state
from src.api.schemas import HealthResponse, RecommendationRequest, RecommendationResponse
from src.app_state import get_recommendation_service, get_store
from src.config import get_settings
from src.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    settings = get_settings()
    store = get_store()
    store_stats = store.stats()
    data_ready = len(store) > 0

    return HealthResponse(
        status="ok",
        ready=app_state.budget_tiers is not None and data_ready,
        budget_tiers_loaded=app_state.budget_tiers is not None,
        budget_tier_keys=list(app_state.budget_tiers.keys()) if app_state.budget_tiers else [],
        data_loaded=data_ready,
        data_path=str(settings.data_path),
        data_error=app_state.data_load_error,
        restaurant_count=store_stats["row_count"],
        city_count=store_stats["city_count"],
        avg_rating=store_stats["avg_rating"],
        avg_cost_for_two=store_stats["avg_cost_for_two"],
        llm_configured=settings.llm_api_key is not None,
    )


@router.get("/cities")
def list_cities(
    service: RecommendationService = Depends(get_recommendation_service),
) -> dict[str, list[str]]:
    return {"cities": service.list_cities()}


@router.get("/cuisines")
def list_cuisines(
    service: RecommendationService = Depends(get_recommendation_service),
) -> dict[str, list[str]]:
    return {"cuisines": service.list_cuisines()}


@router.post("/recommendations", response_model=RecommendationResponse)
def create_recommendations(
    request: RecommendationRequest,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationResponse:
    return service.recommend(request)
