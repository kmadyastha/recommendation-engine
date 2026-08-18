interface ErrorStateProps {
  message: string;
  onRetry: () => void;
  onBack: () => void;
}

export function ErrorState({ message, onRetry, onBack }: ErrorStateProps) {
  return (
    <div className="flex w-full max-w-2xl flex-col items-center rounded-xl border border-error-container/50 bg-surface-container-low p-xl text-center">
      <div className="mb-md flex h-16 w-16 items-center justify-center rounded-full bg-error-container/20">
        <span className="material-symbols-outlined text-[32px] text-error">error</span>
      </div>
      <h2 className="mb-sm text-title-md text-on-surface">Something went wrong</h2>
      <p className="mb-md text-body-lg text-on-surface-variant">{message}</p>
      <div className="flex flex-col gap-sm sm:flex-row">
        <button
          type="button"
          onClick={onRetry}
          className="rounded-lg bg-primary-container px-lg py-3 text-title-md text-on-primary-container"
        >
          Try again
        </button>
        <button
          type="button"
          onClick={onBack}
          className="rounded-lg border border-outline-variant px-lg py-3 text-title-md text-on-surface-variant hover:text-on-surface"
        >
          Back to search
        </button>
      </div>
    </div>
  );
}
