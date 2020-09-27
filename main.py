TODO: """НУЖНО СДЕЛАТЬ СЛОВАРЬ, В КОТОРОМ КЛЮЧАМИ БУДУТ ЖАНРЫ,
А ЗНАЧЕНИЯМИ URL1(ДЛЯ ПОЛУЧЕНИЯ ПАГИНАЦИИ) И URL2(ДЛЯ ПРОБЕЖКИ ПО СТРАНИЦАМ)
ВООБЩЕ МОЖНО ИСПОЛЬЗОВАТЬ ОДИН ЮРЛ, ПРОСТО БРАТЬ ЕГО ВМЕСТЕ С PAGE, ДАЖЕ ЕСЛИ СТРАНИЦА ОДНА
А ПОТОМ УЖЕ МЕНЯТЬ ЗНАЧЕНИЕ PAGE, ЕСЛИ СТРАНИЦ БОЛЬШЕ ОДНОЙ.
ТАК ВСЁ БУДЕТ РАБОТАТЬ НАМНОГО БЫСТРЕЕ.
ЮРЛ НУЖНО БРАТЬ ТУТ https://www.kinopoisk.ru/popular/films/?sort=popularity&tab=all
ТОЛЬКО НУЖНО ВЫБРАТЬ НЕОБХОДИМЫЕ ЖАНРЫ"""
import requests
from lxml import html
import time

start = ['документальный', 'боевик', 'фантастика', 'вестерн', 'драма', 'музыка', 'детектив', 'биография', 'аниме',
         'ужасы',
         'семейный', 'детский', 'фэнтези', 'приключения', 'военный', 'история', 'триллер', 'мелодрама', 'мультфильм',
         'спорт', 'комедия', 'криминал', 'мюзикл']


def main(genre):
    if genre == 'аниме':
        url = 'https://www.kinopoisk.ru/popular/films/anime/?sort=popularity&tab=all'
        r = requests.get(url)
        print(r.status_code)
        t = html.fromstring(r.content.decode('utf-8'))
        try:
            page = t.xpath("//a[@class='paginator__page-number']/text()")[-1]
        except IndexError:
            page = 1
        movie_list = []
        for page_index in range(int(page)):
            print(f'Page: {page_index}')
            url = f'https://www.kinopoisk.ru/popular/films/anime/?page={page_index}&sort=popularity&tab=all'
            r = requests.get(url)
            t = html.fromstring(r.content.decode('utf-8'))
            for i in range(30):
                genre_list = t.xpath(f"//div[@class='desktop-rating-selection-film-item']"
                                     f"[{i}]/div[2]/div[1]/div[1]/div/a/p[3]/span[2]/text()")
                for item in genre_list:
                    # print(no_movie)
                    if genre in item:
                        name = t.xpath("//p[@class='selection-film-item-meta__name']/text()")[i - 1]
                        movie_list.append(name)
                    else:
                        break
        print(movie_list)
        r.close()


if __name__ == '__main__':
    main('аниме')
