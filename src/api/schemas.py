"""API request and response schemas."""

from typing import Literal

from pydantic import BaseModel, Field

from src.models.preferences import BudgetTier


class RecommendationRequest(BaseModel):
    location: str = Field(..., min_length=1, description="City or location")
    budget: BudgetTier = Field(..., description="Budget tier: low, medium, or high")
    cuisine: str | None = Field(default=None, description="Preferred cuisine")
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0)
    additional_preferences: str | None = Field(default=None)
    limit: int = Field(default=5, ge=1, le=50)


class RecommendationItem(BaseModel):
    rank: int
    restaurant_name: str
    cuisine: str
    rating: float | None
    cost_for_two: float | None
    location: str
    why_recommended: str


class RecommendationMeta(BaseModel):
    total_candidates: int
    returned: int
    source: Literal["rule_based", "llm", "fallback"]


class RecommendationResponse(BaseModel):
    query: RecommendationRequest
    summary: str | None = None
    recommendations: list[RecommendationItem] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    empty_reason: str | None = None
    meta: RecommendationMeta


class HealthResponse(BaseModel):
    status: str
    ready: bool
    budget_tiers_loaded: bool
    budget_tier_keys: list[str]
    data_loaded: bool
    data_path: str
    data_error: str | None = None
    restaurant_count: int
    city_count: int
    avg_rating: float | None = None
    avg_cost_for_two: float | None = None
    llm_configured: bool
