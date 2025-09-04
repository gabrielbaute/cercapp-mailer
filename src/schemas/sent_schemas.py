from pydantic import BaseModel, EmailStr
from datetime import datetime

class SentCreate(BaseModel):
    sender: EmailStr
    recipient: EmailStr
    message: str

class SentResponse(BaseModel):
    id: int
    sender: EmailStr
    recipient: EmailStr
    message: str
    sent_at: datetime

    class Config:
        from_attributes = True