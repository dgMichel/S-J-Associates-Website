from pydantic import BaseModel, ConfigDict
from typing import Optional


class UnavailableDateCreate(BaseModel):
    date: str
    reason: Optional[str] = None


class UnavailableRangeCreate(BaseModel):
    start: str
    end: str
    reason: Optional[str] = None


class UnavailableDateResponse(BaseModel):
    id: int
    date: str
    reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
