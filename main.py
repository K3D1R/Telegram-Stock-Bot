#Импорт всех нужных библиотек
from email import message
import logging
import requests  #Для осуществления URL запросов
from bs4 import BeautifulSoup  #импорт библиотеки для работы с html
from config import bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

#Подключение базы данных
import sqlite3
db = sqlite3.Connection('stock.db')
cur = db.cursor()

#Машины состояний
class tickker(StatesGroup):
    tickr_cost = State()
class favorri(StatesGroup):
    favor_add = State()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
#Меню
button_favourite = KeyboardButton('/⭐Избранное')
button_currency = KeyboardButton('/💹Валюта')
button_change = KeyboardButton('/Изменить Избранное')
button_add_fav = KeyboardButton('/+Добавить_в_избранное')
button_look_fav = KeyboardButton('/Посмотреть_Избранное')
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
greet_kb.add(button_currency, button_help, button_price).add(button_ROSN, button_GAZP, button_SBER, button_favourite)
favourite_kb = ReplyKeyboardMarkup(resize_keyboard=True)
favourite_kb.add(button_add_fav,button_look_fav,back_button)

#текст ошибки
error_text = "Ошибка! Неверная ссылка/Сервер не отвечает"

#Функции
def conn_check(url):
    """Проверяет подключение"""
    headers = {
        'user agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
        }
    response = requests.get(url, headers)
    code = response.status_code
    return code

#Функия для выдачи цены.
def price_ticker(url):
        """Функцию отвечает за получения цены тикера с сайта РБК"""
        #заголовок для URL запроса, для избежания распозновия Бот-запроса
        headers = {
        'user agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
        }
        #переменная, для соххранения html разметки страницы
        try:
            if conn_check(url) == 200:
                html = requests.get(url, headers)
                #парсим теги в переменную soup
                soup = BeautifulSoup(html.content, 'html.parser')
                #поиск цены акции
                convert = soup.find('span',{'class':"chart__info__sum"})
                #формирование выдачи
                price = float(convert.text[1:].strip().replace(',','.').replace(' ',''))#можно сделать короче, но на всякий случай пусть будет так
                currency = convert.text[:1]
                currency_price = str(price)+currency
                print(f'Цена актива:{currency_price}')
                #таймер
                return currency_price
            else:
                return "Ошибка соединения" 
        except AttributeError:
            return error_text
        except requests.exceptions.MissingSchema:
            return "⚠️Неправильная ссылка⚠️"
        except requests.exceptions.InvalidURL:
            return "⚠️Неправильная ссылка⚠️"


def error_check(price, text):
    """Отвечает за корректный ответ пользователю при ошибке"""
    if price == error_text:
        return error_text
    elif price == "⚠️Неправильная ссылка⚠️":
        return price
    elif price == "⚠️Ошибка соединения!⚠️":
        return price
    else:
        return text

        
#Обработчики
@dp.message_handler(commands = ['start'])
async def send_welcome(message: types.Message):
    
    await message.bot.send_message(message.from_user.id, f"Привет, {message.from_user.username} \n Я stoсk_bot. Я помогу тебе узнать стоимость акций различных компаний", reply_markup= greet_kb)

@dp.message_handler(commands = ['🤔FAQ'])
async def help(message: types.Message):
    FAQ =(f"""Привет, {message.from_user.username}! Я - stock_bot!\n Моё назначение - давать тебе котировки ценных бумаг\n по ссылкам с сайта rbc.ru(Не реклама).
    Ты можешь создать список бумаг, за котировками которых будет удобно следить (!Тестовая функция!Работает с нареканиями)\n
    ⚠️Бот работает не совсем коректно!⚠️
    ⚠️Обрабатываются только ссылки на quote.rbc! Ввиду особенностей программы⚠️
    ⚠️Не стоит беспокоится утечки⚠️ В бд не записывается ничего кроме id (Для идентификации)\n и ссылок!
    ⚠️При удалении истории чата теряется доступ к записям в списке Избранного!⚠️
    ⚠️Проект неопытного программиста⚠️
    ⚠️В избранное можно добавить до 10 тикеров(Включительно)⚠️
    Спасибо за понимание!
    """)
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
    text = error_check(sprice, f"💹Цена акции:{sprice}🧾\n :{url}")
    await message.reply(text)
    await state.finish()

@dp.message_handler(commands= ['💹Валюта'])
async def currency_choose(message:types.Message):
    await message.reply("Выберите валюту, нажав на клавиатуру.", reply_markup=currency_kb)

@dp.message_handler(commands=['Доллар_США_＄'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59111'
    sprice = price_ticker(url)
    text = error_check(sprice, f"＄ Цена доллара:{sprice}\n :{url}")
    await message.reply(text)

@dp.message_handler(commands=['€_Евро'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59090'
    sprice = price_ticker(url)
    text = error_check(sprice, f"€ Цена евро:{sprice}\n :{url}")
    await message.reply(text)

@dp.message_handler(commands=['¥_Юань'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59066'
    sprice = price_ticker(url)
    text = error_check(sprice, f"¥ Цена юаня:{sprice}\n :{url}")
    await message.reply(text)

@dp.message_handler(commands=['🔥GAZP'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59256'
    sprice = price_ticker(url)
    text = error_check(sprice, f"🔥Цена Газпрома: {sprice}🧾\n :{url}")
    await message.reply(text)

@dp.message_handler(commands=['🛢ROSN'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59430'
    sprice = price_ticker(url)
    text = error_check(sprice, f"🛢Цена Роснефти:{sprice}🧾\n :{url}")
    await message.reply(text)

@dp.message_handler(commands=['🏦SBER'])
async def get_currency(message:types.Message):
    url = 'https://quote.rbc.ru/ticker/59762'
    sprice = price_ticker(url)
    text = error_check(sprice, f"🏦Цена Сбербанка: {sprice}🧾\n :{url}")
    await message.reply(text)


@dp.message_handler(commands= ['◀Назад'])
async def back_comm(message:types.Message):
    await message.reply("Выберите операцию", reply_markup=greet_kb)

@dp.message_handler(commands= ['con'])
async def check_conn(message:types.Message):
    if conn_check("https://quote.rbc.ru/") == 200:
        text = "Cоединение стабильно"
    else:
        text = "Соединение нестабильно"
    await message.reply(text)

@dp.message_handler(commands=['⭐Избранное'])
async def favor(message:types.Message):
    await message.reply("Выберите операцию", reply_markup=favourite_kb)
#Избранное
#Добавление в избранное
@dp.message_handler(commands=['+Добавить_в_избранное'], state = None)
async def add_fav_url_part_1(message:types.Message):
    await message.answer("Введите URL С сайта РБК")
    await favorri.favor_add.set()

@dp.message_handler(state=favorri.favor_add)
async def add_fav_url_part_2(message:types.Message, state= FSMContext):
#Получение id пользователя и url
    url = message.text
    id = message.from_user.id
    def get_urls():
        try:
            headers = {
            'user agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.3.848 Yowser/2.5 Safari/537.36"
            }
            html = requests.get(url, headers)
            cur.execute("INSERT INTO users_data(id, stock_url) VALUES(?,?)", (id, url))
            db.commit()
            return "Добавлено"
        except AttributeError:
            return error_text
        except requests.exceptions.MissingSchema:
            return "⚠️Неправильная ссылка⚠️"
        except requests.exceptions.InvalidURL:
            return "⚠️Неправильная ссылка⚠️"
    await message.reply(get_urls())
    await state.finish()
    
#Просмотр цен избранных активов
@dp.message_handler(commands = ['Посмотреть_Избранное'])
async def look_fav(message:types.Message):
    cur.execute("SELECT stock_url FROM users_data")
    stock = cur.fetchall()
    try:
        for item in stock:
            item = item[0]
            stock_price = price_ticker(item)
            await message.reply(f"{stock_price}\n"+item)
    except TypeError: 
        await message.reply("У вас нет избранных котировок!")

if __name__ == '__main__':
     executor.start_polling(dp, skip_updates=True)

cur.close()
db.close
