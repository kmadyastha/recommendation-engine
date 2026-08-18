"""Tests for dataset loader."""

from pathlib import Path

import pandas as pd
import pytest

from src.config import PROJECT_ROOT
from src.data.loader import DatasetLoadError, map_raw_columns, read_raw_csv, resolve_raw_path


def test_resolve_sample_csv():
    path = resolve_raw_path(PROJECT_ROOT / "data/raw/swiggy_sample.csv")
    assert path.exists()


def test_read_sample_csv():
    df = read_raw_csv(PROJECT_ROOT / "data/raw/swiggy_sample.csv")
    assert len(df) > 0
    assert "name" in df.columns
    assert "city" in df.columns
    assert "cuisine" in df.columns


def test_missing_raw_file_raises():
    with pytest.raises(DatasetLoadError):
        resolve_raw_path(PROJECT_ROOT / "data/raw/does_not_exist.csv")


def test_map_raw_columns_alternate_names():
    raw = pd.DataFrame(
        {
            "Restaurant": ["Test Rest"],
            "City": ["Bangalore"],
            "Food type": ["Chinese"],
            "Price": [300],
            "Avg ratings": [4.2],
            "Total ratings": [100],
        }
    )
    mapped = map_raw_columns(raw)
    assert mapped["name"].iloc[0] == "Test Rest"
    assert mapped["city"].iloc[0] == "Bangalore"
    assert mapped["cuisine"].iloc[0] == "Chinese"

