interface AISummaryProps {
  summary: string | null;
  fallbackTitle?: string;
}

export function AISummary({ summary, fallbackTitle }: AISummaryProps) {
  return (
    <div className="ai-gradient-bg ai-gradient-border flex items-start gap-sm rounded-xl p-sm">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-surface-container">
        <span
          className="material-symbols-outlined ai-gradient-text"
          style={{ fontVariationSettings: "'FILL' 1" }}
        >
          auto_awesome
        </span>
      </div>
      <div>
        <h1 className="mb-xs text-title-md text-on-surface">
          {fallbackTitle || "I've found the perfect spots for you."}
        </h1>
        {summary && (
          <p className="text-body-lg text-on-surface-variant">{summary}</p>
        )}
      </div>
    </div>
  );
}
