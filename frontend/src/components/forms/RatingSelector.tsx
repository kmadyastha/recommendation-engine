"use client";

interface RatingSelectorProps {
  value: number;
  onChange: (value: number) => void;
  disabled?: boolean;
}

export function RatingSelector({ value, onChange, disabled }: RatingSelectorProps) {
  const steps = [0, 1, 2, 3, 4, 5];

  return (
    <div className="flex h-10 items-center gap-base">
      {steps.slice(1).map((star) => (
        <button
          key={star}
          type="button"
          disabled={disabled}
          aria-label={`Minimum ${star} stars`}
          onClick={() => onChange(star === value ? star - 1 : star)}
          className="transition-colors disabled:opacity-50"
        >
          <span
            className={`material-symbols-outlined ${
              star <= value ? "text-secondary" : "text-surface-variant hover:text-secondary-fixed"
            }`}
            style={{ fontVariationSettings: star <= value ? "'FILL' 1" : "'FILL' 0" }}
          >
            star
          </span>
        </button>
      ))}
      <span className="ml-sm font-rating-number text-rating-number text-on-surface">
        {value > 0 ? `${value.toFixed(1)}+` : "Any rating"}
      </span>
    </div>
  );
}
