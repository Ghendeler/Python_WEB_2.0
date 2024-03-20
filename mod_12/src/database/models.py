from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    surname = Column(String(50))
    email = Column(String(50))
    phone = Column(String(20))
    birthday = Column(Date)
    note = Column(String(250))
