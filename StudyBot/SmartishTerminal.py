import sys
import os

from Data import Object
from DataBase import Database
import datetime as dt
from Data import INFO
from json import load

db = Database()
FREEZE_META_PATH = os.path.join(os.path.dirname(__file__), 'freeze_meta.json')


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


def getNotRepeated(daysRange=31):
    objs = []
    today = dt.date.today()
    for date in range(daysRange):
        date = today - dt.timedelta(days=date)
        objs.extend(db.getObjectsByDate(date))
    info = '\n\n\n'.join(sorted(map(str, objs), reverse=True))
    if not info:
        print(f"Good news: Nothing new for last {daysRange} days!")
    else:
        print(info)


def get(args=None):
    data = args[0] if args else None
    if isinstance(data, str):
        data = dt.datetime.strptime(data, "%d.%m").date()
        # replace year to current year
        cur_year = dt.date.today().year
        data = data.replace(year=cur_year)
    elif not data:
        data = dt.date.today()
    objs = db.getObjectsByDate(data)
    info = '\n\n\n'.join(sorted(map(str, objs), reverse=True))
    if not info:
        print("Good news: Nothing new for the selected day!")
    else:
        print(info)

def remove(args):
    try:
        name = args[0].strip()
        db.deleteByName(name)
        db.saveChanges()
        print(f"Hey! It's removed successfully.")
    except Exception as e:
        print(f"Sorry, args format is incorrect:\n{e}")

def makeShiftsNotRepeated(daysRange=31, from_today=False):
    """Shift all not repeated objects from the last daysRange days.
    If from_today is True, then shift them as if they were repeated today.
    Otherwise, shift them as if they were repeated on the day they should be repeated.
    """
    start_date = dt.date.today() - dt.timedelta(days=daysRange)
    end_date = dt.date.today() + dt.timedelta(days=1)
    db.makeShiftsRange(start_date, end_date, from_today=from_today)
    db.saveChanges()
    print(f"Hey! It's shifted successfully.")

def makeShifts():
    db.makeShifts()
    db.saveChanges()
    print("Shifts are done!")


def makeShiftsFrom(args):
    try:
        date_str = args[0].strip()
        start_date = dt.datetime.strptime(date_str, "%d.%m")
        start_date = start_date.replace(year=2023).date()
        db.makeShiftsRange(start_date)
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

def freeze():
    """Freeze the current state of the database. Save date of the freeze."""
    today = dt.date.today()
    meta = today.strftime("%d.%m.%Y")
    with open(FREEZE_META_PATH, 'w') as f:
        f.write(meta)
    
    print(f"Database is frozen on {today}")

def unfreeze():
    """Unfreeze the database. Load the date of the freeze, shift all objects from that date to today, clear the freeze date."""
    if not os.path.exists(FREEZE_META_PATH):
        print("Database is not frozen.")
        return
    
    with open(FREEZE_META_PATH, 'r') as f:
        meta = f.read().strip()
    os.remove(FREEZE_META_PATH)
    
    freeze_date = dt.datetime.strptime(meta, "%d.%m.%Y").date()
    today = dt.date.today()
    n_days_passed = (today - freeze_date).days
    print(f"Database is unfrozen. {n_days_passed} days passed since the freeze date ({freeze_date}).")
    db.calenderShift(n_days_passed)


def close():
    global db
    print("Have a nice day!")
    del db
    sys.exit(0)




def handle_input(input_str):
    command, *args = input_str.split(': ')
    if command == "add":
        addPlus(args, reformat=False)
    elif command == "addPlus":
        addPlus(args)
    elif command == "getToday":
        get()
    elif command == "get":
        get(args)
    elif command == "getAll":
        getNotRepeated()
    elif command == "makeShifts":
        makeShifts()
    elif command == "makeShiftsFrom":
        makeShiftsFrom(args)
    elif command == "makeShiftsAll":
        makeShiftsNotRepeated()
    elif command == "makeShiftsAllFromToday":
        makeShiftsNotRepeated(from_today=True)
    elif command == "view":
        view()
    elif command == "remove":
        remove(args)
    elif command == "close":
        close()
    elif command == "freeze":
        freeze()
    elif command == "unfreeze":
        unfreeze()
    else:
        print("Invalid command")

while True:
    user_input = input("Enter command: ")
    handle_input(user_input)

