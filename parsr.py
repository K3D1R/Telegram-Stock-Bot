#импорт всех нужных библиотек


from turtle import update
from aiohttp import request
import requests #Для осуществления URL запросов
from bs4 import BeautifulSoup # импорт библиотеки для работы с html
import time # импорт библиотеки для установки задержки

sleep = 4 #задержка

price = 0
def update_ticker():
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

    convert = soup.find('span',{'class':"chart__info__sum"})

    price = float(convert.text[1:].strip().replace(',','.'))

    print(f'Цена акции SBERP:{price}')

    time.sleep(sleep)
    return price
    

price = update_ticker()
print(price)

