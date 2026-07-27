export interface Car {
  slug: string;
  color: string;
  model: string;
  brand: string;
  year: number;
  plate: string;
  pricePerDay: number;
  available: boolean;
  description: string;
  features: Array<string>;
  specs: { engine: string, transmission: string, fuel: string, seats: number, doors: number };
  photos: { front: string, side: string, main: string, back: string };
  bookedDates: Array<{ start: string, end: string }>;
}

export const cars: Array<Car> = [
  {

    slug: 'suzuki-ignis-red-py-807',
    brand: 'Suzuki',
    model: 'Ignis',
    year: 2016,
    color: 'Red',
    plate: 'PY 807',
    available: true,
    pricePerDay: 150,
    photos: {
      front: '/red_suzuki_ignis_defrente.webp',
      side: '/red_suzuki_ignis_delado.webp',
      main: "/rojo.webp",
      back: '/red_suzuki_ignis_detras.webp',
    },
    description:
      'Vibrant Red Suzuki Ignis 2016. A stylish and reliable compact car, ideal for navigating the city with ease.',
    specs: {
      engine: '1.2L 4-cylinder',
      transmission: 'Manual',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [
      { start: '2026-07-05', end: '2026-07-08' },
      { start: '2026-07-15', end: '2026-07-20' },
    ],
  },
  {
    slug: 'suzuki-ignis-gold-paq-852',
    brand: 'Suzuki',
    model: 'Ignis',
    year: 2016,
    color: 'Gold',
    plate: 'PAQ 852',
    available: true,
    pricePerDay: 150,
    photos: {
      front: '/gold_suzuki_defrente.webp',
      side: '/gold_suzuki_delado.webp',
      main: "/oro2.webp",
      back: '/gold_suzuki_detras.webp',
    },
    description:
      'Well-maintained Suzuki Ignis 2016 in elegant Gold. Perfect for city driving with great fuel economy and compact design.',
    specs: {
      engine: '1.2L 4-cylinder',
      transmission: 'Manual',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [
      { start: '2026-07-10', end: '2026-07-13' },
    ],
  },

  {
    slug: 'suzuki-ignis-white-paq-855',
    brand: 'Suzuki',
    model: 'Ignis',
    year: 2016,
    color: 'White',
    plate: 'PAQ 855',
    available: true,
    pricePerDay: 150,
    photos: {
      front: '/white_suziki_ignis_defrente.webp',
      side: '/white_suziki_ignis_delado.webp',
      main: '/blanco.webp',
      back: '/white_suziki_ignis_detras.webp',
    },
    description:
      'Crisp White Suzuki Ignis 2016. Clean, practical, and efficient — the ideal daily driver for any journey.',
    specs: {
      engine: '1.2L 4-cylinder',
      transmission: 'Manual',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [
      { start: '2026-07-22', end: '2026-07-28' },
    ],
  },
  {
    slug: 'suzuki-ignis-gold-paq-853',
    brand: 'Suzuki',
    model: 'Ignis',
    year: 2016,
    color: 'Gold',
    plate: 'PAQ 853',
    available: true,
    pricePerDay: 150,
    photos: {
      front: '/gold_suzuki_defrente.webp',
      side: '/gold_suzuki_delado.webp',
      main: "/oro.webp",
      back: '/gold_suzuki_detras.webp',
    },
    description:
      'Another elegant Gold Suzuki Ignis 2016. Reliable, fuel-efficient, and ready to take you wherever you need to go.',
    specs: {
      engine: '1.2L 4-cylinder',
      transmission: 'Manual',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [
      { start: '2026-07-02', end: '2026-07-04' },
      { start: '2026-07-25', end: '2026-07-27' },
    ],
  },
  {
    slug: 'suzuki-ignis-turquoise-py-808',
    brand: 'Suzuki',
    model: 'Ignis',
    year: 2016,
    color: 'Turquoise',
    plate: 'PY 808',
    available: true,
    pricePerDay: 150,
    photos: {
      front: '/turquoise_suzuki_iggnis_defrente.webp',
      side: '/turquoise_suzuki_iggnis_delado.webp',
      main: '/Azul.webp',
      back: '/turquoise_suzuki_iggnis_detras.webp',
    },
    description:
      'Eye-catching Turquoise Suzuki Ignis 2016. Stand out on the road with this unique color while enjoying reliable performance.',
    specs: {
      engine: '1.2L 4-cylinder',
      transmission: 'Manual',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [],
  },
  {
    slug: 'nissan-cube-brown-pr-945',
    brand: 'Nissan',
    model: 'Cube',
    year: 2016,
    color: 'Brown',
    plate: 'PR 945',
    available: true,
    pricePerDay: 160,
    photos: {
      front: '/nissan_cube_z12_defrente.webp',
      side: '/nissan_cube_z12_delado.webp',
      main: "/cubo.webp",
      back: '/nissan_cube_z12_detras.webp',
    },
    description:
      'Spacious and quirky Nissan Cube in Brown. Currently on long-term rental — check back soon for availability.',
    specs: {
      engine: '1.5L 4-cylinder',
      transmission: 'Automatic',
      fuel: 'Gasoline',
      seats: 5,
      doors: 5,
    },
    features: ['Air Conditioning', 'Power Steering', 'Bluetooth', 'CD Radio', 'ABS Brakes'],
    bookedDates: [
      { start: '2026-07-01', end: '2026-07-15' },
    ],
  },

]

export function getCarBySlug(slug: string) {
  return cars.find((car) => car.slug === slug)
}

export function getCarsByBrand(brand: string) {
  return cars.filter((car) => car.brand === brand)
}

export const brands = [...new Set(cars.map((car) => car.brand))]

export function isDateBooked(car: Car, date: Date): boolean {
  const d = date.toISOString().slice(0, 10)
  return car.bookedDates.some((b) => d >= b.start && d <= b.end)
}

export function isRangeAvailable(car: Car, start: Date, days: number): boolean {
  for (let i = 0; i < days; i++) {
    const d = new Date(start)
    d.setDate(d.getDate() + i)
    if (isDateBooked(car, d)) return false
  }
  return true
}
