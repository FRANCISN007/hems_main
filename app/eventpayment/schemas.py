from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Base Schema for EventPayment
class EventPaymentBase(BaseModel):
    event_id: int
    organiser: str
    amount_paid: float
    discount_allowed: float = 0.0
    payment_method: str
    payment_status: Optional[str] = "pending"
    created_by: str

    class Config:
        from_attributes = True  # Replaces `orm_mode = True` for newer Pydantic versions

# Schema for Creating an Event Payment
class EventPaymentCreate(EventPaymentBase):
    pass

# Schema for Response when Retrieving an Event Payment
class EventPaymentResponse(BaseModel):
    id: int
    event_id: int
    organiser: str
    event_amount: float  #  Ensure this field exists
    amount_paid: float
    discount_allowed: float
    balance_due: float
    payment_method: str
    payment_status: str
    payment_date: datetime
    created_by: str

    class Config:
        from_attributes = True
