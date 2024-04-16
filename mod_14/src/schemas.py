from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    """
    A Pydantic model representing a contact.
    """
    name: str
    surname: str
    email: EmailStr | None = Field(default=None)
    phone: str
    birthday: date
    note: Optional[str]  # Additional data (optional)


class ResponseContactModel(BaseModel):
    """
    A Pydantic model representing the response containing contact details.
    """
    id: int
    name: str
    surname: str
    email: Optional[EmailStr]
    phone: str
    birthday: date
    note: Optional[str]


class UserModel(BaseModel):
    """
    A Pydantic model representing a user.
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    A Pydantic model representing a user in the database.
    """
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    A Pydantic model representing the response containing user details.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    A Pydantic model representing a token.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    """
    A Pydantic model representing a request containing an email.
    """
    email: EmailStr
