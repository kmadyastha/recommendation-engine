"""Tests for empty dataset edge case."""

from pathlib import Path

from src.data.loader import read_raw_csv
from src.data.pipeline import run_pipeline
from src.data.preprocessor import preprocess_dataframe


def test_empty_csv_pipeline(tmp_path: Path):
    empty_csv = tmp_path / "empty.csv"
    empty_csv.write_text("id,name,city,rating,rating_count,cost,cuisine\n", encoding="utf-8")

    raw = read_raw_csv(empty_csv)
    assert raw.empty

    processed = preprocess_dataframe(raw)
    assert processed.empty

    output = tmp_path / "empty.parquet"
    run_pipeline(raw_path=empty_csv, output_path=output)
    assert output.exists()
