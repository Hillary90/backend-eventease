from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    event_id: int

class BookingCancel(BaseModel):
    event_id: int

class BookingResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    organizer_id: int

    class Config:
        from_attributes = True

class BookingWithUser(BaseModel):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    user: UserBase

    class Config:
        from_attributes = True

class BookingWithEvent(BaseModel):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    event: EventBase

    class Config:
        from_attributes = True
