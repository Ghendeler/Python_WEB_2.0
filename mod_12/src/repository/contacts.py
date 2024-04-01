from datetime import date
from typing import List

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ResponseContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.user_id == user.id)
        .first()
    )


async def create_contact(body: ContactModel, user: User, db: Session):
    new_contact = Contact(
        name=body.name,
        surname=body.surname,
        email=body.email,
        phone=body.phone,
        birthday=body.birthday,
        note=body.note,
        user=user,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


async def update_contact(
    contact_id: int, body: ContactModel, user: User, db: Session
) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.user_id == user.id)
        .first()
    )
    if contact:
        contact.name = (body.name,)
        contact.surname = (body.surname,)
        contact.phone = (body.phone,)
        contact.birthday = (body.birthday,)
        contact.note = (body.note,)
        contact.user_id = (user.id,)
        db.commit()
    return contact


async def remove_contact(contact_id: int, user: User, db: Session) -> Contact | None:
    contact = (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.user_id == user.id)
        .first()
    )
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def get_contacts_by_birthday(days: int, user: User, db: Session):
    ids = []
    cur_date = date.today()
    y = cur_date.year

    contacts = db.query(Contact).filter(Contact.user_id == user.id).all()
    for contact in contacts:
        cur_birthday = contact.birthday.replace(year=y)
        if cur_birthday < cur_date:
            cur_birthday = contact.birthday.replace(year=y + 1)
        delta = (cur_birthday - cur_date).days
        if delta <= days:
            ids.append(contact.id)

    contacts_birthday = db.query(Contact).filter(Contact.id.in_(ids)).all()
    return contacts_birthday
