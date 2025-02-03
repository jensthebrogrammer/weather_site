from config import db   # imports our database


class TodayData(db.Model):
    pass

class UniqueIcons(db.Model):
    def __init__(self):
        id = db.Column(db.Integer, primary_key=True)
        event = db.Column(db.String(30), unique=True, nullable=False)
        icon = db.Column(db.String(100))

    def to_json(self):
        return {
            "event": self.event,
            "icon": self.icon
        }
