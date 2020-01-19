from core.database import db
from datetime import datetime


class Currency(db.Model):
    __tablename__: str = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    denote = db.Column(db.String(100), unique=True, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
