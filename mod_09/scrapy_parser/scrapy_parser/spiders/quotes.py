import scrapy


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
            # print('test=', quote)
            yield {
                "qoute": quote.xpath("span[@class='text']/text()").get(),
                "author": quote.xpath("span/small/text()").get(),
                "tags": quote.xpath("div[@class='tags']/a/text()").extract(),
            }

            # yield response.follow(url=self.start_urls[0] + quote.xpath("span/a/@href").get(), callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
