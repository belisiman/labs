import logging
import telebot
from py_bing_search import PyBingImageSearch

bot = telebot.TeleBot('275994346:AAEYbr6J1JqBVIE7eg1h3Jy_X_zPo39FJ2w')
BingKey = "0uZ5Rifm4B3PxJM2P5tCAq0O+PglqlVbylG+2PiUP/M"


@bot.message_handler(commands=['start'])
def SendInfo(messege):


    bot.send_message(messege.chat.id, 'Привет! я твой бот. Введи запрос для поиска изображения:')


@bot.message_handler(commands=['help'])
def SendHelp(messege):


    bot.send_message(messege.chat.id, "Список доступных коммад: /start, /about ")


@bot.message_handler(content_types='text')
def SendMessage(message):
    bot.send_message(message.chat.id, "Ожидайте, мы ищем для Вас картиночки!")
    bing_image = PyBingImageSearch(BingKey, str(message.text))
    result = bing_image.search(limit=5, format='json')
    for image in result:
        bot.send_message(message.chat.id, 'Фото:')
        bot.send_photo(message.chat.id, image.media_url)

# Сконфигурируем Log-файл
logging.basicConfig(filename='botLog.log',
                    format='%(filename)s[LINE:%(lineno)d]# '
                           '%(levelname)-8s [%(asctime)s] ',
                    level=logging.DEBUG)

logging.info('Start the bot.')

try:
    bot.polling(none_stop=True)
except Exception:
    logging.critical('ERROR...')
finally:
    bot.polling(none_stop=True)
