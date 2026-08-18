"""Tests for health endpoint and configuration."""

from fastapi.testclient import TestClient

from src.config import load_budget_tiers


def test_health_returns_200(client: TestClient):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["ready"] is True
    assert body["budget_tiers_loaded"] is True
    assert set(body["budget_tier_keys"]) == {"low", "medium", "high"}
    assert body["data_loaded"] is True
    assert body["restaurant_count"] > 0


def test_budget_tiers_load():
    tiers = load_budget_tiers()
    assert "low" in tiers
    assert "medium" in tiers
    assert "high" in tiers
    assert tiers["medium"]["min"] == 300
    assert tiers["medium"]["max"] == 600
