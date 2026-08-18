"""Data ingestion and storage (Phase 1)."""

from src.data.loader import read_raw_csv
from src.data.pipeline import run_pipeline
from src.data.preprocessor import preprocess_dataframe
from src.data.store import RestaurantStore
