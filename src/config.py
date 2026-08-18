"""Application configuration and budget tier loading."""

from functools import lru_cache
from pathlib import Path
from typing import Any

import json
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BUDGET_TIERS_PATH = PROJECT_ROOT / "data" / "config" / "budget_tiers.json"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    llm_api_key: str | None = Field(default=None, alias="LLM_API_KEY")
    llm_base_url: str | None = Field(default=None, alias="LLM_BASE_URL")
    llm_model: str = Field(default="llama-3.1-8b-instant", alias="LLM_MODEL")
    llm_temperature: float = Field(default=0.3, alias="LLM_TEMPERATURE")
    data_path: Path = Field(
        default=PROJECT_ROOT / "data" / "processed" / "restaurants.parquet",
        alias="DATA_PATH",
    )
    budget_tiers_path: Path = Field(
        default=DEFAULT_BUDGET_TIERS_PATH,
        alias="BUDGET_TIERS_PATH",
    )
    cors_origins: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="CORS_ORIGINS",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_cors_origins() -> list[str]:
    """Parse comma-separated CORS origins from settings."""
    return [origin.strip() for origin in get_settings().cors_origins.split(",") if origin.strip()]


def load_budget_tiers(path: Path | None = None) -> dict[str, Any]:
    """Load and validate budget tier configuration from JSON."""
    tiers_path = path or get_settings().budget_tiers_path
    if not tiers_path.is_absolute():
        tiers_path = PROJECT_ROOT / tiers_path

    with tiers_path.open(encoding="utf-8") as f:
        tiers = json.load(f)

    required = {"low", "medium", "high"}
    if not required.issubset(tiers.keys()):
        missing = required - set(tiers.keys())
        raise ValueError(f"Budget tiers config missing keys: {sorted(missing)}")

    for name in required:
        tier = tiers[name]
        if "min" not in tier:
            raise ValueError(f"Budget tier '{name}' must define 'min'")

    return tiers
