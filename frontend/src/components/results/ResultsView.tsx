import type { PreferenceFormValues, RecommendationResponse } from "@/lib/types";
import { AISummary } from "./AISummary";
import { PreferenceSidebar } from "./PreferenceSidebar";
import { RecommendationCard } from "./RecommendationCard";
import { SourceBadge } from "../ui/SourceBadge";

interface ResultsViewProps {
  response: RecommendationResponse;
  formValues: PreferenceFormValues;
  onEdit: () => void;
  onSearchAgain: () => void;
}

export function ResultsView({
  response,
  formValues,
  onEdit,
  onSearchAgain,
}: ResultsViewProps) {
  const { recommendations, summary, meta } = response;

  return (
    <div className="mx-auto flex w-full max-w-[1280px] flex-col gap-lg md:flex-row">
      <PreferenceSidebar values={formValues} onEdit={onEdit} />

      <section className="flex w-full flex-col gap-md md:w-2/3 lg:w-3/4">
        <AISummary summary={summary} />

        <div className="mt-sm flex flex-wrap items-center justify-between gap-sm">
          <span className="text-title-md text-on-surface">
            {meta.returned} result{meta.returned === 1 ? "" : "s"} found
          </span>
          <div className="flex flex-wrap items-center gap-sm">
            <span className="text-body-sm text-on-surface-variant">
              {meta.total_candidates.toLocaleString()} candidates matched
            </span>
            <SourceBadge source={meta.source} />
          </div>
        </div>

        <div className="mt-sm flex flex-col gap-md">
          {recommendations.map((item) => (
            <RecommendationCard key={`${item.rank}-${item.restaurant_name}`} item={item} />
          ))}
        </div>

        <div className="mt-lg flex justify-center pb-xl">
          <button
            type="button"
            onClick={onSearchAgain}
            className="rounded-full border border-surface-container-high bg-transparent px-lg py-xs text-title-md text-on-surface transition-colors hover:bg-surface-container"
          >
            Search again
          </button>
        </div>
      </section>
    </div>
  );
}
