export const SITE = {
  name: "5J & Associates",
  shortName: "5J Rentals",
  tagline: "Premium Car Rental in Grenada",
  description:
    "Reliable and affordable car rental in Grenada. Rent a Suzuki Ignis or Nissan Cube from EC$150 per day. Transparent pricing, no hidden fees, free WhatsApp booking. Open 24/7.",
  url: import.meta.env.PUBLIC_SITE_URL || "https://www.5j-associates.com",
  locale: "en_GD",
  language: "en",
  defaultOgImage: "/og-image.svg",
  email: import.meta.env.EMAIL || "fivejandassociates@gmail.com",
  phone: import.meta.env.PHONE || "+1 (473) 403-6877",
  whatsapp: "https://wa.me/14734046549",
  mapsUrl: "https://maps.me/link/ge0/8kxIMHp80t/Lugar_desconocido",
  address: {
    streetAddress: "St. George's",
    addressLocality: "St. George's",
    addressRegion: "St. George",
    postalCode: "00000",
    addressCountry: "GD",
  },
  geo: {
    latitude: 12.0561,
    longitude: -61.7488,
  },
  openingHours: [
    {
      days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
      opens: "00:00",
      closes: "23:59",
    },
  ],
  social: {
    whatsapp: "https://wa.me/14734046549",
    facebook: "https://www.facebook.com/5JAssociates",
    instagram: "https://www.instagram.com/5jassociates",
  },
  keywords: [
    "car rental Grenada",
    "rent a car Grenada",
    "Grenada car hire",
    "car rental St George's Grenada",
    "Suzuki Ignis rental Grenada",
    "Nissan Cube rental Grenada",
    "cheap car rental Grenada",
    "Caribbean car rental",
    "Grenada airport car rental",
    "Maurice Bishop airport car rental",
    "self drive Grenada",
    "Grenada road trip",
    "Grenada vacation car",
    "Caribbean island car hire",
    "rent car Grenada EC$",
    "24 hour car rental Grenada",
    "car rental near me Grenada",
  ],
  naicsCode: "532111",
  foundingYear: "2018",
};

export const NAV = [
  { label: "Home", href: "/" },
  { label: "Suzuki Ignis", href: "/#suzuki" },
  { label: "Nissan Cube", href: "/#nissan" },
  { label: "Contact", href: "/#contact" },
];

export function absoluteUrl(path: string): string {
  if (path.startsWith("http")) return path;
  const base = SITE.url.replace(/\/$/, "");
  return `${base}${path.startsWith("/") ? path : `/${path}`}`;
}