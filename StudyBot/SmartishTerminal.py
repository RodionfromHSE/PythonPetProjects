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


def start():
    print(f"""
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


def add(args):
    try:
        splitMsg = args[0].split(',')

        obj = Object(*splitMsg, dt.date.today())

        db.addObject(obj, INFO['INITIAL_LEVEL'])
        db.saveChanges()

        print(f"Hey! It's added successfully. \n{obj}")
    except Exception as e:
        print(f"Sorry, args format is incorrect:\n{e}")


def addPlus(args):
    try:
        names = args[0].split(' + ')

        addedObjs = list()
        for name in names:
            obj = Object(name=name, repDate=dt.date.today())
            db.addObject(obj, INFO['INITIAL_LEVEL'])
            addedObjs.append(obj)

        db.saveChanges()
        print(f"Hey! It's added successfully. \n{addedObjs}")
    except Exception as e:
        print(f"Sorry, args format is incorrect:\n{e}")


def getToday():
    objs = db.getObjectsByDate(dt.date.today())
    print(objs)
    print(db.getAllObjectsOnLevel(1))
    info = '\n\n\n'.join(sorted(map(str, objs), reverse=True))
    if not info:
        print("Good news: Nothing new today!")
    else:
        print(info)


def makeShifts():
    db.makeShifts()
    db.saveChanges()
    print("Shifts are done!")


def makeShiftsFrom(args):
    try:
        date_str = args[0].strip()
        start_date = dt.datetime.strptime(date_str, "%d.%m")
        start_date = start_date.replace(year=2023).date()
        db.makeShiftsFrom(start_date)
        db.saveChanges()
        print(f"Hey! It's shifted successfully.")
    except Exception as e:
        print(f"Sorry, args format is incorrect:\n{e}")


def view():
    view_str = str()
    for level in range(INFO['LEVELS_AMOUNT']):
        level_objs = db.getAllObjectsOnLevel(level)
        view_str += f'\n\n----------------- __LEVEL {level + 1}__ --------------------\n\n'
        view_str += ', \n'.join(map(str, level_objs))

    print(view_str)


def temp():
    print("""En:    

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


def close():
    print("Have a nice day!")
    sys.exit()




def handle_input(input_str):
    command, *args = input_str.split(': ')
    if command == "start":
        start()
    elif command == "add":
        add(args)
    elif command == "addPlus":
        addPlus(args)
    elif command == "getToday":
        getToday()
    elif command == "makeShifts":
        makeShifts()
    elif command == "makeShiftsFrom":
        makeShiftsFrom(args)
    elif command == "view":
        view()
    elif command == "temp":
        temp()
    else:
        print("Invalid command")

while True:
    user_input = input("Enter command: ")
    handle_input(user_input)
