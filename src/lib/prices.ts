export type PriceOverrides = Record<string, number>;

const KEY = "car_price_overrides";

export function getPriceOverrides(): PriceOverrides {
  if (typeof window === "undefined") return {};
  try {
    return JSON.parse(localStorage.getItem(KEY) || "{}") as PriceOverrides;
  } catch {
    return {};
  }
}

export function getOverridePrice(slug: string, fallback: number): number {
  const overrides = getPriceOverrides();
  const value = overrides[slug];
  return typeof value === "number" && !Number.isNaN(value) ? value : fallback;
}

export function setPriceOverride(slug: string, price: number): void {
  const overrides = getPriceOverrides();
  overrides[slug] = price;
  localStorage.setItem(KEY, JSON.stringify(overrides));
}

export function applyPriceOverrides(): void {
  if (typeof window === "undefined") return;
  document.querySelectorAll<HTMLElement>("[data-price-slug]").forEach((el) => {
    const slug = el.dataset.priceSlug!;
    const basePrice = parseFloat(el.dataset.basePrice || "0");
    const finalPrice = getOverridePrice(slug, basePrice);
    el.textContent = `EC$${finalPrice}`;
    el.dataset.price = String(finalPrice);
  });
}

export function dispatchPricesChanged(): void {
  window.dispatchEvent(new CustomEvent("prices:changed"));
}
