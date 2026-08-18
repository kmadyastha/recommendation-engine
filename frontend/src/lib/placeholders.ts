/** Generic food/restaurant placeholder images (Unsplash). Assigned deterministically per restaurant name. */
export const RESTAURANT_PLACEHOLDER_IMAGES = [
  "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80",
  "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80",
  "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80",
  "https://images.unsplash.com/photo-1559339352-11d035aa65de?w=800&q=80",
  "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&q=80",
  "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&q=80",
  "https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=800&q=80",
  "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=800&q=80",
  "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800&q=80",
  "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80",
];

export function getRestaurantImage(restaurantName: string): string {
  let hash = 0;
  for (let i = 0; i < restaurantName.length; i += 1) {
    hash = (hash * 31 + restaurantName.charCodeAt(i)) >>> 0;
  }
  return RESTAURANT_PLACEHOLDER_IMAGES[hash % RESTAURANT_PLACEHOLDER_IMAGES.length];
}

export function formatRating(rating: number | null): string {
  if (rating === null || Number.isNaN(rating)) {
    return "No rating";
  }
  return rating.toFixed(1);
}

export function formatCost(cost: number | null): string {
  if (cost === null || Number.isNaN(cost)) {
    return "Price N/A";
  }
  return `₹${Math.round(cost)} for two`;
}

export function splitCuisineTags(cuisine: string): string[] {
  return cuisine
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean)
    .slice(0, 3);
}
