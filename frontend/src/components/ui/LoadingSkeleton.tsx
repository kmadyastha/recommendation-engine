export function LoadingSkeleton() {
  return (
    <div className="flex w-full max-w-4xl flex-col gap-md">
      <div className="rounded-xl border border-outline-variant/20 bg-surface-container-low p-md">
        <div className="mb-4 flex items-center gap-sm">
          <div className="skeleton-shimmer h-10 w-10 rounded-full" />
          <div className="flex-1 space-y-2">
            <div className="skeleton-shimmer h-5 w-2/3 rounded" />
            <div className="skeleton-shimmer h-4 w-full rounded" />
          </div>
        </div>
        <p className="text-center text-body-sm text-on-surface-variant">
          Finding the best spots for you…
        </p>
        <p className="mt-1 text-center text-body-sm text-outline">
          Our AI is ranking restaurants based on your preferences
        </p>
      </div>

      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="overflow-hidden rounded-xl border border-outline-variant/20 bg-[#1A1A1F]"
        >
          <div className="flex flex-col md:flex-row">
            <div className="skeleton-shimmer h-48 w-full md:h-auto md:w-2/5" />
            <div className="flex flex-1 flex-col gap-sm p-sm">
              <div className="skeleton-shimmer h-4 w-24 rounded" />
              <div className="skeleton-shimmer h-6 w-3/4 rounded" />
              <div className="skeleton-shimmer h-4 w-1/2 rounded" />
              <div className="mt-auto skeleton-shimmer h-20 w-full rounded-lg" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
