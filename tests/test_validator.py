"""Tests for recommendation validator."""

import pytest

from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.validator import RecommendationValidator, ValidationError, enrich_recommendations


@pytest.fixture
def candidates():
    return [
        Restaurant(
            id="r_1",
            name="North Spice",
            city="Bangalore",
            cuisine="North Indian",
            rating=4.5,
            rating_count=100,
            cost_for_two=400,
        ),
        Restaurant(
            id="r_2",
            name="Chinese Wok",
            city="Bangalore",
            cuisine="Chinese",
            rating=4.2,
            rating_count=50,
            cost_for_two=350,
        ),
    ]


def test_validate_accepts_valid_ids(candidates):
    validator = RecommendationValidator()
    result = validator.validate(
        [
            {
                "restaurant_id": "r_1",
                "rank": 1,
                "why_recommended": "Great fit for North Indian in Bangalore.",
            }
        ],
        candidates,
        limit=5,
    )
    assert len(result) == 1


def test_validate_rejects_unknown_id(candidates):
    validator = RecommendationValidator()
    with pytest.raises(ValidationError):
        validator.validate(
            [{"restaurant_id": "fake_999", "rank": 1, "why_recommended": "test"}],
            candidates,
            limit=5,
        )


def test_validate_rejects_duplicate_ranks(candidates):
    validator = RecommendationValidator()
    with pytest.raises(ValidationError):
        validator.validate(
            [
                {"restaurant_id": "r_1", "rank": 1, "why_recommended": "a"},
                {"restaurant_id": "r_2", "rank": 1, "why_recommended": "b"},
            ],
            candidates,
            limit=5,
        )


def test_enrich_uses_dataset_facts(candidates):
    validator = RecommendationValidator()
    validated = validator.validate(
        [{"restaurant_id": "r_1", "rank": 1, "why_recommended": "Custom explanation."}],
        candidates,
        limit=5,
    )
    prefs = UserPreferences(location="Bangalore", budget="medium")
    items = enrich_recommendations(validated, candidates, prefs)

    assert items[0].restaurant_name == "North Spice"
    assert items[0].rating == 4.5
    assert items[0].cost_for_two == 400
    assert items[0].why_recommended == "Custom explanation."
