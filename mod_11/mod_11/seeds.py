from faker import Faker

from db import SessionLocal
from models import Contact


db = SessionLocal()

fake = Faker(["uk-UA"])
contact_list = []

for _ in range(100):
    contact = Contact(
        name=fake.first_name(),
        surname=fake.last_name(),
        email=fake.ascii_free_email(),
        phone=fake.phone_number(),
        birthday=fake.date_of_birth(minimum_age=10, maximum_age=75),
    )
    contact_list.append(contact)

db.add_all(contact_list)
db.commit()
