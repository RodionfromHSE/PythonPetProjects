import sys

from Data import Object
from DataBase import Database
import datetime as dt
from Data import INFO
from json import load

db = Database()



def start():
    print(f"""
Hello, I'm smartish!

Example:
addPlus: item1 + item2 + item3...

getToday - get what to repeat today

makeShifts - shift all that you need to repeat today as you've repeated it

makeShiftsFrom: 12.10
""")



def reformatArgs(args):
    """
    Convert arguments from ['arg1', 'arg2', 'arg3'] to ['arg1 YesterdayDate', 'arg2 YesterdayDate', 'arg3 YesterdayDate']
    :param args: list of strings
    :return: list of strings
    """
    yesterday = dt.date.today() - dt.timedelta(days=1)
    yesterday = yesterday.strftime("%d.%m")
    return [f"{arg} {yesterday}" for arg in args]

def addPlus(args, reformat=True):
    try:
        names = args[0].split(' + ')
        if reformat:
            names = reformatArgs(names)
        addedObjs = list()
        for name in names:
            obj = Object(name=name, repDate=dt.date.today())
            db.addObject(obj, INFO['INITIAL_LEVEL'])
            addedObjs.append(obj)

        db.saveChanges()
        print(f"Hey! It's added successfully. \n")
        for obj in addedObjs:
            print(obj)
    except Exception as e:
        print(f"Sorry, args format is incorrect:\n{e}")

# def push(args):
#     try:
#         args = args.strip()
#         if len(args.)
#         obj = Object(name=name, repDate=dt.date.today())
#         db.addObject(obj, INFO['INITIAL_LEVEL'])
#         db.saveChanges()
#         print(f"Hey! It's added successfully. \n")
#         print(obj)
#     except Exception as e:
#         print(f"Sorry, args format is incorrect:\n{e}"


def getToday():
    objs = db.getObjectsByDate(dt.date.today())
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
        addPlus(args, reformat=False)
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
    elif command == "close":
        close()
    elif command == "start":
        start()
    else:
        print("Invalid command")

while True:
    user_input = input("Enter command: ")
    handle_input(user_input)

