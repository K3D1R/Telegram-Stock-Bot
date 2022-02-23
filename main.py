import logging
import emoji

from turtle import update
from aiohttp import request
import requests #Для осуществления URL запросов
from bs4 import BeautifulSoup # импорт библиотеки для работы с html
import time # импорт библиотеки для установки задержки

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
#bot's token
API_TOKEN = '5166586300:AAEExuhGbEUQdam4AHnIXaay7BgYwzcruh8'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

button_help = KeyboardButton('/FAQ')
button_price = KeyboardButton('/Цена_акции')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_help, button_price)

@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет \n Я stok_bot. Я помогу тебе узнать стоимость акции SBERP", reply_markup= greet_kb)

@dp.message_handler(commands = ['FAQ'])
async def help(message: types.Message):
    FAQ =("FAQ\n  К сожалению сейчас отслеживаются только привилегированные акции Cбербанка(SBERP)"
    "\n  Бот работает не совсем стабильно"
    "\n  Цены акций берутся с сайта РБК:\n https://quote.rbc.ru/ticker/59763 ")
    await message.reply(FAQ)

@dp.message_handler(commands = ['Цена_акции'])
async def getprice(message: types.Message):
    def price_ticker():
        #Ссылка на актив
        SBERP = "https://quote.rbc.ru/ticker/59763"

        #заголовок для URL запроса, для избежания распозновия Бот-запроса
        headers = {
        'user agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
        }

        #переменная, для соххранения html разметки страницы
        html = requests.get(SBERP, headers)

        #парсим теги в переменную soup
        soup =BeautifulSoup(html.content, 'html.parser')
        #поиск цены акции
        convert = soup.find('span',{'class':"chart__info__sum"})
        #формирование выдачи
        price = float(convert.text[1:].strip().replace(',','.'))
        currency = convert.text[:1]
        stock_price = str(price)+currency
        print(f'Цена акции SBERP:{stock_price}')
    
        return stock_price
    price = price_ticker()
    await message.reply(f"Цена акций SBERP:{price}\nSBERP:https://quote.rbc.ru/ticker/59763")


if __name__ == '__main__':
     executor.start_polling(dp, skip_updates=True)


    