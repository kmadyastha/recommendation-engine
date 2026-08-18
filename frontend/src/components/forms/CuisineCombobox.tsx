"use client";

import { useEffect, useMemo, useRef, useState } from "react";

interface CuisineComboboxProps {
  cuisines: string[];
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function CuisineCombobox({
  cuisines,
  value,
  onChange,
  disabled,
}: CuisineComboboxProps) {
  const [query, setQuery] = useState(value || "Any cuisine");
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setQuery(value || "Any cuisine");
  }, [value]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const filtered = useMemo(() => {
    const q = query === "Any cuisine" ? "" : query.trim().toLowerCase();
    if (!q) return cuisines.slice(0, 50);
    return cuisines.filter((c) => c.toLowerCase().includes(q)).slice(0, 50);
  }, [cuisines, query]);

  return (
    <div ref={containerRef} className="relative">
      <span className="material-symbols-outlined absolute left-sm top-1/2 -translate-y-1/2 text-outline-variant">
        ramen_dining
      </span>
      <input
        type="text"
        value={query}
        disabled={disabled}
        placeholder="Any cuisine"
        autoComplete="off"
        className="input-inset w-full rounded-lg border border-outline-variant bg-surface-container-lowest py-3 pl-12 pr-10 text-body-lg text-on-surface outline-none transition-all placeholder:text-outline-variant focus:border-primary focus:ring-1 focus:ring-primary disabled:opacity-50"
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
      />
      <span className="material-symbols-outlined pointer-events-none absolute right-sm top-1/2 -translate-y-1/2 text-outline-variant">
        arrow_drop_down
      </span>

      {open && !disabled && (
        <ul className="absolute z-20 mt-1 max-h-60 w-full overflow-auto rounded-lg border border-outline-variant bg-surface-container-low shadow-xl no-scrollbar">
          <li>
            <button
              type="button"
              className="w-full px-sm py-2 text-left text-body-sm text-on-surface-variant transition-colors hover:bg-surface-container-high"
              onMouseDown={(e) => {
                e.preventDefault();
                onChange("");
                setQuery("Any cuisine");
                setOpen(false);
              }}
            >
              Any cuisine
            </button>
          </li>
          {filtered.map((cuisine) => (
            <li key={cuisine}>
              <button
                type="button"
                className="w-full px-sm py-2 text-left text-body-sm text-on-surface transition-colors hover:bg-surface-container-high"
                onMouseDown={(e) => {
                  e.preventDefault();
                  onChange(cuisine);
                  setQuery(cuisine);
                  setOpen(false);
                }}
              >
                {cuisine}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
