#Импорт всех нужных библиотек
from audioop import add
import logging
from turtle import update
from aiohttp import request
from matplotlib import ticker
import requests  #Для осуществления URL запросов
from bs4 import BeautifulSoup  #импорт библиотеки для работы с html


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

class tickker(StatesGroup):
    tickr_cost = State()
#bot's token
API_TOKEN = ''

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
#Меню
button_currnecy = KeyboardButton('/💹Валюта')
#Валюта
button_rubble_dollar_usa = KeyboardButton('/Доллар_США_＄')
button_rubble_euro = KeyboardButton('/€_Евро')
button_rubble_yan = KeyboardButton('/¥_Юань')
back_button = KeyboardButton('/◀Назад')
#Мини меню
button_help = KeyboardButton('/🤔FAQ')
button_price = KeyboardButton('/Цена_акции🧾')
#Быстрые акции
button_GAZP = KeyboardButton('/🔥GAZP')
button_SBER = KeyboardButton('/🏦SBER')
button_ROSN = KeyboardButton('/🛢ROSN')
# клавиатуры
currency_kb = ReplyKeyboardMarkup(resize_keyboard=True)
currency_kb.add(button_rubble_dollar_usa, button_rubble_euro, button_rubble_yan, back_button)
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_currnecy, button_help, button_price).add(button_ROSN, button_GAZP, button_SBER)

#Функия для выдачи цены.
def price_ticker(url):

        #заголовок для URL запроса, для избежания распозновия Бот-запроса
        headers = {
        'user agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
        }

        #переменная, для соххранения html разметки страницы
        html = requests.get(url, headers)

        #парсим теги в переменную soup
        soup = BeautifulSoup(html.content, 'html.parser')
        #поиск цены акции
        convert = soup.find('span',{'class':"chart__info__sum"})
        #формирование выдачи
        price = float(convert.text[1:].strip().replace(',','.').replace(' ',''))#можно сделать короче, но на всякий случай пусть будет так
        currency = convert.text[:1]
        currency_price = str(price)+currency
        print(f'Цена евро:{currency_price}')
        #таймер
        return currency_price

#Обработчики
@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    await message.bot.send_message(message.from_user.id, "Привет \n Я stoсk_bot. Я помогу тебе узнать стоимость акций различных компаний", reply_markup= greet_kb)
    
@dp.message_handler(commands = ['🤔FAQ'])
async def help(message: types.Message):
    FAQ =(f"FAQ\n {u'⚠'} К сожалению поддерживаются только ссылки с сайта РБК"
    "\n ⚠ Бот работает не совсем стабильно"
    "\n ⚠ Цены акций берутся с сайта РБК:\n https://quote.rbc.ru/")
    await message.reply(FAQ)

#реакция на команду выдача цены актива
@dp.message_handler(commands = ['Цена_акции🧾'], state = None)
async def getURL_part1(message: types.Message):
    await message.reply("Вставь ссылку на акцию с сайта РБК")
    await tickker.tickr_cost.set()

@dp.message_handler(state = tickker.tickr_cost)
async def ticker_url(message:types.Message, state:FSMContext):
    url = message.text
    sprice = price_ticker(url)
    await message.reply(f"💹Цена акции:{sprice}🧾\n :{url}")
    await state.finish()

@dp.message_handler(commands= ['💹Валюта'])
async def currency_choose(message:types.Message):
    await message.reply("Выберите валюту, нажав на клавиатуру.", reply_markup=currency_kb)
@dp.message_handler(commands=['Доллар_США_＄'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59111'
    sprice = price_ticker(url)
    await message.reply(f"＄ Цена доллара:{sprice}\n :{url}")

@dp.message_handler(commands=['€_Евро'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59090'
    sprice = price_ticker(url)
    await message.reply(f"€ Цена евро:{sprice}\n :{url}")

@dp.message_handler(commands=['¥_Юань'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59066'
    sprice = price_ticker(url)
    await message.reply(f"¥ Цена юаня:{sprice}\n :{url}")

@dp.message_handler(commands=['🔥GAZP'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59256'
    sprice = price_ticker(url)
    await message.reply(f"💹Цена Газпрома: {sprice}🧾\n :{url}")

@dp.message_handler(commands=['🛢ROSN'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59430'
    sprice = price_ticker(url)
    await message.reply(f"🛢Цена Роснефти:{sprice}🧾\n :{url}")

@dp.message_handler(commands=['🏦SBER'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59762'
    sprice = price_ticker(url)
    await message.reply(f"🏦Цена Сбербанка: {sprice}🧾\n :{url}")


@dp.message_handler(commands= ['◀Назад'])
async def back(message:types.Message):
    await message.reply("Выберите операцию", reply_markup=greet_kb)

if __name__ == '__main__':
     executor.start_polling(dp, skip_updates=True)
