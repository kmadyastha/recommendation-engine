# Column Mapping: Raw Kaggle CSV → Internal Model

Source dataset: [Swiggy Restaurants Dataset](https://www.kaggle.com/datasets/ashishjangra27/swiggy-restaurants-dataset)

## Expected raw columns (`swiggy.csv`)

| Raw column | Internal field | Notes |
|------------|----------------|-------|
| `id` | `id` | Prefixed as `r_{id}` if numeric source id |
| `name` | `name` | Required |
| `city` | `city` | Normalized via alias map |
| `rating` | `rating` | Float 0–5; non-numeric → null |
| `rating_count` | `rating_count` | Integer; missing → 0 |
| `cost` | `cost_for_two` | Parsed from strings like `₹ 450` |
| `cuisine` | `cuisine` | Original display string |
| `cuisine` (parsed) | `cuisines` | List of cuisine tokens |

## Alternate column names

The loader resolves columns using `data/config/column_mapping.json`. Common alternates from other Swiggy CSV exports are supported (e.g. `Restaurant`, `Food type`, `Price`).

## Dropped rows

Rows are dropped when:

- `name` or `city` is missing or blank after normalization

## Optional raw columns (not stored)

`lic_no`, `link`, `address`, `menu` — ignored unless mapped in future phases.
