"""Restaurant domain model."""

from pydantic import BaseModel, Field


class Restaurant(BaseModel):
    """Normalized restaurant record from the Swiggy dataset."""

    id: str = Field(..., description="Stable internal restaurant ID")
    name: str = Field(..., description="Restaurant name")
    city: str = Field(..., description="Normalized city name")
    cuisine: str = Field(..., description="Display cuisine string from source")
    cuisines: list[str] = Field(
        default_factory=list,
        description="Parsed cuisine tokens for filtering",
    )
    cost_for_two: float | None = Field(
        default=None,
        description="Cost for two in INR",
    )
    rating: float | None = Field(
        default=None,
        ge=0,
        le=5,
        description="Average rating",
    )
    rating_count: int = Field(default=0, ge=0, description="Number of ratings")
