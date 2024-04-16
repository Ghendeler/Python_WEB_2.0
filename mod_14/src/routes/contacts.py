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
    """
    Get a list of contacts.

    :param skip: Number of contacts to skip for the result.
    :param limit: Maximum number of contacts to return.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: List of contacts.
    """
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
    """
    Get a specific contact by ID.

    :param contact_id: ID of the contact to get.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: Contact with the given ID.
    """
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
    """
    Create a new contact.

    :param body: Contact details.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: Created contact.
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(
    body: ContactModel,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Update a specific contact by ID.

    :param body: Contact details to update.
    :param contact_id: ID of the contact to update.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: Updated contact.
    """
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
    """
    Delete a specific contact by ID.

    :param contact_id: ID of the contact to delete.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: Deleted contact.
    """
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )
    return contact


@router.get("/birthday/", response_model=list[ResponseContactModel])
async def contacts_birthday(
    days: int = 7,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    Get contacts who have a birthday within a certain number of days.

    :param days: Number of days to check for birthdays.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: List of contacts with birthdays within the specified number of days.
    """
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
    """
    Find contacts by a search string.

    :param find_str: Search string to find contacts.
    :param db: Database session.
    :param current_user: Current authenticated user.
    :return: List of contacts that match the search string.
    """
    contacts = await repository_contacts.get_contacts_by_str(find_str, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts
