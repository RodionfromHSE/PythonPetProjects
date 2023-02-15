import telebot
import sys

from Data import Object
from DataBase import Database
import datetime as dt
from Data import INFO
from json import load

credentials_path = r"C:\Users\home\Desktop\Programming\Python Project\PythonPetProjects\StudyBot\credentials.json"
with open(credentials_path, "r") as f:
    API_KEY = load(f)['API_KEY']
bot = telebot.TeleBot(API_KEY)
db = Database()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"""
Hello, I'm smartish!
/add - add new item to LS (Leitner system)
Example:
/add 
nameOfItem,linkToTheItem

/addPlus - add new *items* to LS (Leitner system)
Example:
/addPlus
item1 + item2 + item3...

/getToday - get what to repeat today 

/makeShifts - shift all that you need to repeat today as you've repeated it

/temp - template

/makeShiftsFrom
12.10
""")


@bot.message_handler(commands=['add'])
def add(message):
    try:
        splitMsg = message.text.split('\n')[1].split(',')

        obj = Object(*splitMsg, dt.date.today())

        db.addObject(obj, INFO['INITIAL_LEVEL'])
        db.saveChanges()

        bot.reply_to(message, f"Hey! It's added successfully. \n{obj}")
    except Exception as e:
        bot.reply_to(message, f"Sorry, message format is incorrect:\n{e}")


@bot.message_handler(commands=['addPlus'])
def addPlus(message):
    try:
        names = message.text.split('\n')[1].split(' + ')

        addedObjs = list()
        for name in names:
            obj = Object(name=name, repDate=dt.date.today())
            db.addObject(obj, INFO['INITIAL_LEVEL'])
            addedObjs.append(obj)

        db.saveChanges()
        bot.reply_to(message, f"Hey! It's added successfully. \n{addedObjs}")
    except Exception as e:
        bot.reply_to(message, f"Sorry, message format is incorrect:\n{e}")


@bot.message_handler(commands=['getToday'])
def getToday(message):
    objs = db.getObjectsByDate(dt.date.today())
    print(objs)
    print(db.getAllObjectsOnLevel(1))
    info = '\n\n\n'.join(sorted(map(str, objs), reverse=True))
    bot.send_message(message.chat.id, "Good news: Nothing new today!" if not info else info, parse_mode="Markdown")


@bot.message_handler(commands=['makeShifts'])
def makeShifts(message):
    db.makeShifts()
    db.saveChanges()
    bot.reply_to(message, "Shifts are done!")


@bot.message_handler(commands=['makeShiftsFrom'])
def makeShiftsFrom(message):
    try:
        date_str = message.text.split('\n')[1].strip()
        start_date = dt.datetime.strptime(date_str, "%d.%m")
        start_date = start_date.replace(year=2022).date()
        db.makeShiftsFrom(start_date)
        db.saveChanges()
        bot.reply_to(message, f"Hey! It's shifted successfully.")
    except Exception as e:
        bot.reply_to(message, f"Sorry, message format is incorrect:\n{e}")


@bot.message_handler(commands=['view'])
def view(message):
    view_str = str()
    for level in range(INFO['LEVELS_AMOUNT']):
        level_objs = db.getAllObjectsOnLevel(level)
        view_str += f'\n\n----------------- __LEVEL {level + 1}__ --------------------\n\n'
        view_str += ', \n'.join(map(str, level_objs))

    bot.reply_to(message, view_str, parse_mode="Markdown")


@bot.message_handler(commands=['temp'])
def temp(message):
    bot.reply_to(message, """En:    

Deutsch:   

*:   

OS:   

MA:    

ML:     

Kt:     

FP:   

SQL:    

MS:     

AC:

Ch:

""")


@bot.message_handler(commands=['close'])
def close(message):
    bot.reply_to(message, "Have a nice day!")
    sys.exit()


# def greetings_check(message):
#     msg = message.text.split()
#     return len(msg) >= 2 and msg[0] == "Hi"
#
#
# @bot.message_handler(func=greetings_check)
# def sayHello(message):
#     msg = message.text.split()
#     bot.reply_to(message, f"Hello {msg[1]}")


bot.polling()
