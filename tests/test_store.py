"""Tests for restaurant store and ingestion pipeline."""

import time
from pathlib import Path

import pytest

from src.config import PROJECT_ROOT
from src.data.pipeline import run_pipeline
from src.data.store import RestaurantStore, RestaurantStoreError


SAMPLE_CSV = PROJECT_ROOT / "data/raw/swiggy_sample.csv"
PROCESSED_FIXTURE = PROJECT_ROOT / "data/processed/test_restaurants.parquet"


@pytest.fixture
def processed_parquet(tmp_path: Path):
    output = tmp_path / "restaurants.parquet"
    run_pipeline(raw_path=SAMPLE_CSV, output_path=output)
    return output


def test_run_pipeline_writes_parquet(processed_parquet: Path):
    assert processed_parquet.exists()
    store = RestaurantStore.from_parquet(processed_parquet)
    assert len(store) > 0
    stats = store.stats()
    assert stats["row_count"] > 0
    assert stats["city_count"] >= 1


def test_store_load_performance(processed_parquet: Path):
    start = time.perf_counter()
    store = RestaurantStore.from_parquet(processed_parquet)
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert len(store) > 0
    assert elapsed_ms < 2000


def test_store_get_by_id(processed_parquet: Path):
    store = RestaurantStore.from_parquet(processed_parquet)
    first_id = store.dataframe.iloc[0]["id"]
    restaurant = store.get_by_id(str(first_id))
    assert restaurant is not None
    assert restaurant.id == str(first_id)


def test_store_list_cities_and_cuisines(processed_parquet: Path):
    store = RestaurantStore.from_parquet(processed_parquet)
    cities = store.list_cities()
    cuisines = store.list_cuisines()
    assert "Bangalore" in cities
    assert any(c.lower() == "north indian" for c in cuisines) or "North Indian" in cuisines


def test_store_missing_file_raises():
    with pytest.raises(RestaurantStoreError):
        RestaurantStore.from_parquet(PROJECT_ROOT / "data/processed/nonexistent.parquet")


def test_build_production_parquet(tmp_path: Path):
    """Generate parquet from sample in temp dir (does not overwrite production data)."""
    output = tmp_path / "restaurants.parquet"
    run_pipeline(raw_path=SAMPLE_CSV, output_path=output)
    store = RestaurantStore.from_parquet(output)
    required_columns = {"name", "city", "cuisine", "cost_for_two", "rating", "rating_count"}
    assert required_columns.issubset(set(store.dataframe.columns))
