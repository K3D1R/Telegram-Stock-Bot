import logging
from parsr import price, update_ticker
import emoji

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
#bot's token
API_TOKEN = ''#Bot's token here

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
    await message.reply(f"Цена акций SBERP:{price}₽\nSBERP:https://quote.rbc.ru/ticker/59763")


if __name__ == '__main__':
     executor.start_polling(dp, skip_updates=True)


    
