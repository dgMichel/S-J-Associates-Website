-- Run this in Supabase SQL editor (https://app.supabase.com/project/_/sql)
-- Idempotent: safe to run multiple times.

create table if not exists public.unavailable_dates (
  id bigserial primary key,
  car_slug text not null,
  date date not null,
  reason text,
  created_at timestamp with time zone not null default now(),
  unique (car_slug, date)
);

create index if not exists idx_unavailable_car_slug on public.unavailable_dates(car_slug);
create index if not exists idx_unavailable_date on public.unavailable_dates(date);

alter table public.unavailable_dates enable row level security;

drop policy if exists "Anyone can read unavailable_dates" on public.unavailable_dates;
create policy "Anyone can read unavailable_dates"
  on public.unavailable_dates
  for select
  using (true);

-- Writes go through the backend using the service_role key, which bypasses RLS,
-- so no additional write policies are needed.
