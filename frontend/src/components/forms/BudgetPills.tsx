"use client";

import type { BudgetTier } from "@/lib/types";

const OPTIONS: { value: BudgetTier; label: string }[] = [
  { value: "low", label: "Low" },
  { value: "medium", label: "Medium" },
  { value: "high", label: "High" },
];

interface BudgetPillsProps {
  value: BudgetTier;
  onChange: (value: BudgetTier) => void;
  disabled?: boolean;
}

export function BudgetPills({ value, onChange, disabled }: BudgetPillsProps) {
  return (
    <div className="input-inset flex h-[50px] rounded-lg border border-outline-variant bg-surface-container-lowest p-1">
      {OPTIONS.map((option) => {
        const active = value === option.value;
        return (
          <button
            key={option.value}
            type="button"
            disabled={disabled}
            onClick={() => onChange(option.value)}
            className={`flex-1 rounded-md text-body-sm transition-colors duration-200 disabled:opacity-50 ${
              active
                ? "border border-outline-variant/30 bg-surface-variant font-bold text-on-surface shadow-sm"
                : "text-on-surface-variant hover:text-on-surface"
            }`}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
