import configparser
import os

import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "books.settings")
django.setup()

from quotes.models import Author, Quote, Tag  # noqa

path = os.path.abspath(os.getcwd()) + "/utils/config.ini"
config = configparser.ConfigParser()
config.read(path)

mongo_user = config.get("DB", "user")
mongodb_pass = config.get("DB", "pass")
db_name = config.get("DB", "db_name")
domain = config.get("DB", "domain")

print("test")
client = MongoClient(
    f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority",
    ssl=True,
)

# db = client
db = client.quotes
# print(
#     f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"
# )

def get_slug(data):
    return data.strip().replace(' ', '-')


authors = db.author.find()
print(authors)
i = 0
for author in authors:
    print(i)
    i += 1
    print(author["fullname"])
    Author.objects.get_or_create(
        fullname=author["fullname"],
        slug=get_slug(author["fullname"]),
        born_date=author["born_date"],
        born_location=author["born_location"],
        description=author["description"],
    )

quotes = db.quote.find()

for quote in quotes:
    tags = list()
    for tag in quote["tags"]:
        t, _ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    author = db.author.find_one({"_id": quote["author"]})
    print(author)
    print(author['fullname'])
    author_obj = Author.objects.get(fullname=author["fullname"])
    print(author_obj)
    quote = Quote.objects.create(quote=quote["quote"], author=author_obj)

    for tag in tags:
        quote.tags.add(tag)
