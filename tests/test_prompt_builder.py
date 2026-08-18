"""Tests for prompt builder."""

from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.prompt_builder import build_messages, candidate_payload


def test_candidate_payload_fields():
    restaurant = Restaurant(
        id="r_1",
        name="Test Rest",
        city="Bangalore",
        cuisine="North Indian",
        rating=4.5,
        rating_count=100,
        cost_for_two=400,
    )
    payload = candidate_payload(restaurant)
    assert payload["id"] == "r_1"
    assert payload["name"] == "Test Rest"


def test_build_messages_includes_candidates():
    prefs = UserPreferences(location="Bangalore", budget="medium", limit=3)
    candidates = [
        Restaurant(
            id="r_1",
            name="A",
            city="Bangalore",
            cuisine="North Indian",
            rating=4.5,
            rating_count=10,
            cost_for_two=400,
        )
    ]
    messages = build_messages(prefs, candidates)
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"
    assert "r_1" in messages[1]["content"]
    assert "ONLY choose from this list" in messages[1]["content"] or "Candidates" in messages[1]["content"]
