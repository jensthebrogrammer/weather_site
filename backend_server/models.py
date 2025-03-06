from config import db   # imports our database
from sqlalchemy.types import PickleType  # for storing objects in the database


class DayWeather(db.Model):
    __bind_key__ = "dayWeather"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(30), nullable=False)
    graph_string = db.Column(db.String(3000))
    time_table = db.Column(PickleType, nullable=False)
    wind_direction = db.Column(db.String(100))

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

    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(40), unique=True, nullable=False)
    icon = db.Column(db.String(300), nullable=False)

    def to_json(self):
        return {
            "event": self.event,
            "icon": self.icon
        }


class PreFetch(db.Model):
    __bind_key__ = "preFetch"

    # in all these different villages, there is going to one DayWeather stored
    # this will make the data quickly available
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(PickleType, nullable=False)

    def to_json(self):
        return {
            "data": self.data
        }


class WeekData(db.Model):
    __bind_key__ = "week_data"

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False, unique=True)
    date = db.Column(db.String(30), nullable=False)
    day1 = db.Column(PickleType, nullable=False)
    day2 = db.Column(PickleType, nullable=False)
    day3 = db.Column(PickleType, nullable=False)
    day4 = db.Column(PickleType, nullable=False)
    day5 = db.Column(PickleType, nullable=False)
    day6 = db.Column(PickleType, nullable=False)
    day7 = db.Column(PickleType, nullable=False)

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
