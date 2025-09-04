from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ContactCreate(BaseModel):
    username: str
    email: EmailStr

class ContactUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class ContactResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True