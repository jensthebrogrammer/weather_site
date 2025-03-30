from config import db, app   # imports our database
from sqlalchemy import PickleType  # for storing objects in the database


class DayWeather(db.Model):
    __bind_key__ = "dayWeather"

    _id = db.Column("id", db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    graph_string = db.Column(db.String(3000))
    time_table = db.Column(PickleType, nullable=False)
    wind_direction = db.Column(db.String(100))

    def __init__(self, location, date, graph_string, time_table, wind_direction):
        self.location = location
        self.date = date
        self.graph_string = graph_string
        self.time_table = time_table
        self.wind_direction = wind_direction

    def to_json(self):
        return {
            "location": self.location,
            "date": self.date,
            "graphString": self.graph_string,
            "timeTable": self.time_table,
            "windDirection": self.wind_direction
        }


class UniqueIcons(db.Model):
    __bind_key__ = "unique_icons"

    _id = db.Column("id", db.Integer, primary_key=True)
    event = db.Column(db.String(40), unique=True, nullable=False)
    icon = db.Column(db.String(300), nullable=False)

    def __init__(self, event, icon):
        self.icon = icon
        self.event = event

    def to_json(self):
        return {
            "event": self.event,
            "icon": self.icon
        }


class PreFetch(db.Model):
    __bind_key__ = "preFetch"

    # in all these different villages, there is going to one DayWeather stored
    # this will make the data quickly available
    _id = db.Column("id", db.Integer, primary_key=True)
    data = db.Column(PickleType, nullable=False)

    def __init__(self, data):
        self.data = data

    def to_json(self):
        return {
            "data": self.data
        }


class WeekData(db.Model):
    __bind_key__ = "week_data"

    _id = db.Column("id", db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False, unique=True)
    date = db.Column(db.String(30), nullable=False)
    day1 = db.Column(PickleType, nullable=False)
    day2 = db.Column(PickleType, nullable=False)
    day3 = db.Column(PickleType, nullable=False)
    day4 = db.Column(PickleType, nullable=False)
    day5 = db.Column(PickleType, nullable=False)
    day6 = db.Column(PickleType, nullable=False)
    day7 = db.Column(PickleType, nullable=False)

    def __init__(self, location, date, day1, day2, day3, day4, day5, day6, day7):
        self.location = location
        self.date = date
        self.day1 = day1
        self.day2 = day2
        self.day3 = day3
        self.day4 = day4
        self.day5 = day5
        self.day6 = day6
        self.day7 = day7

    def to_json(self):
        return {
            "location": self.location,
            'date': self.date,
            "day1": self.day1,
            "day2": self.day2,
            "day3": self.day3,
            "day4": self.day4,
            "day5": self.day5,
            "day6": self.day6,
            "day7": self.day7
        }


with app.app_context():
    db.create_all()
