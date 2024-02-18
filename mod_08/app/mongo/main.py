import redis
from mongoengine.queryset.visitor import Q

import connect
from models import Quote, Author


PROMPT = " >>> "

r = redis.Redis(host="localhost", port=6379, password=None)


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


def put_to_cash(key, value):
    r.set(key, value)
    return True


def get_from_cash(key):
    value = r.get(key)
    print(value)
    if value:
        print('from cach')
    return value


@input_error
def find_by_author(name):
    if name is None:
        raise ValueError
    result = get_from_cash("author" + name[0])
    if result is None:
        author = Author.objects(fullname__istartswith=name[0]).first()
        quotes = Quote.objects(author=author.id)
        result = str()
        for quote in quotes:
            result += ("-------------------\n")
            result += f"quote: {quote.quote}\n \
                author: {quote.author.fullname}\n \
                tags: {quote.tags}\n"
        put_to_cash(("author" + name[0]), result)
    if isinstance(result, bytes):
        result = result.decode('utf8')
    return result


@input_error
def find_by_tag(tag):
    if tag is None:
        raise ValueError
    result = get_from_cash("tag" + tag[0])
    if result is None:
        quotes = Quote.objects(tags__istartswith=tag[0])
        result = str()
        for quote in quotes:
            result += ("-------------------\n")
            result += (f"quote: {quote.quote} \n \
                author: {quote.author.fullname} \n \
                tags: {quote.tags}")
        put_to_cash(("tag" + tag[0]), result)
    if isinstance(result, bytes):
        result = result.decode('utf8')
    return result


@input_error
def find_by_tags(tags):
    if tags is None:
        raise ValueError
    result = get_from_cash("tags" + tags[0] + tags[1])
    if result is None:
        quotes = Quote.objects(
            Q(tags__istartswith=tags[0]) |
            Q(tags__istartswith=tags[1])
        )
        result = str()
        for quote in quotes:
            result += ("-------------------\n")
            result += (f"quote: {quote.quote} \n \
                author: {quote.author.fullname} \n \
                tags: {quote.tags}\n")
        put_to_cash(("tags" + tags[0] + tags[1]), result)
    if isinstance(result, bytes):
        result = result.decode('utf8')
    return result


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
