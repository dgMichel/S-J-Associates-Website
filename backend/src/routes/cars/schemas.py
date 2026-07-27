from pydantic import BaseModel, ConfigDict
from typing import Optional


class CarResponse(BaseModel):
    slug: str
    brand: str
    model: str
    year: int
    color: str
    plate: str
    price_per_day: float
    available: bool
    description: Optional[str] = None
    features: Optional[list[str]] = None
    specs: Optional[dict] = None
    photos: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class CarCreate(BaseModel):
    slug: str
    brand: str
    model: str
    year: int
    color: str
    plate: str
    price_per_day: float
    available: bool = True
    description: Optional[str] = None
    features: Optional[list[str]] = None
    specs: Optional[dict] = None
    photos: Optional[dict] = None


class CarUpdate(BaseModel):
    price_per_day: Optional[float] = None
    available: Optional[bool] = None
    description: Optional[str] = None


class UnavailableDateCreate(BaseModel):
    date: str
    reason: Optional[str] = None


class UnavailableDateResponse(BaseModel):
    id: int
    date: str
    reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
