import type { RecommendationSource } from "@/lib/types";
import { SOURCE_LABELS } from "@/lib/types";

interface SourceBadgeProps {
  source: RecommendationSource;
}

export function SourceBadge({ source }: SourceBadgeProps) {
  return (
    <div className="flex items-center gap-xs rounded-full border border-surface-container-high bg-surface-container px-sm py-xs">
      <span className="material-symbols-outlined text-[16px] text-tertiary-container">
        auto_awesome
      </span>
      <span className="text-label-caps uppercase tracking-wider text-on-surface-variant">
        {SOURCE_LABELS[source]}
      </span>
    </div>
  );
}
