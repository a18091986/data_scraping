import scrapy
from scrapy.http import HtmlResponse
from books.items import BooksItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=science']
    i = 2

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='product-card__image-link smartLink']//@href").getall()
        # next_page = 'http://book24.ru/search/page-' + str(2) + '/?q=science'
        next_page_link = 'http://book24.ru/search/page-' + str(Book24Spider.i) + '/?q=science'
        if len(links) > 0:
            Book24Spider.i += 1
            yield response.follow(next_page_link, callback=self.parse)

        for link in links:
            yield  response.follow(link, callback = self.parse_book)

    def parse_book(self, response: HtmlResponse):
        book_name = response.xpath("//h1/text()").get()
        book_author = response.xpath("//div[@class = 'product-characteristic__value']//text()").getall()[0]
        book_price_main = response.xpath("//span[@class = 'app-price product-sidebar-price__price']/text()").get()
        book_rating = response.xpath("//span[@class = 'rating-widget__main-text']/text()").get()
        yield BooksItem(name = book_name, author = book_author, price_main = book_price_main, rating = book_rating)
