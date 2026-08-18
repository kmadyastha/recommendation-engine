"""Offline data ingestion pipeline CLI."""

import argparse
import logging
import sys
import time
from pathlib import Path

from src.config import PROJECT_ROOT, get_settings
from src.data.loader import DatasetLoadError, read_raw_dataset
from src.data.preprocessor import log_sample_rows, preprocess_dataframe

logger = logging.getLogger(__name__)


def run_pipeline(
    raw_path: Path | None = None,
    output_path: Path | None = None,
    raw_dir: Path | None = None,
) -> Path:
    """Load raw dataset, preprocess, and write parquet output."""
    settings = get_settings()
    output = output_path or settings.data_path
    if not output.is_absolute():
        output = PROJECT_ROOT / output

    output.parent.mkdir(parents=True, exist_ok=True)

    raw_df = read_raw_dataset(raw_path, raw_dir)
    processed = preprocess_dataframe(raw_df)
    log_sample_rows(processed, count=10)

    processed.to_parquet(output, index=False)
    logger.info("Wrote %d rows to %s", len(processed), output)
    return output


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )

    parser = argparse.ArgumentParser(description="Preprocess Swiggy restaurant dataset")
    parser.add_argument(
        "--raw",
        type=Path,
        help="Path to raw CSV or JSON file (default: search data/raw/)",
    )
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "raw",
        help="Directory to search for raw CSV",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output parquet path (default: DATA_PATH from settings)",
    )
    args = parser.parse_args(argv)

    start = time.perf_counter()
    try:
        output = run_pipeline(args.raw, args.output, args.raw_dir)
    except DatasetLoadError as exc:
        logger.error("%s", exc)
        return 1

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info("Pipeline completed in %.0f ms", elapsed_ms)
    return 0


if __name__ == "__main__":
    sys.exit(main())
