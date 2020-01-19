from core.database import db
from datetime import datetime


class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__: str = 'certificate'
    issuer_id = db.Column(db.Integer, db.ForeignKey('certificate_giver.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    number = db.Column(db.Integer, nullable=False)
    foods = db.relationship('Food', backref='certificate', lazy=True)
