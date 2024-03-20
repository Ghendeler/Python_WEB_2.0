from datetime import date
from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy import or_, text
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactModel, ResponseContactModel
from src.repository import contacts as repository_contacts
from src.database.models import Contact


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ResponseContactModel])
async def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.get("/{contact_id}", response_model=ResponseContactModel)
async def read_contact(
    contact_id: int = Path(description="The ID of the contact to get", gt=0),
    db: Session = Depends(get_db),
):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("/", response_model=ContactModel)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(
    body: ContactModel, contact_id: int, db: Session = Depends(get_db)
):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )
    return contact


@router.delete("/{contact_id}", response_model=ResponseContactModel)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )
    return contact


# ----------------------------------------------------
@router.get("/birthday/", response_model=list[ResponseContactModel])
async def contacts_birthday(days: int = 7, db: Session = Depends(get_db)):
    ids = []
    cur_date = date.today()
    y = cur_date.year

    contacts = db.query(Contact).all()
    for contact in contacts:
        cur_birthday = contact.birthday.replace(year=y)
        if cur_birthday < cur_date:
            cur_birthday = contact.birthday.replace(year=y + 1)
        delta = (cur_birthday - cur_date).days
        if delta <= days:
            ids.append(contact.id)

    contacts_birthday = db.query(Contact).filter(Contact.id.in_(ids)).all()
    return contacts_birthday


@router.get("/find/", response_model=list[ResponseContactModel])
async def find_contacts(find_str: str, db: Session = Depends(get_db)):
    contacts = (
        db.query(Contact)
        .filter(
            or_(
                Contact.name.like(f"%{find_str}%"),
                Contact.surname.like(f"%{find_str}%"),
                Contact.email.like(f"%{find_str}%"),
            )
        )
        .all()
    )
    return contacts
