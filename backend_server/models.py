#from config import db   # imports our database

'''
class dayWeather(db.Model):
    pass
'''

'''
class UniqueIcons(db.Model):
    __bind_key__= "unique_icons"
    def __init__(self):
        id = db.Column(db.Integer, primary_key=True)
        event = db.Column(db.String(30), unique=True, nullable=False)
        icon = db.Column(db.String(100))

    def to_json(self):
        return {
            "event": self.event,
            "icon": self.icon
        }
'''
