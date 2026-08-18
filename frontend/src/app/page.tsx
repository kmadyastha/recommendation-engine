"use client";

import { useCallback, useEffect, useState } from "react";
import { BackgroundEffects } from "@/components/layout/BackgroundEffects";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { Hero } from "@/components/layout/Hero";
import { PreferenceForm } from "@/components/forms/PreferenceForm";
import { ResultsView } from "@/components/results/ResultsView";
import { PreferenceSidebar } from "@/components/results/PreferenceSidebar";
import { EmptyState } from "@/components/ui/EmptyState";
import { ErrorState } from "@/components/ui/ErrorState";
import { LoadingSkeleton } from "@/components/ui/LoadingSkeleton";
import { StatusModal } from "@/components/ui/StatusModal";
import { getCities, getCuisines, getHealth, postRecommendations } from "@/lib/api";
import type {
  PreferenceFormValues,
  RecommendationResponse,
} from "@/lib/types";
import { DEFAULT_FORM_VALUES } from "@/lib/types";

type ViewState = "form" | "loading" | "results" | "empty" | "error";

export default function HomePage() {
  const [view, setView] = useState<ViewState>("form");
  const [cities, setCities] = useState<string[]>([]);
  const [cuisines, setCuisines] = useState<string[]>([]);
  const [formValues, setFormValues] = useState<PreferenceFormValues>(DEFAULT_FORM_VALUES);
  const [response, setResponse] = useState<RecommendationResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState("");
  const [restaurantCount, setRestaurantCount] = useState<number>();
  const [cityCount, setCityCount] = useState<number>();
  const [statusOpen, setStatusOpen] = useState(false);
  const [catalogError, setCatalogError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCatalog() {
      try {
        const [health, cityList, cuisineList] = await Promise.all([
          getHealth(),
          getCities(),
          getCuisines(),
        ]);
        setRestaurantCount(health.restaurant_count);
        setCityCount(health.city_count);
        setCities(cityList);
        setCuisines(cuisineList);
      } catch (err) {
        setCatalogError(err instanceof Error ? err.message : "Failed to load data");
      }
    }
    loadCatalog();
  }, []);

  const submitSearch = useCallback(async (values: PreferenceFormValues) => {
    setFormValues(values);
    setView("loading");
    setErrorMessage("");

    try {
      const result = await postRecommendations({
        location: values.location,
        budget: values.budget,
        cuisine: values.cuisine || null,
        min_rating: values.min_rating,
        additional_preferences: values.additional_preferences || null,
        limit: values.limit,
      });

      setResponse(result);

      if (result.recommendations.length === 0) {
        setView("empty");
      } else {
        setView("results");
      }
    } catch (err) {
      setErrorMessage(
        err instanceof Error ? err.message : "Unable to fetch recommendations",
      );
      setView("error");
    }
  }, []);

  const backToForm = useCallback(() => {
    setView("form");
    setResponse(null);
    setErrorMessage("");
  }, []);

  const showResults = view === "results" || view === "empty" || view === "error";

  return (
    <div className="relative flex min-h-screen flex-col">
      <BackgroundEffects />
      <Header
        showEdit={showResults}
        onEditSearch={backToForm}
      />

      <main className="z-10 flex flex-grow flex-col px-margin-mobile pb-xl pt-32 md:px-margin-desktop">
        {view === "form" && (
          <div className="flex flex-col items-center">
            <Hero restaurantCount={restaurantCount} cityCount={cityCount} />
            {catalogError && (
              <p className="mb-md max-w-xl text-center text-body-sm text-error">
                Could not load cities/cuisines: {catalogError}. Start the API at{" "}
                <code className="text-secondary">http://127.0.0.1:8000</code>
              </p>
            )}
            <PreferenceForm
              cities={cities}
              cuisines={cuisines}
              defaultValues={formValues}
              onSubmit={submitSearch}
            />
          </div>
        )}

        {view === "loading" && (
          <div className="mx-auto flex w-full max-w-[1280px] flex-col items-center gap-lg">
            <div className="w-full max-w-4xl opacity-60 pointer-events-none">
              <PreferenceForm
                cities={cities}
                cuisines={cuisines}
                defaultValues={formValues}
                onSubmit={() => {}}
                disabled
              />
            </div>
            <LoadingSkeleton />
          </div>
        )}

        {view === "results" && response && (
          <ResultsView
            response={response}
            formValues={formValues}
            onEdit={backToForm}
            onSearchAgain={backToForm}
          />
        )}

        {view === "empty" && response && (
          <div className="mx-auto flex w-full max-w-[1280px] flex-col items-center gap-lg md:flex-row md:items-start">
            <aside className="w-full md:w-1/3 lg:w-1/4">
              <PreferenceSidebar values={formValues} onEdit={backToForm} />
            </aside>
            <EmptyState
              reason={response.empty_reason}
              suggestions={response.suggestions}
              onAdjust={backToForm}
              onSuggestionClick={() => backToForm()}
            />
          </div>
        )}

        {view === "error" && (
          <div className="mx-auto flex w-full justify-center">
            <ErrorState
              message={errorMessage}
              onRetry={() => submitSearch(formValues)}
              onBack={backToForm}
            />
          </div>
        )}
      </main>

      <Footer onStatusClick={() => setStatusOpen(true)} />
      <StatusModal open={statusOpen} onClose={() => setStatusOpen(false)} />
    </div>
  );
}
