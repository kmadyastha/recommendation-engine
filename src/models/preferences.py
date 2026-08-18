"""User preference models for restaurant search."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

BudgetTier = Literal["low", "medium", "high"]


class UserPreferences(BaseModel):
    """User inputs for restaurant recommendations."""

    location: str = Field(..., min_length=1, description="City or location")
    budget: BudgetTier = Field(..., description="Budget tier: low, medium, or high")
    cuisine: str | None = Field(default=None, description="Preferred cuisine (optional)")
    min_rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Minimum rating")
    additional_preferences: str | None = Field(
        default=None,
        description="Free-text extras (e.g. family-friendly)",
    )
    limit: int = Field(default=5, ge=1, le=50, description="Max recommendations to return")

    @field_validator("location", "cuisine", "additional_preferences", mode="before")
    @classmethod
    def strip_optional_strings(cls, value: object) -> object:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            return stripped if stripped else None
        return value

    @field_validator("location")
    @classmethod
    def location_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("location must not be empty")
        return value.strip()
