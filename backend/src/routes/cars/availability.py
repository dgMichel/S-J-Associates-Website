from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from src.db.supabase import get_supabase_admin
from src.utils.auth import require_admin
from src.routes.cars.schemas import (
    UnavailableDateCreate,
    UnavailableRangeCreate,
    UnavailableDateResponse,
)

router = APIRouter(prefix="/cars", tags=["Availability"])

KNOWN_SLUGS = {
    "suzuki-ignis-red-py-807",
    "suzuki-ignis-gold-paq-852",
    "suzuki-ignis-white-paq-855",
    "suzuki-ignis-gold-paq-853",
    "suzuki-ignis-turquoise-py-808",
    "nissan-cube-brown-pr-945",
}

MAX_RANGE_DAYS = 365


def _serialize(row: dict) -> UnavailableDateResponse:
    return UnavailableDateResponse(
        id=row["id"],
        date=row["date"],
        reason=row.get("reason"),
    )


def _parse_iso(date_str: str) -> datetime:
    try:
        return datetime.fromisoformat(date_str)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fecha inválida: {date_str}. Use YYYY-MM-DD",
        )


def _daterange(start: datetime, end: datetime):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


@router.get("/{slug}/unavailable", response_model=list[UnavailableDateResponse])
async def list_unavailable(slug: str):
    if slug not in KNOWN_SLUGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    sb = get_supabase_admin()
    result = (
        sb.table("unavailable_dates")
        .select("*")
        .eq("car_slug", slug)
        .order("date")
        .execute()
    )
    return [_serialize(row) for row in (result.data or [])]


@router.post("/{slug}/unavailable/range", response_model=list[UnavailableDateResponse], status_code=status.HTTP_201_CREATED)
async def add_unavailable_range(slug: str, body: UnavailableRangeCreate, _=Depends(require_admin)):
    if slug not in KNOWN_SLUGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    start = _parse_iso(body.start)
    end = _parse_iso(body.end)
    if end < start:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end debe ser >= start")

    days = (end - start).days + 1
    if days > MAX_RANGE_DAYS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rango demasiado grande ({days} días). Máximo {MAX_RANGE_DAYS}.",
        )

    rows = [
        {"car_slug": slug, "date": d.date().isoformat(), "reason": body.reason}
        for d in _daterange(start, end)
    ]

    sb = get_supabase_admin()
    result = sb.table("unavailable_dates").upsert(rows, on_conflict="car_slug,date").execute()
    inserted = result.data or []
    if not inserted:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo insertar el rango")
    return [_serialize(row) for row in inserted]


@router.post("/{slug}/unavailable", response_model=UnavailableDateResponse, status_code=status.HTTP_201_CREATED)
async def add_unavailable(slug: str, body: UnavailableDateCreate, _=Depends(require_admin)):
    if slug not in KNOWN_SLUGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    _parse_iso(body.date)

    sb = get_supabase_admin()
    existing = (
        sb.table("unavailable_dates")
        .select("id")
        .eq("car_slug", slug)
        .eq("date", body.date)
        .execute()
    )
    if existing.data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Fecha ya marcada como no disponible")

    result = (
        sb.table("unavailable_dates")
        .insert({"car_slug": slug, "date": body.date, "reason": body.reason})
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo insertar")
    return _serialize(result.data[0])


@router.delete("/{slug}/unavailable/range", status_code=status.HTTP_204_NO_CONTENT)
async def remove_unavailable_range(slug: str, start: str, end: str, _=Depends(require_admin)):
    if slug not in KNOWN_SLUGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    s = _parse_iso(start)
    e = _parse_iso(end)
    if e < s:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="end debe ser >= start")

    days = (e - s).days + 1
    if days > MAX_RANGE_DAYS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rango demasiado grande ({days} días). Máximo {MAX_RANGE_DAYS}.",
        )

    dates = [d.date().isoformat() for d in _daterange(s, e)]
    sb = get_supabase_admin()
    sb.table("unavailable_dates").delete().eq("car_slug", slug).in_("date", dates).execute()
    return None


@router.delete("/{slug}/unavailable/{date_str}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_unavailable(slug: str, date_str: str, _=Depends(require_admin)):
    if slug not in KNOWN_SLUGS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    _parse_iso(date_str)
    sb = get_supabase_admin()
    sb.table("unavailable_dates").delete().eq("car_slug", slug).eq("date", date_str).execute()
    return None
