# Restaurant Recommendation Engine

AI-powered restaurant recommendation service inspired by Swiggy. Combines structured restaurant data with LLM reasoning to produce personalized, grounded recommendations.

## Documentation

| Document | Description |
|----------|-------------|
| [Docs/problemStatement.md](Docs/problemStatement.md) | Product scope and success criteria |
| [Docs/architecture.md](Docs/architecture.md) | System architecture |
| [Docs/implementation-plan.md](Docs/implementation-plan.md) | Phasewise build plan |
| [Docs/edge-case.md](Docs/edge-case.md) | Edge cases and test scenarios |
| [Docs/eval.md](Docs/eval.md) | Evaluation and sign-off criteria |

## Prerequisites

- Python 3.11+
- pip

## Setup

### 1. Clone and install dependencies

```bash
cd recommendation-engine
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and set your values:

| Variable | Description |
|----------|-------------|
| `LLM_API_KEY` | API key (Groq, OpenAI, etc.) |
| `LLM_BASE_URL` | For Groq: `https://api.groq.com/openai/v1` |
| `LLM_MODEL` | For Groq: `llama-3.3-70b-versatile` |
| `DATA_PATH` | Path to processed dataset (Phase 1+) |
| `BUDGET_TIERS_PATH` | Path to budget tier config (default: `data/config/budget_tiers.json`) |

### Which data file is used?

| File | Purpose | Used by API? |
|------|---------|--------------|
| `data/raw/data.json/data.json` | **Your full Kaggle download (~1 GB)** | Source only — must be preprocessed once |
| `data/processed/restaurants.parquet` | **Cleaned data the API reads** | **Yes — this is what powers recommendations** |
| `data/raw/swiggy_sample.csv` | Tiny 16-row file for automated tests only | **No** (tests use a temp copy) |

After preprocessing your JSON, the API uses **`restaurants.parquet`** (currently **53,013 restaurants, 531 cities**). You do **not** need the 16-row sample file for normal use.

### 3. Prepare restaurant data

**Option A — Sample data (development / tests)**

A sample CSV is included at `data/raw/swiggy_sample.csv`. Preprocess it:

```bash
python -m src.data.loader --raw data/raw/swiggy_sample.csv
```

**Option B — Full Kaggle dataset (CSV or JSON)**

Download the [Swiggy Restaurants Dataset](https://www.kaggle.com/datasets/ashishjangra27/swiggy-restaurants-dataset) and place either:

- `swiggy.csv` in `data/raw/`, or
- `data.json` in `data/raw/` (Kaggle often extracts as `data/raw/data.json/data.json`)

Then run:

```bash
python -m src.data.loader
```

For the large JSON file (~1 GB), preprocessing may take several minutes and requires several GB of free RAM.

Or point directly at your JSON file:

```bash
python -m src.data.loader --raw data/raw/data.json/data.json
```

This writes `data/processed/restaurants.parquet`. Column mapping is documented in [data/config/COLUMN_MAPPING.md](data/config/COLUMN_MAPPING.md).

## Run the API

From the project root:

```bash
uvicorn src.main:app --reload
```

The API starts at `http://127.0.0.1:8000`.

- Health check: `GET http://127.0.0.1:8000/api/v1/health`
- OpenAPI docs: `http://127.0.0.1:8000/docs`

## Run the BiteWise frontend (Phase 6)

The UI lives in `frontend/` (Next.js 14, TypeScript, Tailwind). It uses the Stitch BiteWise dark-theme design and connects to the FastAPI backend.

### 1. Install frontend dependencies

```bash
cd frontend
npm install
cp .env.local.example .env.local
```

### 2. Start both servers (two terminals)

**Terminal 1 — API**

```bash
# from project root
uvicorn src.main:app --reload
```

**Terminal 2 — Frontend**

```bash
cd frontend
npm run dev
```

Open **http://localhost:3000** in your browser.

The frontend proxies `/api/v1/*` to the backend via `next.config.mjs` rewrites, so CORS is not required in dev (CORS is still enabled for direct API access).

### UI features

- Searchable city and cuisine dropdowns (from live API)
- Budget pills, star rating, optional vibe text, result count
- Loading skeletons during LLM calls
- Ranked restaurant cards with AI explanations
- Empty and error states
- API status modal (footer or header)
- **Placeholder food images:** 10 generic Unsplash images assigned deterministically per restaurant name (real images not in dataset yet)

### Production build

```bash
cd frontend
npm run build
npm start
```

### Example health check

```bash
curl http://127.0.0.1:8000/api/v1/health
```

### Example recommendations request

```bash
curl -X POST http://127.0.0.1:8000/api/v1/recommendations \
  -H "Content-Type: application/json" \
  -d "{\"location\":\"Bangalore\",\"budget\":\"medium\",\"cuisine\":\"North Indian\",\"min_rating\":4.0,\"limit\":5}"
```

List cities and cuisines:

```bash
curl http://127.0.0.1:8000/api/v1/cities
curl http://127.0.0.1:8000/api/v1/cuisines
```

Expected response:

```json
{
  "status": "ok",
  "ready": true,
  "budget_tiers_loaded": true,
  "budget_tier_keys": ["low", "medium", "high"],
  "data_loaded": true,
  "data_path": "data/processed/restaurants.parquet",
  "restaurant_count": 14,
  "city_count": 4,
  "llm_configured": false
}
```

## Run tests

```bash
pytest tests/ -v
```

## Project structure

```
recommendation-engine/
├── Docs/                   # Project documentation
├── data/
│   ├── config/             # Budget tiers and other config
│   ├── raw/                # Original Kaggle download (gitignored)
│   └── processed/          # Cleaned dataset (Phase 1+)
├── src/
│   ├── config.py           # Settings and budget tier loader
│   ├── main.py             # FastAPI application
│   ├── data/
│   │   ├── loader.py       # Raw CSV loader
│   │   ├── preprocessor.py # Cleaning and normalization
│   │   ├── store.py        # In-memory restaurant store
│   │   └── pipeline.py     # Offline preprocess CLI
│   ├── models/
│   │   ├── restaurant.py   # Restaurant domain model
│   │   └── preferences.py  # User preference model
│   ├── api/
│   │   ├── routes.py       # REST endpoints
│   │   └── schemas.py      # Request/response models
│   └── services/
│       ├── filter_service.py    # Deterministic filtering
│       └── fallback_ranker.py   # Rule-based ranking
├── tests/
├── frontend/               # BiteWise Next.js UI (Phase 6)
├── stitch_bitewise_ai_recommendation_interface/  # Google Stitch design reference
├── requirements.txt
├── .env.example
└── README.md
```

## Implementation status

- [x] **Phase 0** — Project foundation, health endpoint, config
- [x] **Phase 1** — Data ingestion and storage
- [x] **Phase 2** — Filter service
- [x] **Phase 3** — REST API (rule-based MVP)
- [x] **Phase 4** — LLM integration
- [x] **Phase 5** — Validation and grounding
- [x] **Phase 6** — BiteWise web UI (Next.js + Tailwind)
- [ ] **Phase 7** — Testing, observability, deployment

## License

See repository license file if applicable.
