from sqlalchemy import Column, Integer, String, Date
from db import Base


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    birthday = Column(Date)
    note = Column(String(250))
