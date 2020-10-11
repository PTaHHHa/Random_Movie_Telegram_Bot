import scrapy
import time

class RandomMovieSpider(scrapy.Spider):

    # def __init__(self, genre, **kwargs):
    #     super().__init__(**kwargs)
    #     self.genre = genre

    name = 'spider'

    def start_requests(self):
        yield scrapy.Request(f'https://www.kinopoisk.ru/popular/films/?sort=popularity&tab=all')

    def parse(self, response):
        for i in range(30):
            response_url = response.xpath("//a[@class='selection-film-item-meta__link']/@href")[i].extract()
            # url = f"https://www.kinopoisk.ru{response_url}"
            parse_url = response.urljoin(''.join(response_url))
            print(parse_url)
            time.sleep(2)
            yield scrapy.Request(parse_url, callback=self.parse_movie)

    def parse_movie(self, response, **kwargs):
        # for i in range(30):
        print('hello')
        try:
            """НАПИСАТЬ РЕГУЛЯРКУ ДЛЯ ПРОВЕРКИ НА INTEGER"""
            # if '%' in response.xpath("//span[contains(@class,'rating__value')]").extract()[1]:
            #     print('WRONG: '+response.xpath("//p[@class='selection-film-item-meta__name']/text()").extract(),)
            # else:
            yield {
                'title': response.xpath("//span[@data-tid='35f45dae']/text()")[0].extract(),
                'original_title': response.xpath
                ("//span[@class='styles_originalTitle__29LcV']/text()").extract(),
                'rating': response.xpath("//span[contains(@class,'film-rating-value')]/text()")[0].extract(),
                # 'url': 'https://www.kinopoisk.ru' +
                #        f'{response.xpath("""//a[@class="selection-film-item-meta__link"]/@href""")[i].extract()}'
            }
        except IndexError:
            print('IndexError, perhaps movie list is over. Check json file!')
        # next_page = response.xpath("//a[@class='paginator__page-relative']/@href").extract()
        # if next_page is not None:
        #     next_page = response.urljoin(''.join(next_page[-1]))
        #     yield scrapy.Request(next_page, callback=self.parse)
