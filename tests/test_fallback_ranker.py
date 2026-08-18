"""Tests for fallback ranker."""

from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.fallback_ranker import candidate_score, rank_restaurants


def test_candidate_score_uses_rating_count():
    high = Restaurant(
        id="r_1",
        name="A",
        city="Bangalore",
        cuisine="Indian",
        rating=4.0,
        rating_count=1000,
    )
    low = Restaurant(
        id="r_2",
        name="B",
        city="Bangalore",
        cuisine="Indian",
        rating=4.0,
        rating_count=10,
    )
    assert candidate_score(high) > candidate_score(low)


def test_rank_restaurants_limits_results():
    restaurants = [
        Restaurant(
            id=f"r_{i}",
            name=f"Rest {i}",
            city="Bangalore",
            cuisine="Indian",
            rating=4.0,
            rating_count=i,
        )
        for i in range(10)
    ]
    ranked = rank_restaurants(restaurants, limit=3)
    assert len(ranked) == 3
    assert ranked[0][0] == 1
    assert ranked[-1][0] == 3
