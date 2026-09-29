-- =====================================================
-- 5J & Associates - Payments & Bookings Schema
-- Run this in Supabase SQL Editor (Database > SQL Editor)
-- =====================================================

-- =====================================================
-- Table: bookings
-- Cada reserva tentativa del cliente
-- =====================================================
create table if not exists bookings (
    id              bigserial primary key,
    reference_code  text unique not null,                          -- ej: 5J-A7K9X3 (mostrado al cliente)
    user_id         uuid references auth.users(id) on delete set null,
    car_slug        text not null,
    start_date      date not null,
    end_date        date not null,
    days            int  not null check (days >= 1),
    customer_name   text not null,
    customer_email  text not null,
    customer_phone  text,
    customer_country text,                                          -- 'GD' para nacionales
    nationality     text not null check (nationality in ('national','foreign')),
    currency        text not null check (currency in ('XCD','USD')),
    subtotal        numeric(10,2) not null,                         -- rental × days
    deposit         numeric(10,2) not null,                         -- refundable deposit
    total           numeric(10,2) not null,                         -- subtotal + deposit
    status          text not null default 'pending_payment'
                      check (status in ('pending_payment','awaiting_transfer_approval',
                                        'paid','cancelled','rejected','refunded')),
    payment_method  text not null check (payment_method in ('paypal','bank_transfer')),
    notes           text,
    created_at      timestamptz not null default now(),
    updated_at      timestamptz not null default now(),
    confirmed_at    timestamptz,
    constraint bookings_dates_check check (end_date >= start_date)
);

create index if not exists idx_bookings_reference on bookings(reference_code);
create index if not exists idx_bookings_user on bookings(user_id);
create index if not exists idx_bookings_status on bookings(status);
create index if not exists idx_bookings_car_dates on bookings(car_slug, start_date, end_date);

-- =====================================================
-- Table: payments
-- Transacciones de PayPal (orders + captures)
-- =====================================================
create table if not exists payments (
    id                  bigserial primary key,
    booking_id          bigint not null references bookings(id) on delete cascade,
    provider            text not null default 'paypal'
                          check (provider in ('paypal')),
    paypal_order_id     text unique,                                -- ID del order en PayPal
    paypal_capture_id   text,                                       -- ID del capture
    paypal_payer_id     text,
    paypal_payer_email  text,
    amount              numeric(10,2) not null,
    currency            text not null,
    status              text not null default 'created'
                          check (status in ('created','approved','captured','refunded','failed')),
    raw_response        jsonb,                                      -- respuesta cruda de PayPal (debug)
    created_at          timestamptz not null default now(),
    captured_at         timestamptz
);

create index if not exists idx_payments_booking on payments(booking_id);
create index if not exists idx_payments_paypal_order on payments(paypal_order_id);

-- =====================================================
-- Table: bank_transfers
-- Reservas pagadas por transferencia bancaria
-- =====================================================
create table if not exists bank_transfers (
    id                  bigserial primary key,
    booking_id          bigint not null unique references bookings(id) on delete cascade,
    bank_name           text not null,                              -- ej: Republic Bank (Grenada) Ltd
    account_name        text not null,                              -- titular de la cuenta
    account_number      text not null,                              -- último(4) visible al cliente
    swift_code          text,                                       -- para internacionales
    reference_code      text not null,                              -- lo que el cliente pone como memo
    proof_url           text,                                       -- URL del comprobante subido
    proof_uploaded_at   timestamptz,
    approved_by         uuid references auth.users(id),             -- admin que aprobó
    approved_at         timestamptz,
    rejection_reason    text,
    rejected_by         uuid references auth.users(id),
    rejected_at         timestamptz,
    created_at          timestamptz not null default now()
);

create index if not exists idx_bank_transfers_booking on bank_transfers(booking_id);
create index if not exists idx_bank_transfers_reference on bank_transfers(reference_code);

-- =====================================================
-- Table: bank_accounts
-- Cuentas bancarias de la empresa (para mostrar al cliente)
-- Una sola activa por moneda típicamente
-- =====================================================
create table if not exists bank_accounts (
    id              bigserial primary key,
    bank_name       text not null,
    account_name    text not null,                                  -- titular
    account_number  text not null,                                  -- número completo
    swift_code      text,
    currency        text not null check (currency in ('XCD','USD')),
    country         text not null,                                 -- 'GD', 'US', etc
    instructions    text,                                          -- texto extra para el cliente
    is_active       boolean not null default true,
    display_order   int not null default 0,
    created_at      timestamptz not null default now()
);

-- Datos de ejemplo - REEMPLAZAR con tus cuentas reales
insert into bank_accounts (bank_name, account_name, account_number, swift_code, currency, country, instructions, display_order)
values
  ('Republic Bank (Grenada) Ltd', '5J & Associates', '1234567890', 'REPBGDGD', 'XCD', 'GD',
   'Use your booking reference (e.g. 5J-A7K9X3) as the transfer memo.', 1),
  ('Republic Bank (Grenada) Ltd', '5J & Associates', '0987654321', 'REPBGDGD', 'USD', 'GD',
   'For international transfers. Use your booking reference as memo.', 2)
on conflict do nothing;

-- =====================================================
-- Modificar unavailable_dates para ligar a bookings
-- =====================================================
alter table unavailable_dates
    add column if not exists booking_id bigint references bookings(id) on delete set null,
    add column if not exists source text not null default 'admin'
      check (source in ('admin','booking'));

create index if not exists idx_unavailable_booking on unavailable_dates(booking_id);

-- =====================================================
-- Trigger: auto-update updated_at
-- =====================================================
create or replace function set_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_bookings_updated_at on bookings;
create trigger trg_bookings_updated_at
    before update on bookings
    for each row execute function set_updated_at();

-- =====================================================
-- RLS (Row Level Security) - Recomendado para Supabase
-- =====================================================

-- Bookings: solo el dueño (user_id) o admin puede verlas
alter table bookings enable row level security;

drop policy if exists "Users view own bookings" on bookings;
create policy "Users view own bookings" on bookings
    for select using (
        auth.uid() = user_id
        or (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

drop policy if exists "Anyone can create a booking" on bookings;
create policy "Anyone can create a booking" on bookings
    for insert with check (true);

drop policy if exists "Admins can update bookings" on bookings;
create policy "Admins can update bookings" on bookings
    for update using (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

-- Payments: solo admin o dueño de la reserva via join
alter table payments enable row level security;

drop policy if exists "Users view own payments" on payments;
create policy "Users view own payments" on payments
    for select using (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
        or exists (
            select 1 from bookings b
            where b.id = payments.booking_id and b.user_id = auth.uid()
        )
    );

-- Bank transfers: admin only
alter table bank_transfers enable row level security;

drop policy if exists "Admins view bank transfers" on bank_transfers;
create policy "Admins view bank transfers" on bank_transfers
    for select using (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

drop policy if exists "Admins update bank transfers" on bank_transfers;
create policy "Admins update bank transfers" on bank_transfers
    for update using (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

-- Bank accounts: lectura pública
alter table bank_accounts enable row level security;

drop policy if exists "Anyone views active bank accounts" on bank_accounts;
create policy "Anyone views active bank accounts" on bank_accounts
    for select using (is_active = true);

drop policy if exists "Admins manage bank accounts" on bank_accounts;
create policy "Admins manage bank accounts" on bank_accounts
    for all using (
        (auth.jwt() -> 'app_metadata' ->> 'role') = 'admin'
    );

-- =====================================================
-- Comentarios para documentación
-- =====================================================
comment on table bookings is 'Customer car rental reservations. Created in pending_payment, transitions to paid when payment confirmed.';
comment on table payments is 'PayPal payment transactions linked to bookings.';
comment on table bank_transfers is 'Bank transfer payment instructions and approval status per booking.';
comment on table bank_accounts is 'Company bank accounts displayed to customers for transfer instructions.';
comment on column bookings.reference_code is 'Customer-facing reference code (e.g. 5J-A7K9X3). Used as bank transfer memo.';
comment on column bookings.status is 'pending_payment → awaiting_transfer_approval (bank) → paid (approved) → refunded/cancelled/rejected';
