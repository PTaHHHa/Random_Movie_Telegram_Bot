TODO: """РЕАЛИЗОВАТЬ САМОГО БОТА"""
import logging
import requests
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from lxml import html

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


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


def start(update, context):
    keyboard = [[InlineKeyboardButton("Option 1", callback_data='1'),
                 InlineKeyboardButton("Option 2", callback_data='2')],

                [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))


def help_command(update, context):
    update.message.reply_text("Use /start to test this bot.")


updater = Updater(token='xxxx', use_context=True)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('help', help_command))
updater.start_polling()
updater.idle()


# if __name__ == '__main__':
#     main('комедия')
