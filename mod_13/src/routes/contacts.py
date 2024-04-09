from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Contact, User
from src.repository import contacts as repository_contacts
from src.schemas import ContactModel, ResponseContactModel
from src.services.auth import auth_service

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get(
    "/",
    response_model=List[ResponseContactModel],
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/{contact_id}", response_model=ResponseContactModel)
async def read_contact(
    contact_id: int = Path(description="The ID of the contact to get", gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post(
    "/",
    response_model=ContactModel,
    description="No more than 10 requests per minute",
    dependencies=[Depends(RateLimiter(times=10, seconds=60))]
)
async def create_contact(
    body: ContactModel,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.update_contact(
        contact_id, body, current_user, db
    )
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def remove_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )
    return contact


# ----------------------------------------------------
@router.get("/birthday/", response_model=list[ResponseContactModel])
async def contacts_birthday(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.get_contacts_by_birthday(
        days, current_user, db
    )
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/find/", response_model=list[ResponseContactModel])
async def find_contacts(
    find_str: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    contacts = await repository_contacts.get_contacts_by_str(find_str, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts
