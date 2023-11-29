from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date


class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr = None
    phone: str
    birthday: date
    note: Optional[str]  # Додаткові дані (необов'язково)


class ResponseContactModel(BaseModel):
    id: int
    name: str
    surname: str
    email: Optional[EmailStr]
    phone: str
    birthday: date
    note: Optional[str]
