"""Tests for LLM recommendation engine."""

import json

import pytest

from src.models.preferences import UserPreferences
from src.models.restaurant import Restaurant
from src.services.recommendation_engine import RecommendationEngine, parse_llm_response, strip_json_fences
from tests.mocks.llm_mock import MockLLMClient, valid_llm_response


def test_strip_json_fences():
    raw = '```json\n{"summary": "hi", "recommendations": []}\n```'
    assert "summary" in strip_json_fences(raw)


def test_parse_llm_response():
    data = parse_llm_response(json.dumps(valid_llm_response()))
    assert data["summary"]
    assert len(data["recommendations"]) == 1


def test_recommendation_engine_with_mock():
    candidate = Restaurant(
        id="r_1",
        name="North Spice",
        city="Bangalore",
        cuisine="North Indian",
        rating=4.5,
        rating_count=100,
        cost_for_two=400,
    )
    client = MockLLMClient(valid_llm_response("r_1"))
    engine = RecommendationEngine(client=client)
    prefs = UserPreferences(location="Bangalore", budget="medium", limit=1)

    result = engine.recommend(prefs, [candidate])
    assert result["recommendations"][0]["restaurant_id"] == "r_1"


def test_recommendation_engine_retries_then_succeeds():
    candidate = Restaurant(
        id="r_1",
        name="North Spice",
        city="Bangalore",
        cuisine="North Indian",
        rating=4.5,
        rating_count=100,
        cost_for_two=400,
    )
    client = MockLLMClient(valid_llm_response("r_1"), fail_times=1)
    engine = RecommendationEngine(client=client)
    prefs = UserPreferences(location="Bangalore", budget="medium", limit=1)

    result = engine.recommend(prefs, [candidate])
    assert result["recommendations"]


def test_recommendation_engine_not_configured():
    engine = RecommendationEngine(client=None)
    assert engine.is_available is False
