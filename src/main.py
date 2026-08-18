"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src import app_state
from src.api.routes import router
from src.config import get_cors_origins, load_budget_tiers
from src.data.store import RestaurantStore, RestaurantStoreError
from src.services.filter_service import FilterService
from src.services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app_state.budget_tiers = load_budget_tiers()
    try:
        app_state.restaurant_store = RestaurantStore.load()
        logger.info("Restaurant store ready: %s", app_state.restaurant_store.stats())
    except RestaurantStoreError as exc:
        app_state.data_load_error = str(exc)
        app_state.restaurant_store = RestaurantStore()
        logger.warning("Restaurant store not loaded: %s", exc)

    app_state.filter_service = FilterService(
        app_state.restaurant_store,
        budget_tiers=app_state.budget_tiers,
    )
    app_state.recommendation_service = RecommendationService(app_state.filter_service)
    yield


app = FastAPI(
    title="Restaurant Recommendation API",
    description="AI-powered food delivery recommendation service (Swiggy use case)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
