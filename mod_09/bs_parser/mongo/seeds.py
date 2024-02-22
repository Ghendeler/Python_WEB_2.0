import json

import connect
from models import Quote, Author


def read_json_file(file):
    with open(file, encoding="UTF-8") as f:
        json_ = json.loads(f.read())
    return json_


def main():

    authors = {}

    authors_json = read_json_file("..\\json\\authors.json")
    for author in authors_json:
        authors[author['fullname']] = \
            Author(
                fullname=author['fullname'],
                born_date=author['born_date'],
                born_location=author['born_location'],
                description=author['description']
            ).save()

    quotes_json = read_json_file("..\\json\\quotes.json")
    for quote in quotes_json:
        Quote(
            tags=quote['tags'],
            author=authors[quote['author']],
            quote=quote['quote'],
        ).save()


if __name__ == "__main__":
    main()
