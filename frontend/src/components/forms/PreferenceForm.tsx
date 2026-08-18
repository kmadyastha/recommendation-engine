"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";
import type { PreferenceFormValues } from "@/lib/types";
import { DEFAULT_FORM_VALUES } from "@/lib/types";
import { BudgetPills } from "./BudgetPills";
import { CityCombobox } from "./CityCombobox";
import { CuisineCombobox } from "./CuisineCombobox";
import { RatingSelector } from "./RatingSelector";

const schema = z.object({
  location: z.string().min(1, "Location is required"),
  budget: z.enum(["low", "medium", "high"]),
  cuisine: z.string(),
  min_rating: z.number().min(0).max(5),
  additional_preferences: z.string(),
  limit: z.number().min(1).max(50),
});

interface PreferenceFormProps {
  cities: string[];
  cuisines: string[];
  defaultValues?: Partial<PreferenceFormValues>;
  onSubmit: (values: PreferenceFormValues) => void;
  disabled?: boolean;
}

export function PreferenceForm({
  cities,
  cuisines,
  defaultValues,
  onSubmit,
  disabled,
}: PreferenceFormProps) {
  const {
    register,
    handleSubmit,
    watch,
    setValue,
    reset,
    formState: { errors },
  } = useForm<PreferenceFormValues>({
    resolver: zodResolver(schema),
    defaultValues: { ...DEFAULT_FORM_VALUES, ...defaultValues },
  });

  const budget = watch("budget");
  const minRating = watch("min_rating");
  const limit = watch("limit");
  const location = watch("location");
  const cuisine = watch("cuisine");

  return (
    <div className="glass-panel relative w-full max-w-4xl overflow-hidden rounded-xl p-md shadow-2xl md:p-lg">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent" />
      <form
        className="relative z-10 flex flex-col gap-lg"
        onSubmit={handleSubmit(onSubmit)}
      >
        <div className="grid grid-cols-1 gap-md md:grid-cols-2">
          <div className="flex flex-col gap-xs">
            <label className="pl-base text-label-caps uppercase tracking-wider text-on-surface-variant">
              Location
            </label>
            <CityCombobox
              cities={cities}
              value={location}
              onChange={(v) => setValue("location", v, { shouldValidate: true })}
              disabled={disabled}
            />
            {errors.location && (
              <p className="text-body-sm text-error">{errors.location.message}</p>
            )}
          </div>

          <div className="flex flex-col gap-xs">
            <label className="pl-base text-label-caps uppercase tracking-wider text-on-surface-variant">
              Cuisine
            </label>
            <CuisineCombobox
              cuisines={cuisines}
              value={cuisine}
              onChange={(v) => setValue("cuisine", v)}
              disabled={disabled}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 items-end gap-md md:grid-cols-3">
          <div className="flex flex-col gap-xs">
            <label className="pl-base text-label-caps uppercase tracking-wider text-on-surface-variant">
              Budget
            </label>
            <BudgetPills
              value={budget}
              onChange={(v) => setValue("budget", v)}
              disabled={disabled}
            />
          </div>

          <div className="flex flex-col gap-xs md:col-span-2">
            <label className="flex items-center gap-xs pl-base text-label-caps uppercase tracking-wider text-on-surface-variant">
              Specific vibe or craving
              <span
                className="material-symbols-outlined text-[14px] text-tertiary-container"
                style={{ fontVariationSettings: "'FILL' 1" }}
              >
                auto_awesome
              </span>
            </label>
            <textarea
              {...register("additional_preferences")}
              disabled={disabled}
              placeholder="e.g. family-friendly, quick delivery, romantic, vegan..."
              className="input-inset h-[50px] w-full resize-none rounded-lg border border-outline-variant bg-surface-container-lowest px-sm py-3 text-body-lg leading-normal text-on-surface outline-none transition-all placeholder:text-outline-variant/50 focus:border-primary focus:ring-1 focus:ring-primary disabled:opacity-50"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 gap-md border-t border-outline-variant/20 pt-sm md:grid-cols-2">
          <div className="flex flex-col gap-xs">
            <label className="pl-base text-label-caps uppercase tracking-wider text-on-surface-variant">
              Minimum rating
            </label>
            <RatingSelector
              value={minRating}
              onChange={(v) => setValue("min_rating", v)}
              disabled={disabled}
            />
          </div>

          <div className="flex flex-col gap-xs md:items-end">
            <label className="pl-base text-label-caps uppercase tracking-wider text-on-surface-variant md:pr-base">
              Options to generate
            </label>
            <div className="input-inset flex h-10 w-32 items-center justify-between rounded-lg border border-outline-variant bg-surface-container-lowest px-sm">
              <button
                type="button"
                disabled={disabled || limit <= 1}
                onClick={() => setValue("limit", Math.max(1, limit - 1))}
                className="flex items-center justify-center text-on-surface-variant transition-colors hover:text-primary disabled:opacity-40"
              >
                <span className="material-symbols-outlined text-[20px]">remove</span>
              </button>
              <span className="text-title-md text-on-surface">{limit}</span>
              <button
                type="button"
                disabled={disabled || limit >= 50}
                onClick={() => setValue("limit", Math.min(50, limit + 1))}
                className="flex items-center justify-center text-on-surface-variant transition-colors hover:text-primary disabled:opacity-40"
              >
                <span className="material-symbols-outlined text-[20px]">add</span>
              </button>
            </div>
          </div>
        </div>

        <div className="mt-sm flex flex-col gap-sm pt-md md:flex-row-reverse">
          <button
            type="submit"
            disabled={disabled}
            className="group relative flex flex-1 items-center justify-center gap-sm overflow-hidden rounded-lg bg-primary-container px-xl py-3 text-title-md text-on-primary-container transition-all duration-300 hover:-translate-y-1 ai-glow disabled:translate-y-0 disabled:opacity-50 md:flex-none"
          >
            <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
            <span className="relative z-10">Get Recommendations</span>
            <span
              className="material-symbols-outlined relative z-10"
              style={{ fontVariationSettings: "'FILL' 1" }}
            >
              auto_awesome
            </span>
          </button>
          <button
            type="button"
            disabled={disabled}
            onClick={() => reset(DEFAULT_FORM_VALUES)}
            className="flex flex-1 items-center justify-center rounded-lg border border-outline-variant bg-transparent px-xl py-3 text-title-md text-on-surface-variant transition-colors duration-200 hover:bg-surface-container hover:text-on-surface disabled:opacity-50 md:flex-none"
          >
            Reset filters
          </button>
        </div>
      </form>
    </div>
  );
}
