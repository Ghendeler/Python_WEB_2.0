from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ResponseContactModel


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactModel, db: Session):
    new_contact = Contact(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        note=body.note,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_contact(
    contact_id: int, body: ContactModel, db: Session
) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = (body.name,)
        contact.surname = (body.surname,)
        contact.phone = (body.phone,)
        contact.birthday = (body.birthday,)
        contact.note = (body.note,)
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
