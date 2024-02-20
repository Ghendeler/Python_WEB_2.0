from mongoengine import Document
from mongoengine.fields import StringField, EmailField, BooleanField, DateField


class Customer(Document):
    fullname = StringField()
    email = EmailField()
    sended = BooleanField(default=False)
    born_date = DateField()
    location = StringField()
    address = StringField()
    description = StringField()
