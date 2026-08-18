"""Mock LLM client for tests."""

import json


class MockLLMClient:
    def __init__(self, response: dict | None = None, *, fail_times: int = 0) -> None:
        self._response = response or {}
        self._fail_times = fail_times
        self._calls = 0

    def complete(self, messages: list[dict[str, str]]) -> str:
        self._calls += 1
        if self._calls <= self._fail_times:
            raise ValueError("Simulated LLM failure")
        return json.dumps(self._response)


def valid_llm_response(candidate_id: str = "r_1") -> dict:
    return {
        "summary": "Great North Indian options in Bangalore for your medium budget.",
        "recommendations": [
            {
                "restaurant_id": candidate_id,
                "rank": 1,
                "why_recommended": "Matches your North Indian preference with strong ratings in Bangalore.",
            }
        ],
    }
