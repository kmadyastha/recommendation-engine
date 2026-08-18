"""Tests for filter service and user preferences."""

import pandas as pd
import pytest
from pydantic import ValidationError

from src.data.store import RestaurantStore
from src.models.preferences import UserPreferences
from src.services.filter_service import DEFAULT_MAX_CANDIDATES, FilterService


def _make_store(rows: list[dict]) -> RestaurantStore:
    return RestaurantStore(pd.DataFrame(rows))


@pytest.fixture
def sample_store() -> RestaurantStore:
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
        {
            "id": "r_3",
            "name": "Budget Bites",
            "city": "Bangalore",
            "cuisine": "Fast Food",
            "cuisines": ["Fast Food", "Snacks"],
            "cost_for_two": 200.0,
            "rating": 3.8,
            "rating_count": 50,
        },
        {
            "id": "r_4",
            "name": "Premium Palace",
            "city": "Bangalore",
            "cuisine": "North Indian",
            "cuisines": ["North Indian"],
            "cost_for_two": 900.0,
            "rating": 4.9,
            "rating_count": 500,
        },
        {
            "id": "r_5",
            "name": "Delhi Darbar",
            "city": "Delhi",
            "cuisine": "North Indian",
            "cuisines": ["North Indian"],
            "cost_for_two": 400.0,
            "rating": 4.3,
            "rating_count": 300,
        },
        {
            "id": "r_6",
            "name": "Low Boundary",
            "city": "Bangalore",
            "cuisine": "North Indian",
            "cuisines": ["North Indian"],
            "cost_for_two": 300.0,
            "rating": 4.0,
            "rating_count": 100,
        },
        {
            "id": "r_7",
            "name": "No Rating",
            "city": "Bangalore",
            "cuisine": "North Indian",
            "cuisines": ["North Indian"],
            "cost_for_two": 400.0,
            "rating": None,
            "rating_count": 0,
        },
    ]
    return _make_store(rows)


@pytest.fixture
def filter_service(sample_store: RestaurantStore) -> FilterService:
    return FilterService(sample_store)


def test_happy_path_bangalore_medium_north_indian():
    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="North Indian",
        min_rating=4.0,
    )
    service = FilterService(
        _make_store(
            [
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
        )
    )
    result = service.filter(prefs)

    assert not result.is_empty
    assert len(result.candidates) == 1
    assert result.candidates[0].name == "North Spice"
    assert result.candidates[0].city == "Bangalore"
    assert result.candidates[0].rating >= 4.0
    assert 300 <= result.candidates[0].cost_for_two <= 600


def test_filter_all_candidates_exist_in_store(filter_service: FilterService, sample_store: RestaurantStore):
    prefs = UserPreferences(location="Bangalore", budget="medium", cuisine="North Indian", min_rating=4.0)
    result = filter_service.filter(prefs)

    store_ids = set(sample_store.dataframe["id"].tolist())
    for candidate in result.candidates:
        assert candidate.id in store_ids


def test_budget_tier_medium_excludes_expensive(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=0.0)
    result = filter_service.filter(prefs)

    ids = {c.id for c in result.candidates}
    assert "r_4" not in ids  # 900 is high tier
    assert "r_3" not in ids  # 200 is low tier
    for candidate in result.candidates:
        assert 300 <= candidate.cost_for_two <= 600


def test_budget_tier_low(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="low", min_rating=0.0)
    result = filter_service.filter(prefs)

    for candidate in result.candidates:
        assert candidate.cost_for_two <= 300


def test_city_normalization_bangalore(filter_service: FilterService):
    prefs = UserPreferences(location="bangalore", budget="high", min_rating=0.0)
    result = filter_service.filter(prefs)

    assert not result.is_empty
    assert all(c.city == "Bangalore" for c in result.candidates)


def test_cuisine_case_insensitive(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="medium", cuisine="chinese", min_rating=0.0)
    result = filter_service.filter(prefs)

    assert len(result.candidates) == 1
    assert result.candidates[0].name == "Chinese Wok"


def test_multi_cuisine_token_match(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="low", cuisine="Snacks", min_rating=0.0)
    result = filter_service.filter(prefs)

    assert len(result.candidates) == 1
    assert result.candidates[0].name == "Budget Bites"


def test_strict_rating_empty_with_suggestions(filter_service: FilterService):
    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="North Indian",
        min_rating=5.0,
    )
    result = filter_service.filter(prefs)

    assert result.is_empty
    assert result.empty_reason == "no_matches_for_filters"
    assert any("rating" in s.lower() for s in result.suggestions)


def test_unknown_city_empty(filter_service: FilterService):
    prefs = UserPreferences(location="Tokyo", budget="medium", min_rating=0.0)
    result = filter_service.filter(prefs)

    assert result.is_empty
    assert result.empty_reason == "no_restaurants_in_city"
    assert result.suggestions


def test_no_cuisine_filter_broader_results(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=4.0)
    result = filter_service.filter(prefs)

    assert len(result.candidates) >= 2


def test_min_rating_excludes_null_rating(filter_service: FilterService):
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=4.0)
    result = filter_service.filter(prefs)

    ids = {c.id for c in result.candidates}
    assert "r_7" not in ids


def test_candidate_cap():
    rows = []
    for i in range(60):
        rows.append(
            {
                "id": f"r_{i}",
                "name": f"Rest {i}",
                "city": "Bangalore",
                "cuisine": "North Indian",
                "cuisines": ["North Indian"],
                "cost_for_two": 400.0,
                "rating": 4.0 + (i % 10) * 0.01,
                "rating_count": i * 10,
            }
        )
    service = FilterService(_make_store(rows), max_candidates=DEFAULT_MAX_CANDIDATES)
    prefs = UserPreferences(location="Bangalore", budget="medium", min_rating=0.0)
    result = service.filter(prefs)

    assert result.total_matched == 60
    assert len(result.candidates) == DEFAULT_MAX_CANDIDATES


def test_list_cities_and_cuisines(filter_service: FilterService):
    cities = filter_service.list_cities()
    cuisines = filter_service.list_cuisines()

    assert "Bangalore" in cities
    assert "Delhi" in cities
    assert "North Indian" in cuisines
    assert "Chinese" in cuisines


def test_user_preferences_validation():
    UserPreferences(location="Bangalore", budget="medium")
    with pytest.raises(ValidationError):
        UserPreferences(location="", budget="medium")
    with pytest.raises(ValidationError):
        UserPreferences(location="Bangalore", budget="luxury")
