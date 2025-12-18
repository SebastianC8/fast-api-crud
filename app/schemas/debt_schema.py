from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date


class DebtBase(BaseModel):
    description: str
    value: float
    date: date

class CreateDebt(DebtBase):
    user_id: int

class UpdateDebt(BaseModel):
    description: Optional[str] = None
    value: Optional[float] = None
    date: Optional[date] = None
    status: Optional[bool] = None
    user_id: Optional[int] = None

class DebtResponse(DebtBase):
    id: int
    user_id: int
    date: date
    status: bool
    model_config = ConfigDict(from_attributes=True)

class DebtWithUserResponse(DebtResponse):
    user_nombre: str
    user_apellido: str
    user_email: str
