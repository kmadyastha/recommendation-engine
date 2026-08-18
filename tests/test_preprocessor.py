"""Tests for data preprocessing."""

import pandas as pd

from src.data.preprocessor import (
    normalize_city,
    parse_cost,
    parse_cuisines,
    parse_rating,
    parse_rating_count,
    preprocess_dataframe,
)


def test_normalize_city_aliases():
    assert normalize_city("Bengaluru") == "Bangalore"
    assert normalize_city(" bangalore ") == "Bangalore"
    assert normalize_city("BANGALORE") == "Bangalore"


def test_parse_cost_variants():
    assert parse_cost("450") == 450.0
    assert parse_cost("₹450") == 450.0
    assert parse_cost("₹ 200") == 200.0
    assert parse_cost("450 for two") == 450.0
    assert parse_cost("") is None
    assert parse_cost(None) is None


def test_parse_rating_invalid_tokens():
    assert parse_rating("NEW") is None
    assert parse_rating("--") is None
    assert parse_rating("Too Few Ratings") is None
    assert parse_rating(4.5) == 4.5
    assert parse_rating(6.0) is None
    assert parse_rating(-1) is None


def test_parse_cuisines_multi():
    display, tokens = parse_cuisines("North Indian, Chinese")
    assert display == "North Indian, Chinese"
    assert tokens == ["North Indian", "Chinese"]


def test_parse_rating_count():
    assert parse_rating_count(0) == 0
    assert parse_rating_count("Too Few Ratings") == 0
    assert parse_rating_count(1200) == 1200
    assert parse_rating_count("50+ ratings") == 50
    assert parse_rating_count("1K+ ratings") == 1000


def test_preprocess_drops_invalid_rows():
    raw = pd.DataFrame(
        [
            {
                "id": 1,
                "name": "Valid Place",
                "city": "Bengaluru",
                "rating": 4.2,
                "rating_count": 10,
                "cost": "₹ 300",
                "cuisine": "North Indian",
            },
            {
                "id": 2,
                "name": "",
                "city": "Bangalore",
                "rating": 4.0,
                "rating_count": 10,
                "cost": 300,
                "cuisine": "Chinese",
            },
            {
                "id": 3,
                "name": "No City",
                "city": "",
                "rating": 4.0,
                "rating_count": 10,
                "cost": 300,
                "cuisine": "Chinese",
            },
        ]
    )
    processed = preprocess_dataframe(raw)
    assert len(processed) == 1
    assert processed.iloc[0]["city"] == "Bangalore"
    assert processed.iloc[0]["cost_for_two"] == 300.0


def test_preprocess_generates_unique_ids_for_duplicates():
    raw = pd.DataFrame(
        [
            {
                "id": 99,
                "name": "Dup Place",
                "city": "Bangalore",
                "rating": 4.0,
                "rating_count": 10,
                "cost": 300,
                "cuisine": "North Indian",
            },
            {
                "id": 99,
                "name": "Dup Place",
                "city": "Bangalore",
                "rating": 4.0,
                "rating_count": 10,
                "cost": 300,
                "cuisine": "North Indian",
            },
        ]
    )
    processed = preprocess_dataframe(raw)
    assert len(processed) == 2
    assert processed["id"].nunique() == 2
