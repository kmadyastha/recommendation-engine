import type {
  HealthResponse,
  RecommendationRequest,
  RecommendationResponse,
} from "./types";

function apiBase(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";
  }
  return "";
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${apiBase()}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new Error(detail || `Request failed (${response.status})`);
  }

  return response.json() as Promise<T>;
}

export async function getHealth(): Promise<HealthResponse> {
  return fetchJson<HealthResponse>("/api/v1/health");
}

export async function getCities(): Promise<string[]> {
  const data = await fetchJson<{ cities: string[] }>("/api/v1/cities");
  return data.cities;
}

export async function getCuisines(): Promise<string[]> {
  const data = await fetchJson<{ cuisines: string[] }>("/api/v1/cuisines");
  return data.cuisines;
}

export async function postRecommendations(
  request: RecommendationRequest,
): Promise<RecommendationResponse> {
  const payload: RecommendationRequest = {
    ...request,
    cuisine: request.cuisine?.trim() || null,
    additional_preferences: request.additional_preferences?.trim() || null,
  };

  return fetchJson<RecommendationResponse>("/api/v1/recommendations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
