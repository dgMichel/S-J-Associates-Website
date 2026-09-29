from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional, Literal
import re


EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


# =====================================================
# BOOKINGS
# =====================================================

class BookingCreate(BaseModel):
    car_slug: str
    start_date: date
    end_date: date
    customer_name: str = Field(min_length=2, max_length=120)
    customer_email: str
    customer_phone: Optional[str] = None
    customer_country: Optional[str] = None
    nationality: Literal["national", "foreign"]
    payment_method: Literal["paypal", "bank_transfer"]

    @field_validator("car_slug")
    @classmethod
    def slug_valid(cls, v: str) -> str:
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("slug inválido")
        return v

    @field_validator("customer_email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        if not EMAIL_RE.match(v):
            raise ValueError("email inválido")
        return v.lower().strip()

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: date, info) -> date:
        start = info.data.get("start_date")
        if start and v < start:
            raise ValueError("end_date debe ser >= start_date")
        return v


class BookingResponse(BaseModel):
    id: int
    reference_code: str
    car_slug: str
    start_date: date
    end_date: date
    days: int
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None
    customer_country: Optional[str] = None
    nationality: str
    currency: str
    subtotal: Decimal
    deposit: Decimal
    total: Decimal
    status: str
    payment_method: str
    notes: Optional[str] = None
    created_at: datetime
    confirmed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BookingListItem(BaseModel):
    id: int
    reference_code: str
    car_slug: str
    start_date: date
    end_date: date
    days: int
    customer_name: str
    customer_email: str
    nationality: str
    currency: str
    total: Decimal
    status: str
    payment_method: str
    created_at: datetime
    confirmed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class BookingRejectRequest(BaseModel):
    reason: str = Field(min_length=3, max_length=500)


# =====================================================
# PAYMENTS (PayPal)
# =====================================================

class PayPalCreateOrderRequest(BaseModel):
    booking_id: int


class PayPalCreateOrderResponse(BaseModel):
    payment_id: int
    order_id: str
    approval_url: str


class PayPalCaptureResponse(BaseModel):
    payment_id: int
    status: str
    booking_status: str


# =====================================================
# BANK TRANSFERS
# =====================================================

class BankInstructionsResponse(BaseModel):
    booking_id: int
    reference_code: str
    bank_name: str
    account_name: str
    account_number: str
    swift_code: Optional[str] = None
    currency: str
    amount: Decimal
    instructions: Optional[str] = None


class BankProofSubmit(BaseModel):
    proof_url: str = Field(min_length=5, max_length=500)
