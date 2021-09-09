import scrapy
from scrapy.http import HtmlResponse
from LM.items import LMparserItem
from scrapy.loader import ItemLoader

class LMSpider(scrapy.Spider):
    name = 'lm'
    allowed_domains = ['leroymerlin.ru']
    i = 2
    start_url = ''

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={query}']
        LMSpider.start_url = [f'https://leroymerlin.ru/search/?q={query}']

    def parse(self, response: HtmlResponse):
        '''Получаем ссылки на объекты и ссылку на след. страницу'''
        ads_links = response.xpath("//div[@class='phytpj4_plp largeCard']/a")
        next_page_link = f'{LMSpider.start_url[0]}&page={str(LMSpider.i)}'
        if len(ads_links) > 0:
            LMSpider.i += 1
            yield response.follow(next_page_link, callback=self.parse)
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)


    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LMparserItem(), response=response)             # Создаем отдельный объект для работы с item (здесь инициализируются все поля item'a и их обработчики)
        loader.add_xpath('name', "//h1/text()")                               # Наполняем item данными (также сразу запускаются предобработчики)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('describe', "//section[@class='pdp-section pdp-section--product-description']//text()")
        loader.add_xpath('photos', "//uc-pdp-media-carousel/picture/source[1]/@data-origin")
        loader.add_value('url', response.url)
        yield loader.load_item()                                                   # Отправляем в пайплайн (также здесь запускаются постобработчики)