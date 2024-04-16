from datetime import date
from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ResponseContactModel


async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    """
    Get a list of contacts for a specific user.

    :param skip: Number of contacts to skip.
    :param limit: Maximum number of contacts to return.
    :param user: The user for whom to get the contacts.
    :param db: Database session.
    :return: List of contacts.
    """
    return (
        db.query(Contact)
        .filter(Contact.user_id == user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Get a specific contact for a user.

    :param contact_id: The id of the contact to get.
    :param user: The user for whom to get the contact.
    :param db: Database session.
    :return: The requested contact.
    """
    return (
        db.query(Contact)
        .filter(Contact.id == contact_id, Contact.user_id == user.id)
        .first()
    )


async def create_contact(body: ContactModel, user: User, db: Session):
    """
    Create a new contact for a user.

    :param body: The contact information.
    :param user: The user for whom to create the contact.
    :param db: Database session.
    :return: The created contact.
    """
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
    """
    Update a contact for a user.

    :param contact_id: The id of the contact to update.
    :param body: The updated contact information.
    :param user: The user for whom to update the contact.
    :param db: Database session.
    :return: The updated contact.
    """
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
    """
    Remove a contact for a user.

    :param contact_id: The id of the contact to remove.
    :param user: The user for whom to remove the contact.
    :param db: Database session.
    :return: The removed contact.
    """
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
    """
    Get contacts for a user whose birthday is within a certain number of days.

    :param days: The number of days within which the contact's birthday falls.
    :param user: The user for whom to get the contacts.
    :param db: Database session.
    :return: The contacts whose birthday falls within the specified number of days.
    """
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


async def get_contacts_by_str(find_str: str, user: User, db: Session):
    """
    Get contacts for a user based on a search string.

    :param find_str: The string to search for in the contact's name, surname, and email.
    :param user: The user for whom to get the contacts.
    :param db: Database session.
    :return: The contacts that match the search string.
    """
    contacts = (
        db.query(Contact)
        .filter(
            or_(
                Contact.name.like(f"%{find_str}%"),
                Contact.surname.like(f"%{find_str}%"),
                Contact.email.like(f"%{find_str}%"),
            ),
            Contact.user_id == user.id,
        )
        .all()
    )
    return contacts
