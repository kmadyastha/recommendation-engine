"use client";

interface HeroProps {
  restaurantCount?: number;
  cityCount?: number;
}

export function Hero({ restaurantCount, cityCount }: HeroProps) {
  const restaurants =
    restaurantCount !== undefined
      ? `${Math.floor(restaurantCount / 1000)}K+ Restaurants`
      : "53K+ Restaurants";
  const cities =
    cityCount !== undefined ? `${cityCount} Cities` : "531 Cities";

  return (
    <header className="mx-auto mb-xl w-full max-w-3xl text-center">
      <h1 className="mb-sm text-display-lg-mobile font-extrabold text-on-surface md:text-display-lg">
        AI picks the{" "}
        <span className="bg-gradient-to-r from-orange-500 to-purple-500 bg-clip-text text-transparent">perfect meal</span> for you.
      </h1>
      <div className="mt-md flex flex-wrap items-center justify-center gap-x-md gap-y-sm text-label-caps uppercase tracking-wider text-on-surface-variant">
        <div className="flex items-center gap-base">
          <span className="material-symbols-outlined text-[16px]">restaurant</span>
          <span>{restaurants}</span>
        </div>
        <span className="h-1 w-1 rounded-full bg-outline-variant" />
        <div className="flex items-center gap-base">
          <span className="material-symbols-outlined text-[16px]">location_city</span>
          <span>{cities}</span>
        </div>
        <span className="h-1 w-1 rounded-full bg-outline-variant" />
        <div className="flex items-center gap-base text-primary">
          <span className="material-symbols-outlined text-[16px]">auto_awesome</span>
          <span>Powered by AI</span>
        </div>
      </div>
    </header>
  );
}