from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.session import get_db
from src.db import models
from src.utils.auth import require_admin
from src.routes.cars.schemas import CarResponse, CarCreate, CarUpdate

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("", response_model=list[CarResponse])
async def list_cars(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Car).order_by(models.Car.brand, models.Car.color))
    return result.scalars().all()


@router.get("/{slug}", response_model=CarResponse)
async def get_car(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Car).filter(models.Car.slug == slug))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")
    return car


@router.post("", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    body: CarCreate,
    db: AsyncSession = Depends(get_db),
    admin: models.User = Depends(require_admin),
):
    result = await db.execute(select(models.Car).filter(models.Car.slug == body.slug))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un auto con ese slug",
        )
    car = models.Car(**body.model_dump())
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return car


@router.put("/{slug}", response_model=CarResponse)
async def update_car(
    slug: str,
    body: CarUpdate,
    db: AsyncSession = Depends(get_db),
    admin: models.User = Depends(require_admin),
):
    result = await db.execute(select(models.Car).filter(models.Car.slug == slug))
    car = result.scalars().first()
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auto no encontrado")

    if body.price_per_day is not None:
        car.price_per_day = body.price_per_day
    if body.available is not None:
        car.available = body.available
    if body.description is not None:
        car.description = body.description

    await db.commit()
    await db.refresh(car)
    return car
