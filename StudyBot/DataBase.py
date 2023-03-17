import sqlite3 as sq
from Data import *
import sys

DB_NAME = r"/home/rodion/Desktop/Programming/Python/PythonPetProjects/StudyBot/leitner_base.db"


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


class Database:
    def __init__(self, DBName=DB_NAME):
        self._con = sq.connect(DBName, check_same_thread=False)
        self._cursor = self._con.cursor()
        self.createLevelsIfNeeded()

    def createLevelsIfNeeded(self):
        # Can we create table of class that we have?
        for i in range(INFO['LEVELS_AMOUNT']):
            self._cursor.execute(f"""CREATE TABLE IF NOT EXISTS level{i}(objName text, link text, date text)""")

    def addObject(self, object, level):
        self._cursor.execute(
            f"""INSERT INTO level{level} VALUES('{object.name}', '{object.link}', '{object.repDate}')""")

    def deleteByName(self, name, level):
        self._cursor.execute(f"DELETE FROM level{level} WHERE objName=(?)", (name,))

    def getObjectsByDateAndLevel(self, date, level):
        self._cursor.execute(f"""SELECT * FROM level{level} WHERE date = '{date}'""")
        return [Object.fromTuple(triple) for triple in self._cursor.fetchall()]

    def extractObjectsByDateAndLevel(self, date, level):
        self._cursor.execute(f"""SELECT * FROM level{level} WHERE date = '{date}'""")
        objs = [Object.fromTuple(triple) for triple in self._cursor.fetchall()]
        self._cursor.execute(f"DELETE FROM level{level} WHERE date=(?)", (date,))
        return objs

    def getObjectsByDate(self, date):
        objs = list()
        for i in range(INFO['LEVELS_AMOUNT']):
            objs += self.getObjectsByDateAndLevel(date, i)
        return objs

    def makeShifts(self, day=dt.date.today()):
        for level in range(INFO['LEVELS_AMOUNT']):
            objs = self.extractObjectsByDateAndLevel(day, level)
            if level == INFO['LEVELS_AMOUNT'] - 1:
                break
            for obj in objs:
                obj.shiftDate(INFO['SHIFTS'][level])
                self.addObject(obj, level + 1)

    def makeShiftsFrom(self, start_date):
        today = dt.date.today()
        for day in daterange(start_date, today):
            self.makeShifts(day)

    def getAllObjectsOnLevel(self, level):
        self._cursor.execute(f"""SELECT * FROM level{level}""")
        return [Object.fromTuple(triple) for triple in self._cursor.fetchall()]

    def saveChanges(self):
        self._con.commit()

    def __del__(self):
        self.saveChanges()
        self._cursor.close()


def DBfromInput():
    db = Database()
    levels = list()
    pairsNamesDate = list()
    for line in map(str.rstrip, sys.stdin):
        if not line:
            continue
        if line == '--':
            levels.append(pairsNamesDate.copy())
            pairsNamesDate.clear()
            continue

        pair = line.split('-')

        names = pair[0].split(' + ')
        date = dt.datetime.strptime(pair[1].strip(), "%d.%m")
        date = date.replace(year=2022).date()

        pairsNamesDate.append([names, date])
    levels.append(pairsNamesDate.copy())

    print('\n-> '.join([' || '.join(map(str, level)) for level in levels]))

    for levelId in range(INFO["LEVELS_AMOUNT"]):
        level = levels[levelId]
        print(levelId)
        for pair in level:
            print(pair)
            date = pair[1]
            for name in pair[0]:
                db.addObject(Object(name, None, date), levelId)


if __name__ == '__main__':
    DBfromInput()
