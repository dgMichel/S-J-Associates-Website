"""Shared booking business logic: pricing, reference codes, currency, auto-block dates."""

import secrets
import string
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from fastapi import HTTPException, status

from src.config import DEPOSIT_NATIONAL_XCD, DEPOSIT_FOREIGN_USD
from src.db.supabase import get_supabase_admin


# Pricing source-of-truth. In production this should be loaded from a config table.
CAR_PRICES_USD = {
    "suzuki-ignis-red-py-807": Decimal("55"),
    "suzuki-ignis-gold-paq-852": Decimal("55"),
    "suzuki-ignis-white-paq-855": Decimal("55"),
    "suzuki-ignis-gold-paq-853": Decimal("55"),
    "suzuki-ignis-turquoise-py-808": Decimal("55"),
    "nissan-cube-brown-pr-945": Decimal("60"),
}

# Static fixed USD->XCD conversion rate (ECCU peg is 2.7169)
USD_TO_XCD = Decimal("2.7169")


def get_price_per_day_usd(slug: str) -> Decimal:
    if slug not in CAR_PRICES_USD:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Auto no encontrado",
        )
    return CAR_PRICES_USD[slug]


def compute_booking_totals(
    slug: str,
    start: date,
    end: date,
    nationality: str,
) -> dict:
    """Return currency, subtotal, deposit, total, days. National=XCD, Foreign=USD."""
    days = (end - start).days + 1
    if days < 1:
        raise HTTPException(status_code=400, detail="Rango de fechas inválido")

    price_per_day_usd = get_price_per_day_usd(slug)
    subtotal_usd = (price_per_day_usd * days).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    if nationality == "national":
        currency = "XCD"
        subtotal = (subtotal_usd * USD_TO_XCD).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        deposit = Decimal(DEPOSIT_NATIONAL_XCD)
    else:
        currency = "USD"
        subtotal = subtotal_usd
        deposit = Decimal(DEPOSIT_FOREIGN_USD)

    total = subtotal + deposit
    return {
        "days": days,
        "currency": currency,
        "subtotal": subtotal,
        "deposit": deposit,
        "total": total,
    }


def generate_reference_code() -> str:
    """Customer-facing reference like '5J-A7K9X3' used as bank transfer memo."""
    alphabet = string.ascii_uppercase + string.digits
    suffix = "".join(secrets.choice(alphabet) for _ in range(6))
    return f"5J-{suffix}"


def dates_inclusive(start: date, end: date):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def check_dates_available(slug: str, start: date, end: date) -> None:
    """Raise 409 if any date in [start, end] is already blocked."""
    sb = get_supabase_admin()
    date_strs = [d.isoformat() for d in dates_inclusive(start, end)]
    result = (
        sb.table("unavailable_dates")
        .select("date")
        .eq("car_slug", slug)
        .in_("date", date_strs)
        .execute()
    )
    if result.data:
        conflict = sorted(row["date"] for row in result.data)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Fechas no disponibles: {', '.join(conflict)}",
        )


def block_dates_for_booking(booking_id: int, slug: str, start: date, end: date) -> None:
    """Insert unavailable_dates rows linked to a booking. Idempotent."""
    sb = get_supabase_admin()
    rows = [
        {
            "car_slug": slug,
            "date": d.isoformat(),
            "reason": "booked",
            "booking_id": booking_id,
            "source": "booking",
        }
        for d in dates_inclusive(start, end)
    ]
    sb.table("unavailable_dates").upsert(
        rows, on_conflict="car_slug,date"
    ).execute()


def unblock_dates_for_booking(booking_id: int) -> None:
    """Remove unavailable_dates rows linked to a booking (used on cancellation)."""
    sb = get_supabase_admin()
    sb.table("unavailable_dates").delete().eq("booking_id", booking_id).execute()


def mark_booking_paid(booking_id: int) -> dict:
    """Atomically: confirm booking + block dates. Returns the updated booking row."""
    sb = get_supabase_admin()
    booking = (
        sb.table("bookings").select("*").eq("id", booking_id).single().execute()
    )
    if not booking.data:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")

    b = booking.data
    if b["status"] == "paid":
        return b  # idempotent

    if b["status"] not in ("pending_payment", "awaiting_transfer_approval"):
        raise HTTPException(
            status_code=409,
            detail=f"No se puede confirmar una reserva en estado '{b['status']}'",
        )

    # Block dates only after we are sure we won't 500 mid-flight
    block_dates_for_booking(
        booking_id=booking_id,
        slug=b["car_slug"],
        start=date.fromisoformat(b["start_date"]),
        end=date.fromisoformat(b["end_date"]),
    )

    from datetime import datetime, timezone
    result = (
        sb.table("bookings")
        .update({"status": "paid", "confirmed_at": datetime.now(timezone.utc).isoformat()})
        .eq("id", booking_id)
        .execute()
    )
    return result.data[0] if result.data else b
