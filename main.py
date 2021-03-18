import requests
import json
import time
import telebot
bot = telebot.TeleBot("1675111126:AAHi4Vi8tVR31t5eu-kcAMAZBp9Zg_08E88")
def jjs():
    url="https://blockchain.info/ru/ticker"
    return requests.get(url).text

def vivod(message):
    d = json.loads(jjs())
    d2 = d[p]
    msg = bot.send_message(message.from_user.id, "Данные о BTC в валюте " + p + ":\n" + "Цена покупки: " + str(
        d2["buy"]) + "\n" + "Цена продажи: " + str(d2["sell"]), reply_markup=keyboard_cancel)
a=[0,0,0,0]
d={}
d2={}
check=0
p=p1=0
dbuy=0
keyboard_input_action=telebot.types.ReplyKeyboardMarkup(True,True)
keyboard_input_action.row("Вывести курс BTC в валюте")
keyboard_input_action.row("Выводить курс BTC по времени")
keyboard_input_action.row("Проверка изменения курса с последнего запроса")

keyboard_input_currency=telebot.types.ReplyKeyboardMarkup(True,True)
keyboard_input_currency.row("USD","AUD","BRL","CAD")
keyboard_input_currency.row("CHF","CLP","CNY","DKK")
keyboard_input_currency.row("EUR","GBP","HKD","INR")
keyboard_input_currency.row("ISK","JPY","KRW","NZD")
keyboard_input_currency.row("PLN","RUB","SEK","SGD")
keyboard_input_currency.row("THB","TRY","TWD")

keyboard3=telebot.types.ReplyKeyboardMarkup(True,True)
keyboard3.row("Изменить валюту")
keyboard3.row("Обновить данные")
keyboard3.row("Назад")

keyboard_cancel=telebot.types.ReplyKeyboardMarkup(True,True)
keyboard_cancel.row("Остановить вывод")

@bot.message_handler(commands=["start"])
def start(message):
    global check
    global p
    check=0
    p=0
    msg=bot.send_message(message.from_user.id,"Выберите действие:",reply_markup=keyboard_input_action)
    bot.register_next_step_handler(msg,obr)

@bot.message_handler(content_types=["text"])
def obr(message):
    if message.text=="Вывести курс BTC в валюте":
        get_text_messages(message)
    elif message.text=="Выводить курс BTC по времени":
        global check,p
        p=0
        check=1
        get_text_messages(message)
    elif message.text=="Проверка изменения курса с последнего запроса":
        check_changes(message)

def obr2(message):
    if message.text=="Изменить валюту":
        get_text_messages(message)
    elif message.text=="Обновить данные":
        viv(message)
    else:
        start(message)

def check_changes(message):
    if p1==0:
        print("Нет данных о последнем запросе")
    else:
        d = json.loads(jjs())
        d2 = d[p1]
        if d2["buy"]==dbuy:
            msg=bot.send_message(message.from_user.id, "Данные о BTC в валюте " + p1 + ":\n\n" + "Курс не изменился"+"\n"+ "Цена: " + str(
                d2["buy"]),reply_markup=keyboard_input_action)
            bot.register_next_step_handler(msg, obr)

        else:
            msg=bot.send_message(message.from_user.id,
                             "Данные о BTC в валюте " + p1 + ":\n\n" + "Курс изменился" + "\n" + "Предыдущая цена: " + str(
                                 dbuy)+"\n"+"Актуальная цена: "+str(d2["buy"]),reply_markup=keyboard_input_action)
            bot.register_next_step_handler(msg, obr)
def get_text_messages(message):
    msg=bot.send_message(message.from_user.id, "Выберите валюту:",reply_markup=keyboard_input_currency)
    if check==1:
        bot.register_next_step_handler(msg,viv2)
    else:
        bot.register_next_step_handler(msg, viv)

def viv(message):
    global p,p1
    global check
    global dbuy
    d=json.loads(jjs())
    if len(message.text) == 3:
        p =p1 = message.text
    d2=d[p]
    dbuy=d2["buy"]
    msg=bot.send_message(message.from_user.id, "Данные о BTC в валюте "+p+":\n"+"Цена покупки: "+str(d2["buy"])+"\n"+"Цена продажи: "+str(d2["sell"]),reply_markup=keyboard3)
    bot.register_next_step_handler(msg, obr2)

def viv2(message):
    global p,p1
    global check
    global dbuy
    if len(message.text) == 3:
        p = message.text
    d = json.loads(jjs())
    d2 = d[p]
    dbuy = d2["buy"]
    msg=bot.send_message(message.from_user.id, "Данные о BTC в валюте " + p + ":\n" + "Цена покупки: " + str(
        d2["buy"]) + "\n" + "Цена продажи: " + str(d2["sell"]),reply_markup=keyboard_cancel)
    viv21(message)


def viv21(message):
    if message.text!="Остановить вывод":
        time.sleep(5)
        viv2(message)
    else:
        start(message)

bot.polling()