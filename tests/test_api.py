"""Integration tests for REST API."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["data_loaded"] is True


def test_list_cities(client: TestClient):
    response = client.get("/api/v1/cities")
    assert response.status_code == 200
    cities = response.json()["cities"]
    assert "Bangalore" in cities


def test_list_cuisines(client: TestClient):
    response = client.get("/api/v1/cuisines")
    assert response.status_code == 200
    cuisines = response.json()["cuisines"]
    assert len(cuisines) > 0


def test_recommendations_happy_path(client: TestClient):
    payload = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "North Indian",
        "min_rating": 4.0,
        "limit": 5,
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["meta"]["source"] in {"rule_based", "llm", "fallback"}
    assert body["meta"]["returned"] > 0
    assert body["meta"]["total_candidates"] >= body["meta"]["returned"]
    assert len(body["recommendations"]) == body["meta"]["returned"]

    for item in body["recommendations"]:
        assert item["restaurant_name"]
        assert item["cuisine"]
        assert item["location"] == "Bangalore"
        assert item["why_recommended"]
        if item["rating"] is not None:
            assert item["rating"] >= 4.0
        if item["cost_for_two"] is not None:
            assert 300 <= item["cost_for_two"] <= 600


def test_recommendations_invalid_budget(client: TestClient):
    payload = {
        "location": "Bangalore",
        "budget": "luxury",
        "min_rating": 4.0,
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 422


def test_recommendations_missing_location(client: TestClient):
    response = client.post("/api/v1/recommendations", json={"budget": "medium"})
    assert response.status_code == 422


def test_recommendations_unknown_city_empty_with_suggestions(client: TestClient):
    payload = {
        "location": "Tokyo",
        "budget": "medium",
        "cuisine": "Japanese",
        "min_rating": 4.0,
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["recommendations"] == []
    assert body["meta"]["returned"] == 0
    assert body["empty_reason"] == "no_restaurants_in_city"
    assert body["suggestions"]


def test_recommendations_over_constrained_filters(client: TestClient):
    payload = {
        "location": "Bangalore",
        "budget": "medium",
        "cuisine": "North Indian",
        "min_rating": 5.0,
    }
    response = client.post("/api/v1/recommendations", json=payload)
    assert response.status_code == 200
    body = response.json()

    assert body["recommendations"] == []
    assert body["empty_reason"] == "no_matches_for_filters"
    assert body["suggestions"]


def test_recommendations_facts_from_dataset(client: TestClient):
    """All display fields should be consistent with filtered constraints."""
    payload = {
        "location": "Bangalore",
        "budget": "medium",
        "min_rating": 0.0,
        "limit": 3,
    }
    response = client.post("/api/v1/recommendations", json=payload)
    body = response.json()

    assert response.status_code == 200
    assert len(body["recommendations"]) <= 3
    for item in body["recommendations"]:
        assert item["location"] == "Bangalore"
        assert item["cost_for_two"] is None or (300 <= item["cost_for_two"] <= 600)
