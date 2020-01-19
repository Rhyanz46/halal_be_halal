from core.database import db
from datetime import datetime


class PaymentMethod(db.Model):
    __tablename__: str = 'payment_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.now())
