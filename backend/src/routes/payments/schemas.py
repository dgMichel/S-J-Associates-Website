from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class CreateCheckoutSessionRequest(BaseModel):
    car: str
    startDate: str
    days: int
    amount: float


class CreateCheckoutSessionResponse(BaseModel):
    url: str


class BookingResponse(BaseModel):
    id: int
    car_slug: str
    start_date: date
    end_date: date
    days: int
    amount: float
    status: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
