from telethon import TelegramClient, events
import random
import requests
import json
import time
import os
import logging
from os import environ

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

api_id = environ.get('API_ID')

api_hash = environ.get('API_HASH')

bot_token = environ.get('BOT_TOKEN')

bot = TelegramClient('session_name', api_id, api_hash)

places = ['Корейцы', 'Сербы', 'Лукоморье', 'Чикаго', 'Розенбаум', 'Шавуха', 'Вьетнам', 'Вилка', 'Барвинок']

lunch_gif = ['https://media.giphy.com/media/7e3Y9b3nTWsaA/giphy.gif',
             'https://media.giphy.com/media/jKaFXbKyZFja0/giphy.gif',
             'https://media.giphy.com/media/FgNmKgaqixS3m/giphy.gif',
             'https://media.giphy.com/media/PS1Ko2AFVTso8/giphy.gif',
             'https://media.giphy.com/media/Cx2qDJYjwq1ji/giphy.gif',
             'https://media.giphy.com/media/eH3Ra3DUp3tMylXedo/giphy.gif',
             'https://media.giphy.com/media/h8uD16sumSaRi/giphy.gif',
             'https://media.giphy.com/media/APJ8aylgEPfzy/giphy.gif',
             'https://media.giphy.com/media/WKUSlerPGZ73i/giphy.gif',
             'https://media.giphy.com/media/xThuWcu8nwBhazm0Fi/giphy.gif',
             'https://media.giphy.com/media/lYRFF6Voh4brq/giphy.gif',
             'https://media.giphy.com/media/rVhabuN8Ww2NW/giphy.gif']

commands = 'Доступные команды:\n' + '\n'.join(['/lunch - Колесо фортуны',
                                               '/list - Куда ходим',
                                               '/poll - Народовластие',
                                               '/hell - Вы действительно хотите знать?',
                                               '/ping - Пациент скорее жив, чем мертв'])

logger.info('bot data is up')


def get_random_gif():
    return random.choice(lunch_gif)


def get_random_lunch_place():
    return random.choice(places)


def get_random_lunch_places():
    random_places = []
    while True:
        if len(random_places) < 4:
            item = random.choice(places)
            if item not in random_places:
                random_places.append(item)
        else:
            break
    return random_places


@bot.on(events.NewMessage(pattern='/lunch'))
async def my_event_handler(event):
    print(event.chat_id)
    await bot.send_file(event.chat_id, get_random_gif())
    time.sleep(1)
    await bot.send_message(event.chat_id, 'Никаких голосований, все решаю я!')
    time.sleep(1)
    place = get_random_lunch_place()
    await bot.send_message(event.chat_id, 'Вот куда идем сегодня: ' + place)
    # await bot.send_file(event.chat_id, place_gif[place])


@bot.on(events.NewMessage(pattern='/list'))
async def list_request_handler(event):
    await bot.send_message(event.chat_id, 'Вот, что у меня есть:\n' + '\n'.join(places))


@bot.on(events.NewMessage(pattern='/poll'))
async def launch_poll(event):
    logger.info('launching poll')
    random_places = get_random_lunch_places()
    url = 'https://api.telegram.org/bot%s/sendPoll' % bot_token
    payload = {'chat_id': event.chat_id, 'question': 'Куда?', 'options': random_places}
    r = requests.post(url, data=json.dumps(payload), headers={'Content-type': 'application/json'})
    logger.info('status code: %d' % r.status_code)
    logger.info(r.text)
    await bot.send_message(event.chat_id, 'Голосуем!')
    await bot.send_file(event.chat_id, get_random_gif())


@bot.on(events.NewMessage(pattern='/hell'))
async def tram_place_message(event):
    await bot.send_file(event.chat_id, 'https://media.giphy.com/media/n0pwZRRYfLv7q/giphy.gif')
    await bot.send_message(event.chat_id, 'Трамвайка')


@bot.on(events.NewMessage(pattern='/info'))
async def send_info(event):
    await bot.send_message(event.chat_id, commands)


@bot.on(events.NewMessage(pattern='/ping'))
async def ping(event):
    await bot.send_message(event.chat_id, 'Рано вы меня хороните')

logger.info('start')

bot.start(bot_token=bot_token)


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
