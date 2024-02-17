from mongoengine.queryset.visitor import Q

import connect
from models import Quote, Author


PROMPT = " >>> "


# decorator
def input_error(func):
    def inner(*args):
        try:
            result = func(*args)
        except IndexError:
            result = "Wrong command"
        except ValueError:
            result = "Give me something to search"
        except KeyboardInterrupt:
            raise SystemExit
        return result
    return inner


def find_by_author(name):
    if name is None:
        raise ValueError
    author = Author.objects(fullname__istartswith=name[0]).first()
    quotes = Quote.objects(author=author.id)
    for quote in quotes:
        print("-------------------")
        print(
            f"quote: {quote.quote} \n \
                author: {quote.author.fullname} \n \
                tags: {quote.tags}"
        )


@input_error
def find_by_tag(tag):
    if tag is None:
        raise ValueError
    quotes = Quote.objects(tags__istartswith=tag[0])
    for quote in quotes:
        print("-------------------")
        print(f"quote: {quote.quote} \n \
            author: {quote.author.fullname} \n \
            tags: {quote.tags}")


def find_by_tags(tags):
    if tags is None:
        raise ValueError
    quotes = Quote.objects(
        Q(tags__istartswith=tags[0]) |
        Q(tags__istartswith=tags[1])
    )
    for quote in quotes:
        print("-------------------")
        print(f"quote: {quote.quote} \n \
              author: {quote.author.fullname} \n \
              tags: {quote.tags}")


def exit(_):
    print('__ BYE __')
    raise SystemExit


ACTION = {
    "name": find_by_author,
    "tag": find_by_tag,
    "tags": find_by_tags,
    "exit": exit
}


def get_action_handler(action):
    return ACTION.get(action)


def parse_request(string):
    result = {}
    raw_parse = string.split(":")
    result["action"] = raw_parse[0].strip()
    if len(raw_parse) > 1:
        result["conditions"] = [r.strip() for r in raw_parse[1].split(",")]
    else:
        result["conditions"] = None
    return result


@input_error
def find_answer(data):
    parsed_request = parse_request(data)
    if parsed_request == {}:
        raise IndexError
    action_handler = get_action_handler(parsed_request['action'])
    print(action_handler)
    if action_handler:
        result = action_handler(parsed_request['conditions'])
    else:
        raise IndexError
    return result


@input_error
def main():
    while True:
        user_request = input(PROMPT)
        answer = find_answer(user_request)
        print(answer)


if __name__ == "__main__":
    main()
