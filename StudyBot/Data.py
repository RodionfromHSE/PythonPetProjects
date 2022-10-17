import datetime as dt

INFO = {
    'INITIAL_LEVEL': 0,
    'LEVELS_AMOUNT': 5,
    'SHIFTS': [2, 4, 7, 10]
}

class Object:
    name = ""
    repDate = ""
    link = ""

    def __init__(self, name=None, link=None, repDate=None):
        if isinstance(repDate, str):
            repDate = dt.datetime.strptime(repDate, "%Y-%m-%d").date()
        self.name = name
        self.repDate = repDate
        self.link = link

    def shiftDate(self, days):
        self.repDate += dt.timedelta(days)

    def fromTuple(triple):
        assert len(triple) == 3
        name = triple[0]
        link = triple[1]
        repDate = triple[2]
        return Object(name, link, repDate)

    def __str__(self):
        if self.link is None or not self.link or self.link == 'None':
            return f"Object: {self.name} Date: {self.repDate}"
        return f"Object: [{self.name}]({self.link}) Date: {self.repDate}"



if __name__ == '__main__':
    topic = "Algebra"
    date = dt.date.today()
    link = "a"
    name = ' '.join((topic, str(date)))
    isinstance(date, dt.date)
    l = [name, link, date]
    object = Object.fromTuple(l)
    print(object)
    object.shiftDate(11)
    print(object)


