"use client";

import Image from "next/image";
import type { RecommendationItem } from "@/lib/types";
import {
  formatCost,
  formatRating,
  getRestaurantImage,
  splitCuisineTags,
} from "@/lib/placeholders";

interface RecommendationCardProps {
  item: RecommendationItem;
}

export function RecommendationCard({ item }: RecommendationCardProps) {
  const isTop = item.rank === 1;
  const isSecond = item.rank === 2;
  const isThird = item.rank === 3;
  const imageUrl = getRestaurantImage(item.restaurant_name);
  const tags = splitCuisineTags(item.cuisine);
  const hasRating = item.rating !== null && !Number.isNaN(item.rating);

  const borderClass = isTop
    ? "border-secondary/50 shadow-[0_0_15px_rgba(255,198,64,0.15)]"
    : isSecond
      ? "border-gray-400/40"
      : isThird
        ? "border-amber-700/40"
        : "border-surface-container-high";

  return (
    <article
      className={`relative overflow-hidden rounded-xl border bg-[#1A1A1F] transition-transform duration-300 hover:-translate-y-1 ${borderClass}`}
    >
      {isTop && (
        <div className="absolute left-sm top-sm z-10 flex items-center gap-xs rounded-full bg-secondary px-sm py-xs text-label-caps uppercase tracking-wider text-on-secondary shadow-md">
          <span
            className="material-symbols-outlined text-[14px]"
            style={{ fontVariationSettings: "'FILL' 1" }}
          >
            star
          </span>
          Top match
        </div>
      )}

      {!isTop && item.rank <= 3 && (
        <div className="absolute left-sm top-sm z-10 rounded-full bg-surface-container px-sm py-xs text-label-caps uppercase tracking-wider text-on-surface-variant">
          #{item.rank}
        </div>
      )}

      <div className="flex flex-col md:flex-row">
        <div className="relative h-48 w-full md:h-auto md:min-h-[220px] md:w-2/5">
          <Image
            src={imageUrl}
            alt={`${item.restaurant_name} placeholder`}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 100vw, 40vw"
          />
        </div>

        <div className="flex w-full flex-col p-sm md:w-3/5">
          <div className="flex items-start justify-between gap-sm">
            <div>
              <div className="mb-xs flex flex-wrap gap-xs">
                {tags.map((tag) => (
                  <span
                    key={tag}
                    className="rounded bg-surface-container px-xs py-base text-label-caps uppercase tracking-wider text-on-surface-variant"
                  >
                    {tag}
                  </span>
                ))}
              </div>
              <h3 className="text-title-md text-on-surface">{item.restaurant_name}</h3>
              <p className="mt-base flex items-center gap-xs text-body-sm text-on-surface-variant">
                <span className="material-symbols-outlined text-[14px]">location_on</span>
                {item.location}
              </p>
            </div>

            <div className="flex shrink-0 flex-col items-end">
              {hasRating ? (
                <div className="flex items-center gap-xs rounded bg-secondary px-xs py-base text-on-secondary">
                  <span className="font-rating-number text-rating-number">
                    {formatRating(item.rating)}
                  </span>
                  <span
                    className="material-symbols-outlined text-[14px]"
                    style={{ fontVariationSettings: "'FILL' 1" }}
                  >
                    star
                  </span>
                </div>
              ) : (
                <span className="rounded bg-surface-container px-xs py-base text-body-sm text-on-surface-variant">
                  No rating
                </span>
              )}
              <span className="mt-xs text-label-caps uppercase tracking-wider text-on-surface-variant">
                {formatCost(item.cost_for_two)}
              </span>
            </div>
          </div>

          <div className="mt-auto pt-sm">
            <div className="flex gap-xs rounded-lg border border-surface-container-high bg-surface-container-low p-sm">
              <span className="material-symbols-outlined mt-1 shrink-0 text-[18px] text-tertiary-container">
                auto_awesome
              </span>
              <div>
                <span className="mb-base block text-label-caps uppercase tracking-wider text-on-surface-variant">
                  Why recommended
                </span>
                <p className="text-body-sm text-on-surface">{item.why_recommended}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </article>
  );
}
