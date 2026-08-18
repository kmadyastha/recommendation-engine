"use client";

import { useEffect, useMemo, useRef, useState } from "react";

interface CityComboboxProps {
  cities: string[];
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function CityCombobox({ cities, value, onChange, disabled }: CityComboboxProps) {
  const [query, setQuery] = useState(value);
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setQuery(value);
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
    const q = query.trim().toLowerCase();
    if (!q) return cities.slice(0, 50);
    return cities.filter((city) => city.toLowerCase().includes(q)).slice(0, 50);
  }, [cities, query]);

  return (
    <div ref={containerRef} className="relative">
      <span className="material-symbols-outlined absolute left-sm top-1/2 -translate-y-1/2 text-outline-variant">
        location_on
      </span>
      <input
        type="text"
        value={query}
        disabled={disabled}
        placeholder="Search city"
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
          {filtered.length === 0 ? (
            <li className="px-sm py-2 text-body-sm text-on-surface-variant">No cities found</li>
          ) : (
            filtered.map((city) => (
              <li key={city}>
                <button
                  type="button"
                  className="w-full px-sm py-2 text-left text-body-sm text-on-surface transition-colors hover:bg-surface-container-high"
                  onMouseDown={(e) => {
                    e.preventDefault();
                    onChange(city);
                    setQuery(city);
                    setOpen(false);
                  }}
                >
                  {city}
                </button>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}
