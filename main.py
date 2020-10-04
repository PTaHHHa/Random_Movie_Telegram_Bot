import logging
import requests
import telebot
import random
from lxml import html

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


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
    r.close()
    return movie_list


bot = telebot.TeleBot(token='xxxxxx')


def keyboard():
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    button1 = telebot.types.InlineKeyboardButton(text='Комедия', callback_data='комедия')
    button2 = telebot.types.InlineKeyboardButton(text='Драма', callback_data='драма')
    markup.add(button1, button2)
    return markup


@bot.message_handler(commands=['help'])
def fourlena(message):
    bot.send_message(message.chat.id, f'Люблю тебя, зая!')
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBawdfeiKudSVydQwlIi2NN-o67oF57AACbwYAAnlc4glk6s9UEq6DMxsE')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Здравствуй, {message.from_user.first_name}!', reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cqd = call.data
    if cqd =='комедия':
        bot.send_message(call.message.chat.id, text='Подбираю фильм')
        result = main(cqd)
        new_result = random.sample(result, 5)
        new_str = [f"{i+1}. {new_result[i]}" for i in range(len(new_result))]
        message_str = '\n'.join(new_str)
        bot.send_message(call.message.chat.id, text=f'{message_str}')
        bot.send_message(call.message.chat.id, text='Новый фильм', reply_markup=keyboard())
    elif cqd =='драма':
        bot.send_message(call.message.chat.id, text='Подбираю фильм')
        result = main(cqd)
        new_result = random.sample(result, 5)
        new_str = [f"{i + 1}. {new_result[i]}" for i in range(len(new_result))]
        message_str = '\n'.join(new_str)
        bot.send_message(call.message.chat.id, text=f'{message_str}')
        bot.send_message(call.message.chat.id, text='\nВыберите жанр', reply_markup=keyboard())
    else:
        bot.send_message(call.message.chat.id, text=f'Я тебя не знаю!')


bot.polling()

# if __name__ == '__main__':
#     main('комедия')
