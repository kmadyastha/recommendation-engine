export type BudgetTier = "low" | "medium" | "high";

export type RecommendationSource = "rule_based" | "llm" | "fallback";

export interface RecommendationRequest {
  location: string;
  budget: BudgetTier;
  cuisine?: string | null;
  min_rating?: number;
  additional_preferences?: string | null;
  limit?: number;
}

export interface RecommendationItem {
  rank: number;
  restaurant_name: string;
  cuisine: string;
  rating: number | null;
  cost_for_two: number | null;
  location: string;
  why_recommended: string;
}

export interface RecommendationMeta {
  total_candidates: number;
  returned: number;
  source: RecommendationSource;
}

export interface RecommendationResponse {
  query: RecommendationRequest;
  summary: string | null;
  recommendations: RecommendationItem[];
  suggestions: string[];
  empty_reason: string | null;
  meta: RecommendationMeta;
}

export interface HealthResponse {
  status: string;
  ready: boolean;
  budget_tiers_loaded: boolean;
  budget_tier_keys: string[];
  data_loaded: boolean;
  data_path: string;
  data_error: string | null;
  restaurant_count: number;
  city_count: number;
  avg_rating: number | null;
  avg_cost_for_two: number | null;
  llm_configured: boolean;
}

export interface PreferenceFormValues {
  location: string;
  budget: BudgetTier;
  cuisine: string;
  min_rating: number;
  additional_preferences: string;
  limit: number;
}

export const DEFAULT_FORM_VALUES: PreferenceFormValues = {
  location: "",
  budget: "medium",
  cuisine: "",
  min_rating: 0,
  additional_preferences: "",
  limit: 5,
};

export const BUDGET_LABELS: Record<BudgetTier, string> = {
  low: "Low (≤₹300)",
  medium: "Medium (₹300–600)",
  high: "High (>₹600)",
};

export const SOURCE_LABELS: Record<RecommendationSource, string> = {
  llm: "AI Powered",
  rule_based: "Smart Ranking",
  fallback: "Backup Ranking",
};
