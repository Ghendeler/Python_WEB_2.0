import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        'FEEDS': {'quotes.json': {
                    'format': 'json',
                    'indent': 2
                }}
        }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield {
                "qoute": quote.xpath("span[@class='text']/text()").get(),
                "author": quote.xpath("span/small/text()").get(),
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
            }

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname": content.xpath("h3[@class='author-title']/text()").get(),
            "born_date": content.xpath("//span[@class='author-born-date']/text()").get(),
            "born_location": content.xpath("//span[@class='author-born-location").get(),
            "description": content.xpath("//div[@class='author-description']/text()").get()
        }


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]
    custom_settings = {
        'FEEDS': {'authors.json': {
                    'format': 'json',
                    'indent': 2
                }}
        }

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            author_url = quote.xpath("span[2]/a/@href").get()
            yield response.follow(url=self.start_urls[0] + author_url, callback=self.parse_author)
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        yield {
            "fullname": content.xpath("h3[@class='author-title']/text()").get(),
            "born_date": content.xpath("p/span[@class='author-born-date']/text()").get(),
            "born_location": content.xpath("p/span[@class='author-born-location']/text()").get(),
            "description": content.xpath("div[@class='author-description']/text()").get().strip()
        }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.crawl(AuthorsSpider)
    process.start()
