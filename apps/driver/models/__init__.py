from core.database import db


class Driver(db.Model):
    __tablename__: str = 'driver'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    ratting = db.Column(db.Integer, default=0)
