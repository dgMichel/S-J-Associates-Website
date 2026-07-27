from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime
from src.db.session import get_db
from src.db import models
from src.utils.auth import require_admin
from src.routes.cars.schemas import UnavailableDateCreate, UnavailableDateResponse

router = APIRouter(prefix="/cars", tags=["Availability"])

@router.get("/{slug}/unavailable", response_model=list[UnavailableDateResponse])
async def list_unavailable(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Car).filter(models.Car.slug == slug))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    result = await db.execute(select(models.UnavailableDate).filter(models.UnavailableDate.car_id == car.id))
    dates = result.scalars().all()
    # convert date objects to isoformat strings in pydantic response
    return [UnavailableDateResponse(id=d.id, date=d.date.isoformat(), reason=d.reason) for d in dates]

@router.post("/{slug}/unavailable", response_model=UnavailableDateResponse, status_code=status.HTTP_201_CREATED)
async def add_unavailable(slug: str, body: UnavailableDateCreate, db: AsyncSession = Depends(get_db), admin: models.User = Depends(require_admin)):
    result = await db.execute(select(models.Car).filter(models.Car.slug == slug))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    try:
        d = datetime.fromisoformat(body.date).date()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fecha inválida, use YYYY-MM-DD")
    # check duplicate
    result = await db.execute(select(models.UnavailableDate).filter(models.UnavailableDate.car_id == car.id, models.UnavailableDate.date == d))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Fecha ya marcada como no disponible")
    ud = models.UnavailableDate(car_id=car.id, date=d, reason=body.reason)
    db.add(ud)
    await db.commit()
    await db.refresh(ud)
    return UnavailableDateResponse(id=ud.id, date=ud.date.isoformat(), reason=ud.reason)

@router.delete("/{slug}/unavailable/{date_str}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_unavailable(slug: str, date_str: str, db: AsyncSession = Depends(get_db), admin: models.User = Depends(require_admin)):
    # date_str expected YYYY-MM-DD
    result = await db.execute(select(models.Car).filter(models.Car.slug == slug))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    try:
        d = datetime.fromisoformat(date_str).date()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fecha inválida, use YYYY-MM-DD")
    q = delete(models.UnavailableDate).where(models.UnavailableDate.car_id == car.id, models.UnavailableDate.date == d)
    await db.execute(q)
    await db.commit()
    return None
