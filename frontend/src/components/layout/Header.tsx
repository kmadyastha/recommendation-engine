"use client";

import { useState } from "react";
import { StatusModal } from "@/components/ui/StatusModal";

interface HeaderProps {
  onEditSearch?: () => void;
  showEdit?: boolean;
}

export function Header({ onEditSearch, showEdit }: HeaderProps) {
  const [statusOpen, setStatusOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 z-50 flex h-20 w-full items-center justify-between border-b border-outline-variant/10 bg-surface/70 px-margin-mobile shadow-sm backdrop-blur-md md:px-margin-desktop">
        <div className="flex items-center gap-sm">
          <span className="text-display-lg-mobile font-extrabold tracking-tight text-primary-container md:text-display-lg">
            BiteWise
          </span>
        </div>

        <div className="flex items-center gap-md">
          {showEdit && onEditSearch && (
            <button
              type="button"
              onClick={onEditSearch}
              className="hidden items-center gap-1 rounded-lg border border-outline-variant/30 px-3 py-2 text-body-sm text-on-surface-variant transition-colors hover:border-primary hover:text-primary md:flex"
            >
              <span className="material-symbols-outlined text-[18px]">edit</span>
              Edit search
            </button>
          )}
          <button
            type="button"
            aria-label="API status"
            onClick={() => setStatusOpen(true)}
            className="text-on-surface-variant transition-colors hover:text-primary"
          >
            <span className="material-symbols-outlined">dns</span>
          </button>
          <div className="flex h-10 w-10 items-center justify-center rounded-full border border-outline-variant bg-surface-container">
            <span className="material-symbols-outlined text-primary">person</span>
          </div>
        </div>
      </nav>
      <StatusModal open={statusOpen} onClose={() => setStatusOpen(false)} />
    </>
  );
}
