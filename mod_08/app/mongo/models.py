from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    quote = StringField()
    author = ReferenceField(Author)
    tags = ListField(StringField())
    meta = {'allow_inheritance': True}
