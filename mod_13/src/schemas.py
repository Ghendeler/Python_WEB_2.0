from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr | None = Field(default=None)
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


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr
