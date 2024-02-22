# import lxml
import requests
from bs4 import BeautifulSoup


# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')
# authors = soup.find_all('small', class_='author')
# tags = soup.find_all('div', class_='tags')

# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     print('-' * 20)


url = "http://quotes.toscrape.com/page/"


def get_quotes(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    all_paragraphs = soup.find_all('span', class_='text')
    all_authors = soup.find_all('small', class_='author')
    all_author_urls = soup.select("[href^='/author']")

    for p in all_paragraphs:
        print(p.text)
    for p in all_authors:
        print(p.text)
    for p in all_author_urls:
        print(p['href'])

    print('-' * 10)


if __name__ == '__main__':
    for page_num in range(1, 7):
        page_url = f'{url}{page_num}/'
        get_quotes(page_url)
