"""Orchestrate filtering, LLM reasoning, validation, and fallback."""

import logging
import time

from src.api.schemas import RecommendationMeta, RecommendationRequest, RecommendationResponse
from src.models.preferences import UserPreferences
from src.services.fallback_ranker import build_summary, rank_restaurants
from src.services.filter_service import FilterResult, FilterService
from src.services.recommendation_engine import RecommendationEngine
from src.services.validator import (
    RecommendationValidator,
    ValidationError,
    enrich_fallback,
    enrich_recommendations,
)

logger = logging.getLogger(__name__)


class RecommendationService:
    def __init__(
        self,
        filter_service: FilterService,
        engine: RecommendationEngine | None = None,
        validator: RecommendationValidator | None = None,
    ) -> None:
        self._filter_service = filter_service
        self._engine = engine or RecommendationEngine()
        self._validator = validator or RecommendationValidator()

    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        preferences = UserPreferences(
            location=request.location,
            budget=request.budget,
            cuisine=request.cuisine,
            min_rating=request.min_rating,
            additional_preferences=request.additional_preferences,
            limit=request.limit,
        )

        filter_result = self._filter_service.filter(preferences)
        if filter_result.is_empty:
            return self._empty_response(request, filter_result)

        if self._engine.is_available:
            try:
                return self._llm_response(request, preferences, filter_result)
            except (ValidationError, RuntimeError, ValueError) as exc:
                logger.warning("LLM path failed, using fallback: %s", exc)
                return self._fallback_response(request, preferences, filter_result)

        return self._rule_based_response(request, preferences, filter_result, source="rule_based")

    def _empty_response(
        self,
        request: RecommendationRequest,
        filter_result: FilterResult,
    ) -> RecommendationResponse:
        return RecommendationResponse(
            query=request,
            summary=None,
            recommendations=[],
            suggestions=filter_result.suggestions,
            empty_reason=filter_result.empty_reason,
            meta=RecommendationMeta(
                total_candidates=0,
                returned=0,
                source="rule_based",
            ),
        )

    def _llm_response(
        self,
        request: RecommendationRequest,
        preferences: UserPreferences,
        filter_result: FilterResult,
    ) -> RecommendationResponse:
        start = time.perf_counter()
        llm_data = self._engine.recommend(preferences, filter_result.candidates)
        validated = self._validator.validate(
            llm_data.get("recommendations", []),
            filter_result.candidates,
            preferences.limit,
        )
        recommendations = enrich_recommendations(validated, filter_result.candidates, preferences)
        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "LLM recommendations: %d returned, %d candidates, %.0f ms",
            len(recommendations),
            filter_result.total_matched,
            elapsed_ms,
        )

        return RecommendationResponse(
            query=request,
            summary=llm_data.get("summary") or build_summary(
                preferences, len(recommendations), filter_result.total_matched
            ),
            recommendations=recommendations,
            suggestions=[],
            empty_reason=None,
            meta=RecommendationMeta(
                total_candidates=filter_result.total_matched,
                returned=len(recommendations),
                source="llm",
            ),
        )

    def _rule_based_response(
        self,
        request: RecommendationRequest,
        preferences: UserPreferences,
        filter_result: FilterResult,
        *,
        source: str,
    ) -> RecommendationResponse:
        ranked = rank_restaurants(filter_result.candidates, preferences.limit)
        recommendations = enrich_fallback(ranked, preferences)

        return RecommendationResponse(
            query=request,
            summary=build_summary(preferences, len(recommendations), filter_result.total_matched),
            recommendations=recommendations,
            suggestions=[],
            empty_reason=None,
            meta=RecommendationMeta(
                total_candidates=filter_result.total_matched,
                returned=len(recommendations),
                source=source,  # type: ignore[arg-type]
            ),
        )

    def _fallback_response(
        self,
        request: RecommendationRequest,
        preferences: UserPreferences,
        filter_result: FilterResult,
    ) -> RecommendationResponse:
        return self._rule_based_response(
            request, preferences, filter_result, source="fallback"
        )

    def list_cities(self) -> list[str]:
        return self._filter_service.list_cities()

    def list_cuisines(self) -> list[str]:
        return self._filter_service.list_cuisines()
