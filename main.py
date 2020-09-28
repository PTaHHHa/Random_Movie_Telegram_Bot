TODO: """РЕАЛИЗОВАТЬ САМОГО БОТА"""
import requests
from lxml import html
import time


def main(genre):
    genre_dict = {'боевик': 'action/', 'фантастика': 'sci-fi/', 'драма': 'drama/', 'детектив': 'mystery/',
                  'биография': 'biography/', 'аниме': 'anime/',
                  'ужасы': 'horror/', 'фэнтези': 'fantasy/', 'приключения': 'adventure/', 'триллер': 'thriller/',
                  'мелодрама': 'romance/', 'мультфильм': 'animation/',
                  'комедия': 'comedy/', 'криминал': 'crime/'}
    url = f'https://www.kinopoisk.ru/popular/films/{genre_dict.get(genre)}?sort=popularity&tab=all'
    r = requests.get(url)
    print(r.status_code)
    t = html.fromstring(r.content.decode('utf-8'))
    try:
        page = t.xpath("//a[@class='paginator__page-number']/text()")[-1]
    except IndexError:
        page = 1
    movie_list = []
    for page_index in range(1, int(page) + 1):
        print(f'Page: {page_index}')
        url = f'https://www.kinopoisk.ru/popular/films/{genre_dict.get(genre)}?page={page_index}&sort=popularity&tab=all'
        print(url)
        r = requests.get(url)
        t = html.fromstring(r.content.decode('utf-8'))
        no_movie = t.xpath("//span[@class='rating__value rating__value_positive']/text()")
        for i in range(30):
            genre_list = t.xpath(f"//div[@class='desktop-rating-selection-film-item']"
                                 f"[{i}]/div[2]/div[1]/div[1]/div/a/p[3]/span[2]/text()")
            for item in genre_list:
                if genre in item and not '%' in no_movie:
                    name = t.xpath("//p[@class='selection-film-item-meta__name']/text()")[i - 1]
                    movie_list.append(name)
                else:
                    pass
    print(movie_list)
    r.close()


if __name__ == '__main__':
    main('комедия')
