"""Tests for recommendation service orchestration."""

import pandas as pd

from src.api.schemas import RecommendationRequest
from src.data.store import RestaurantStore
from src.services.filter_service import FilterService
from src.services.recommendation_engine import RecommendationEngine
from src.services.recommendation_service import RecommendationService
from tests.mocks.llm_mock import MockLLMClient, valid_llm_response


def _service_with_data(mock_client: MockLLMClient | None = None) -> RecommendationService:
    rows = [
        {
            "id": "r_1",
            "name": "North Spice",
            "city": "Bangalore",
            "cuisine": "North Indian",
            "cuisines": ["North Indian"],
            "cost_for_two": 450.0,
            "rating": 4.5,
            "rating_count": 1200,
        },
        {
            "id": "r_2",
            "name": "Chinese Wok",
            "city": "Bangalore",
            "cuisine": "Chinese",
            "cuisines": ["Chinese"],
            "cost_for_two": 350.0,
            "rating": 4.2,
            "rating_count": 800,
        },
    ]
    store = RestaurantStore(pd.DataFrame(rows))
    filter_service = FilterService(store)
    engine = RecommendationEngine(client=mock_client)
    return RecommendationService(filter_service, engine=engine)


def test_rule_based_when_no_llm():
    service = _service_with_data(mock_client=None)
    request = RecommendationRequest(
        location="Bangalore",
        budget="medium",
        cuisine="North Indian",
        min_rating=4.0,
        limit=5,
    )
    response = service.recommend(request)
    assert response.meta.source == "rule_based"
    assert len(response.recommendations) == 1


def test_llm_path_with_mock():
    service = _service_with_data(mock_client=MockLLMClient(valid_llm_response("r_1")))
    request = RecommendationRequest(
        location="Bangalore",
        budget="medium",
        cuisine="North Indian",
        min_rating=4.0,
        limit=5,
    )
    response = service.recommend(request)
    assert response.meta.source == "llm"
    assert response.recommendations[0].restaurant_name == "North Spice"
    assert response.recommendations[0].rating == 4.5


def test_fallback_on_invalid_llm_id():
    bad_response = {
        "summary": "test",
        "recommendations": [
            {"restaurant_id": "fake_id", "rank": 1, "why_recommended": "bad"}
        ],
    }
    service = _service_with_data(mock_client=MockLLMClient(bad_response))
    request = RecommendationRequest(
        location="Bangalore",
        budget="medium",
        cuisine="North Indian",
        min_rating=4.0,
        limit=5,
    )
    response = service.recommend(request)
    assert response.meta.source == "fallback"
    assert len(response.recommendations) >= 1
