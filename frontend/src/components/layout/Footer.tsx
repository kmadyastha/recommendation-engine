"use client";

interface FooterProps {
  onStatusClick?: () => void;
}

export function Footer({ onStatusClick }: FooterProps) {
  return (
    <footer className="z-10 mt-auto w-full border-t border-outline-variant/20 bg-surface-container-lowest py-xl">
      <div className="flex flex-col items-center justify-between gap-md px-margin-mobile md:flex-row md:px-margin-desktop">
        <span className="text-label-caps uppercase tracking-wider text-on-surface">
          © {new Date().getFullYear()} BiteWise AI
        </span>
        <div className="flex flex-wrap justify-center gap-md text-body-sm text-secondary">
          <button
            type="button"
            onClick={onStatusClick}
            className="transition-colors hover:text-secondary-container"
          >
            API Status
          </button>
          <span className="text-on-surface-variant">All systems operational</span>
        </div>
      </div>
    </footer>
  );
}
