from datetime import date
from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, text

from db import Base, get_db, engine
from models import Contact
from schemas import ContactModel, ResponseContactModel

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api")
async def root():
    return {"message": "Welcome to FastAPI!"}


@app.get("/api/healthchecker")
async def healthchecker(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.post("/contacts/new")
async def create_contact(contact: ContactModel, db: Session = Depends(get_db)):
    new_contact = Contact(
        name=contact.name,
        surname=contact.surname,
        phone=contact.phone,
        birthday=contact.birthday,
        note=contact.note,
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@app.get("/contacts", response_model=list[ResponseContactModel])
async def read_contacts(
    skip: int = 0,
    limit: int = Query(default=10, ge=10, le=100),
    db: Session = Depends(get_db),
):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@app.get("/contacts/{contact_id}", response_model=ResponseContactModel)
async def read_contact(
    contact_id: int = Path(description="The ID of the note to get", gt=0, le=10),
    db: Session = Depends(get_db),
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=ResponseContactModel)
async def update_contact(contact_id: int, note: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )

    contact.note = note
    db.commit()
    db.refresh(contact)
    return contact


@app.delete("/Contacts/{contact_id}")
async def del_contact(
    contact_id: int, contact: ResponseContactModel, db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No contact with this id: {contact_id} found",
        )

    if contact:
        db.delete(contact)
        db.commit()
    return {"deleted contact": contact_id}


@app.get("/contacts/birthday/", response_model=list[ResponseContactModel])
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

    """
    def is_next_birthday(birthday, days):
        cur_date = date.today()
        y = cur_date.year
        cur_birthday = birthday.replace(year=y)
        if cur_birthday < cur_date:
            cur_birthday = birthday.replace(year=y+1)
        return (cur_birthday - cur_date) <= days
    """

    """
    select * from (
        select *, cast(birthday + (extract(year from age(birthday)) + 1) * interval '1' year as date) next_birthday
        from contacts )
    where next_birthday >= current_date and next_birthday <= current_date + 60
    order by next_birthday
    """


@app.get("/contacts/find/", response_model=list[ResponseContactModel])
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
