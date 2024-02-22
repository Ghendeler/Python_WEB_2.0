import json
import requests

from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com/"


def find_next_page_url(soup):
    next_page_button = soup.find(class_="next")
    if next_page_button:
        return next_page_button.find("a")["href"]


def get_quotes(soup):
    quotes_ = []
    raw_quotes = soup.find_all("div", class_="quote")

    for quote in raw_quotes:
        tags = quote.find_all(class_="tag")
        quotes_.append(
            {
                "quote": quote.find("span", class_="text").text,
                "author": quote.find(class_="author").text,
                "author_url": f"{BASE_URL}{quote.find('a')['href'][1:]}",
                "tags": [tag.text for tag in tags],
            }
        )
    return quotes_


def get_author(soup):
    author = {}
    author["fullname"] = soup.find(class_="author-title").text
    author["born_date"] = soup.find(class_="author-born-date").text
    author["born_location"] = soup.find(class_="author-born-location").text
    author["description"] = soup.find(class_="author-description").text
    return author


def parse_data(url):
    quotes_ = []

    while True:
        html_doc = requests.get(url)

        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.text, "html.parser")
            quotes_.extend(get_quotes(soup))
            next_page_url = find_next_page_url(soup)
            if next_page_url:
                print(next_page_url)
                url = f"{BASE_URL}{next_page_url}"
            else:
                break
    return quotes_


def main():
    quotes = parse_data(BASE_URL)

    quotes_list = [
        {"quote": quote["quote"], "author": quote["author"], "tags": quote["tags"]}
        for quote in quotes
    ]

    authors_list = []
    authors_url = {quote["author"]: quote["author_url"] for quote in quotes}

    for author_url in authors_url.values():
        html_doc = requests.get(author_url)

        if html_doc.status_code == 200:
            soup = BeautifulSoup(html_doc.text, "html.parser")
            authors_list.append(get_author(soup))

    with open('json\\quotes.json', 'w') as fh:
        json.dump(quotes_list, fh, indent=2)
    with open('json\\authors.json', 'w') as fh:
        json.dump(authors_list, fh, indent=2)


if __name__ == "__main__":
    main()
