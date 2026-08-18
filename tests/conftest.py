"""Shared pytest fixtures."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.config import PROJECT_ROOT, get_settings
from src.data.pipeline import run_pipeline
from src.main import app

SAMPLE_CSV = PROJECT_ROOT / "data/raw/swiggy_sample.csv"


@pytest.fixture(scope="module")
def sample_parquet(tmp_path_factory) -> Path:
    output_dir = tmp_path_factory.mktemp("processed")
    output = output_dir / "restaurants.parquet"
    run_pipeline(raw_path=SAMPLE_CSV, output_path=output)
    return output


@pytest.fixture(scope="module")
def client(sample_parquet: Path):
    import os

    os.environ["DATA_PATH"] = str(sample_parquet)
    get_settings.cache_clear()

    with TestClient(app) as test_client:
        yield test_client

    get_settings.cache_clear()
