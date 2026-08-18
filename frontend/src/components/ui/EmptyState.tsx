interface EmptyStateProps {
  reason?: string | null;
  suggestions: string[];
  onAdjust: () => void;
  onSuggestionClick?: (suggestion: string) => void;
}

export function EmptyState({
  reason,
  suggestions,
  onAdjust,
  onSuggestionClick,
}: EmptyStateProps) {
  return (
    <div className="flex w-full max-w-2xl flex-col items-center rounded-xl border border-outline-variant/30 bg-surface-container-low p-xl text-center">
      <div className="mb-md flex h-16 w-16 items-center justify-center rounded-full bg-surface-container">
        <span className="material-symbols-outlined text-[32px] text-on-surface-variant">
          search_off
        </span>
      </div>
      <h2 className="mb-sm text-title-md text-on-surface">No restaurants match your filters</h2>
      {reason && (
        <p className="mb-md text-body-lg text-on-surface-variant">{reason}</p>
      )}
      {suggestions.length > 0 && (
        <div className="mb-md flex flex-wrap justify-center gap-xs">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => onSuggestionClick?.(suggestion)}
              className="rounded-full border border-outline-variant bg-surface-container px-sm py-xs text-body-sm text-on-surface-variant transition-colors hover:border-primary hover:text-primary"
            >
              {suggestion}
            </button>
          ))}
        </div>
      )}
      <button
        type="button"
        onClick={onAdjust}
        className="rounded-lg bg-primary-container px-lg py-3 text-title-md text-on-primary-container transition-transform hover:-translate-y-0.5"
      >
        Adjust filters
      </button>
    </div>
  );
}
