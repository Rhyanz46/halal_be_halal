from core.database import db
from datetime import datetime


class CertificateGiver(db.Model):
    __tablename__: str = 'certificate_giver'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    certificates = db.relationship('Certificate', uselist=False, backref='certificate_giver', lazy=True)
    time_created = db.Column(db.DateTime, default=datetime.now())
