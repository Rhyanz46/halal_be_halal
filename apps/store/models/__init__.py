from datetime import datetime
from core.database import db


class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), unique=True)
    description = db.Column(db.TEXT)
    address = db.Column(db.TEXT)
    img = db.Column(db.TEXT)
    lat = db.Column(db.Float, default=0.0)
    lang = db.Column(db.Float, default=0.0)
    foods = db.relationship('Food', backref='store')

    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_created = db.Column(db.DateTime, default=datetime.now())

    def __serialize__(self):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "lat": self.lat,
            "lang": self.lang
        }
        return data
