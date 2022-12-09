import telebot
import random
from random import randint
from telebot import types
import requests
import pandas as pd 
import xml.etree.ElementTree as et 
import datetime
 
bot = telebot.TeleBot('5581979231:AAE7akSwOPfPiGmcn-6iQ0TShwfgx2KQSPE')


 
def pogyandex( ):
    # Адрес api метода для запроса get
    url = 'https://api.weather.yandex.ru/v2/forecast/'
    param = {
    "lat":53.5303,   # широта
    "lon":49.3461,   # долгота
    "lang":"ru_RU"
    }
 
    # Отправляем get request (запрос GET)
    response = requests.get(url, headers={'X-Yandex-API-Key':'6cb65e42-b402-4565-a7fa-61c961c06adc'},params=param)
    data1 = response.json()
 
    d1 = {
    "str":data1['geo_object']['country']['name'],
    "obl":data1['geo_object']['province']['name'],
    "gor":data1['geo_object']['locality']['name'],
    
    "temp":data1['fact']['temp'],
    "feels":data1['fact']['feels_like'],
    "speed":data1['fact']['wind_speed'],
    "pressure":data1['fact']['pressure_mm'],
    "humidity":data1['fact']['humidity'],
    "uv":data1['fact']['uv_index'],

    "sunrise":data1['forecasts'][0]['sunrise'],
    "sunset":data1['forecasts'][0]['sunset']

    }
   
    return d1

 
def val1( v_date):
    # Адрес api метода для запроса get
    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    params = {
        'date_req': v_date
    }
    # Отправляем get request (запрос GET)
    response = requests.get(url, params)
    tree = et.ElementTree(et.fromstring(response.text))
    root = tree.getroot()
    df_cols = ["date", "numcode", "nominal", "name", "value"]
    rows = []
    for node in root:
        s_numcode = node.find("NumCode").text if node is not None else None
        s_charcode = node.find("CharCode").text if node is not None else None
        s_nominal = node.find("Nominal").text if node is not None else None
        s_name = node.find("Name").text if node is not None else None
        s_value = node.find("Value").text if node is not None else None
    
    
        rows.append({"date": v_date, "numcode": s_numcode,
                 "nominal": s_nominal,
                 "name": s_name, "value": s_value})

    df = pd.DataFrame(rows, columns = df_cols)
    #-------изменение реквизитов DataFrame
    df.loc[(df['name'] =='Фунт стерлингов Соединенного королевства'), 'name'] = 'Фунт стерлингов'
    df.loc[(df['name'] =='СДР (специальные права заимствования)'), 'name'] = 'СДР'
 
    li = ['840' ,'978', '826','156','392']
    df=df[df.numcode.isin(li)]

    return df
    
    
 
 
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
  if message.text == "Start":
       
        # Готовим кнопки
        keyboard = types.InlineKeyboardMarkup()
        # По очереди готовим текст и обработчик для курса валют
        key_kurs = types.InlineKeyboardButton(text='Курсы валют ЦБ РФ', callback_data='kurs1')
        # И добавляем кнопку на экран
        keyboard.add(key_kurs)
        key_pog = types.InlineKeyboardButton(text='Погода в Тольятти', callback_data='pog1')
        keyboard.add(key_pog)
        # Показываем все кнопки сразу и пишем сообщение о выборе
        bot.send_message(message.from_user.id, text='Сделайте выбор', reply_markup=keyboard)
  elif message.text == "/help":
      bot.send_message(message.from_user.id, "Напиши Start")
  else:
      bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
        
 
# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
  dt=datetime.datetime.now().strftime("%d.%m.%Y")  #текущая дата день месяц год
  # Если нажали на кнопку, выводим информацию
  if call.data == "pog1": 
    s4=pogyandex()


    msg='Местоположение:  '+s4['str'] + ',  ' + s4['obl'] + ',  ' + s4['gor']+ '\nПрогноз погоды на ' + dt+ '\nТемпература :  ' + str(s4['temp']) + '°C,  ощущается как  ' +str(s4['feels']) + '°C\nСкорость ветра достигает: ' +str(s4['speed'])+' м/с,  давление: ' +str(s4['pressure'])+' мм рт.ст.,  влажность воздуха: ' +str(s4['humidity'])+'%, УФ-индекс: ' +str(s4['uv'])  +',  восход солнца: ' +str(s4['sunrise'])+',  заход солнца: ' +str(s4['sunset'])
 
    
    # Отправляем текст в Телеграм
    bot.send_message(call.message.chat.id, msg)
  if call.data == "kurs1": 
    # Формируем текущую дату
    dt=datetime.datetime.now().strftime("%d.%m.%Y")
    dk= val1(dt)
    


    msg=dk.to_string()
    bot.send_message(call.message.chat.id, msg)

 
bot.polling(none_stop=True, interval=0)