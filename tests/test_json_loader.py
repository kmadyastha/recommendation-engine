"""Tests for JSON dataset loading."""

from src.data.loader import flatten_kaggle_json, resolve_raw_path
from src.config import PROJECT_ROOT


def test_flatten_kaggle_json_structure():
    data = {
        "Abohar": {
            "link": "https://www.swiggy.com/city/abohar",
            "restaurants": {
                "567335": {
                    "name": "AB FOODS POINT",
                    "rating": "--",
                    "rating_count": "Too Few Ratings",
                    "cost": "₹ 200",
                    "cuisine": "Beverages,Pizzas",
                }
            },
        },
        "Bangalore": {
            "restaurants": {
                "211": {
                    "name": "Tandoor Hut",
                    "rating": "4.4",
                    "rating_count": "1K+ ratings",
                    "cost": "₹ 300",
                    "cuisine": "North Indian,Chinese",
                }
            }
        },
    }
    df = flatten_kaggle_json(data)
    assert len(df) == 2
    assert set(df["city"]) == {"Abohar", "Bangalore"}
    assert df.iloc[0]["id"] == "567335"


def test_resolve_full_json_path():
    path = resolve_raw_path(PROJECT_ROOT / "data/raw/data.json")
    assert path.name == "data.json"
    assert path.exists()
