import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/Science/?stype=0']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-title-link']//@href").getall()
        next_page = response.xpath("//div[@class='pagination-next']//@href ").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield  response.follow(link, callback = self.parse_book)

    def parse_book(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").get()
        book_author = response.xpath("//a[contains(@data-event-label, 'author')]/text()").getall()
        book_price_main = response.xpath("//span[@class = 'buying-priceold-val-number']/text()").get()
        book_price_discont = response.xpath("//span[@class = 'buying-pricenew-val-number']/text()").get()
        book_rating = float(response.xpath("//div[@id = 'rate']/text()").get())
        yield BooksItem(name = book_name, author = book_author, price_main = book_price_main,
        price_discont = book_price_discont, rating = book_rating)
